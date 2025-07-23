"""
Flask API for Insurance Products with JWT Authentication and Role-Based Authorization
"""
import json
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, List, Optional, Any

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity,
    get_jwt
)


app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.environ.get(
    'JWT_SECRET_KEY', 
    'your-secret-key-change-in-production'
)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

# Sample users database (in production, use a proper database)
USERS = {
    'admin': {
        'password': 'admin123',  # In production, use hashed passwords
        'role': 'admin'
    },
    'user': {
        'password': 'user123',  # In production, use hashed passwords
        'role': 'user'
    }
}


def load_products() -> List[Dict[str, Any]]:
    """
    Load products from JSON file.
    
    Returns:
        List[Dict[str, Any]]: List of product dictionaries
    """
    try:
        with open('products.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_products(products: List[Dict[str, Any]]) -> None:
    """
    Save products to JSON file.
    
    Parameters:
        products (List[Dict[str, Any]]): List of product dictionaries to save
    """
    with open('products.json', 'w') as f:
        json.dump(products, f, indent=2)


def require_admin():
    """
    Decorator to require admin role for endpoint access.
    
    Returns:
        Response with 403 error if user is not admin, otherwise allows access
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            claims = get_jwt()
            
            if not current_user or claims.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token.
    
    Expected JSON payload:
        {
            "username": "string",
            "password": "string"
        }
    
    Returns:
        JSON response with access token or error message
    """
    if not request.json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    user = USERS.get(username)
    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Create token with user role in claims
    additional_claims = {'role': user['role']}
    access_token = create_access_token(
        identity=username,
        additional_claims=additional_claims
    )
    
    return jsonify({
        'access_token': access_token,
        'user': {
            'username': username,
            'role': user['role']
        }
    })


@app.route('/api/products', methods=['GET'])
@jwt_required()
def get_products():
    """
    Get all insurance products.
    Requires valid JWT token.
    
    Returns:
        JSON response with list of products
    """
    products = load_products()
    return jsonify(products)


@app.route('/api/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id: int):
    """
    Get a specific insurance product by ID.
    Requires valid JWT token.
    
    Parameters:
        product_id (int): ID of the product to retrieve
    
    Returns:
        JSON response with product data or error message
    """
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify(product)


@app.route('/api/products', methods=['POST'])
@jwt_required()
@require_admin()
def create_product():
    """
    Create a new insurance product.
    Requires valid JWT token and admin role.
    
    Expected JSON payload:
        {
            "name": "string",
            "description": "string",
            "price": float,
            "coverage": "string",
            "deductible": float
        }
    
    Returns:
        JSON response with created product or error message
    """
    if not request.json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    required_fields = ['name', 'description', 'price', 'coverage', 'deductible']
    for field in required_fields:
        if field not in request.json:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    products = load_products()
    
    # Generate new ID
    new_id = max([p['id'] for p in products], default=0) + 1
    
    new_product = {
        'id': new_id,
        'name': request.json['name'],
        'description': request.json['description'],
        'price': float(request.json['price']),
        'coverage': request.json['coverage'],
        'deductible': float(request.json['deductible'])
    }
    
    products.append(new_product)
    save_products(products)
    
    return jsonify(new_product), 201


@app.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()
@require_admin()
def update_product(product_id: int):
    """
    Update an existing insurance product.
    Requires valid JWT token and admin role.
    
    Parameters:
        product_id (int): ID of the product to update
    
    Returns:
        JSON response with updated product or error message
    """
    if not request.json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    products = load_products()
    product_index = next(
        (i for i, p in enumerate(products) if p['id'] == product_id), 
        None
    )
    
    if product_index is None:
        return jsonify({'error': 'Product not found'}), 404
    
    # Update only provided fields
    updatable_fields = ['name', 'description', 'price', 'coverage', 'deductible']
    for field in updatable_fields:
        if field in request.json:
            if field in ['price', 'deductible']:
                products[product_index][field] = float(request.json[field])
            else:
                products[product_index][field] = request.json[field]
    
    save_products(products)
    
    return jsonify(products[product_index])


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
@require_admin()
def delete_product(product_id: int):
    """
    Delete an insurance product.
    Requires valid JWT token and admin role.
    
    Parameters:
        product_id (int): ID of the product to delete
    
    Returns:
        JSON response confirming deletion or error message
    """
    products = load_products()
    product_index = next(
        (i for i, p in enumerate(products) if p['id'] == product_id), 
        None
    )
    
    if product_index is None:
        return jsonify({'error': 'Product not found'}), 404
    
    deleted_product = products.pop(product_index)
    save_products(products)
    
    return jsonify({
        'message': 'Product deleted successfully',
        'deleted_product': deleted_product
    })


@app.errorhandler(401)
def unauthorized(error):
    """Handle unauthorized access attempts."""
    return jsonify({'error': 'Authentication required'}), 401


@app.errorhandler(403)
def forbidden(error):
    """Handle forbidden access attempts."""
    return jsonify({'error': 'Insufficient permissions'}), 403


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired token attempts."""
    return jsonify({'error': 'Token has expired'}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid token attempts."""
    return jsonify({'error': 'Invalid token'}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing token attempts."""
    return jsonify({'error': 'Authentication token required'}), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)