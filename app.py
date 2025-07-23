import json
import os
from typing import Dict, List, Optional, Union
from datetime import timedelta

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, 
    get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

# In-memory user storage (for demo purposes)
users = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'role': 'admin'
    },
    'user': {
        'password': generate_password_hash('user123'),
        'role': 'user'
    }
}

# Blocklist for JWT tokens (for logout functionality)
blocklist = set()


def load_products() -> List[Dict]:
    """
    Load products from the JSON file.
    
    Returns:
        List[Dict]: List of product dictionaries.
    """
    try:
        with open('products.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_products(products: List[Dict]) -> None:
    """
    Save products to the JSON file.
    
    Parameters:
        products (List[Dict]): List of product dictionaries to save.
    """
    with open('products.json', 'w') as f:
        json.dump(products, f, indent=2)


def require_admin_role() -> Optional[Dict]:
    """
    Check if the current user has admin role.
    
    Returns:
        Optional[Dict]: Error response if user is not admin, None otherwise.
    """
    current_user = get_jwt_identity()
    user_data = users.get(current_user, {})
    
    if user_data.get('role') != 'admin':
        return {'error': 'Admin access required'}, 403
    return None


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header: Dict, jwt_payload: Dict) -> bool:
    """
    Check if a JWT token has been revoked (blocklisted).
    
    Parameters:
        jwt_header (Dict): JWT header.
        jwt_payload (Dict): JWT payload containing token data.
    
    Returns:
        bool: True if token is revoked, False otherwise.
    """
    return jwt_payload['jti'] in blocklist


@app.route('/api/login', methods=['POST'])
def login() -> Union[Dict, tuple]:
    """
    Authenticate user and return JWT access token.
    
    Returns:
        Union[Dict, tuple]: JWT token on success or error response.
    """
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    username = data['username']
    password = data['password']
    
    if username not in users:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not check_password_hash(users[username]['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify({
        'access_token': access_token,
        'user': username,
        'role': users[username]['role']
    })


@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout() -> Dict:
    """
    Logout user by adding their JWT token to blocklist.
    
    Returns:
        Dict: Success message.
    """
    jti = get_jwt()['jti']
    blocklist.add(jti)
    return jsonify({'message': 'Successfully logged out'})


@app.route('/api/products', methods=['GET'])
@jwt_required()
def get_products() -> Dict:
    """
    Get all products. Requires authentication.
    
    Returns:
        Dict: List of all products.
    """
    products = load_products()
    return jsonify({'products': products})


@app.route('/api/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id: int) -> Union[Dict, tuple]:
    """
    Get a specific product by ID. Requires authentication.
    
    Parameters:
        product_id (int): The ID of the product to retrieve.
    
    Returns:
        Union[Dict, tuple]: Product data or error response.
    """
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({'product': product})


@app.route('/api/products', methods=['POST'])
@jwt_required()
def create_product() -> Union[Dict, tuple]:
    """
    Create a new product. Requires admin role.
    
    Returns:
        Union[Dict, tuple]: Created product or error response.
    """
    admin_check = require_admin_role()
    if admin_check:
        return jsonify(admin_check[0]), admin_check[1]
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['name', 'description', 'price', 'coverage', 'deductible']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    products = load_products()
    
    # Generate new ID
    new_id = max([p['id'] for p in products], default=0) + 1
    
    new_product = {
        'id': new_id,
        'name': data['name'],
        'description': data['description'],
        'price': float(data['price']),
        'coverage': data['coverage'],
        'deductible': int(data['deductible'])
    }
    
    products.append(new_product)
    save_products(products)
    
    return jsonify({'product': new_product}), 201


@app.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id: int) -> Union[Dict, tuple]:
    """
    Update an existing product. Requires admin role.
    
    Parameters:
        product_id (int): The ID of the product to update.
    
    Returns:
        Union[Dict, tuple]: Updated product or error response.
    """
    admin_check = require_admin_role()
    if admin_check:
        return jsonify(admin_check[0]), admin_check[1]
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    products = load_products()
    product_index = next((i for i, p in enumerate(products) 
                         if p['id'] == product_id), None)
    
    if product_index is None:
        return jsonify({'error': 'Product not found'}), 404
    
    # Update product fields
    product = products[product_index]
    for field in ['name', 'description', 'price', 'coverage', 'deductible']:
        if field in data:
            if field == 'price':
                product[field] = float(data[field])
            elif field == 'deductible':
                product[field] = int(data[field])
            else:
                product[field] = data[field]
    
    products[product_index] = product
    save_products(products)
    
    return jsonify({'product': product})


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id: int) -> Union[Dict, tuple]:
    """
    Delete a product. Requires admin role.
    
    Parameters:
        product_id (int): The ID of the product to delete.
    
    Returns:
        Union[Dict, tuple]: Success message or error response.
    """
    admin_check = require_admin_role()
    if admin_check:
        return jsonify(admin_check[0]), admin_check[1]
    
    products = load_products()
    product_index = next((i for i, p in enumerate(products) 
                         if p['id'] == product_id), None)
    
    if product_index is None:
        return jsonify({'error': 'Product not found'}), 404
    
    deleted_product = products.pop(product_index)
    save_products(products)
    
    return jsonify({
        'message': 'Product deleted successfully',
        'product': deleted_product
    })


@app.route('/api/health', methods=['GET'])
def health_check() -> Dict:
    """
    Health check endpoint - publicly accessible.
    
    Returns:
        Dict: Health status.
    """
    return jsonify({'status': 'healthy', 'message': 'API is running'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)