"""
Flask application for insurance products API.

This module provides a RESTful API for managing insurance products
with CRUD operations and proper error handling.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from typing import List, Dict, Any, Optional
import json
import os

app = Flask(__name__)
CORS(app)

# Load products data
PRODUCTS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'products.json')


def load_products() -> List[Dict[str, Any]]:
    """Load products from JSON file."""
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_products(products: List[Dict[str, Any]]) -> None:
    """Save products to JSON file."""
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(products, file, indent=2)


def format_currency(amount: float) -> str:
    """Format currency as USD with two decimals."""
    return f"${amount:.2f}"


def validate_product(product: Dict[str, Any]) -> Optional[str]:
    """Validate product data and return error message if invalid."""
    required_fields = ['name', 'description', 'price', 'coverage']
    
    for field in required_fields:
        if field not in product:
            return f"Missing required field: {field}"
    
    if not isinstance(product['price'], (int, float)) or product['price'] < 0:
        return "Price must be a non-negative number"
    
    if 'deductible' in product:
        if not isinstance(product['deductible'], (int, float)) or product['deductible'] < 0:
            return "Deductible must be a non-negative number"
    
    return None


@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all insurance products."""
    products = load_products()
    
    # Format prices for display
    for product in products:
        product['formatted_price'] = format_currency(product['price'])
    
    return jsonify(products)


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id: int):
    """Get a specific product by ID."""
    products = load_products()
    
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    product['formatted_price'] = format_currency(product['price'])
    return jsonify(product)


@app.route('/api/products', methods=['POST'])
def create_product():
    """Create a new insurance product."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    error = validate_product(data)
    if error:
        return jsonify({'error': error}), 400
    
    products = load_products()
    
    # Generate new ID
    new_id = max([p['id'] for p in products], default=0) + 1
    
    new_product = {
        'id': new_id,
        'name': data['name'],
        'description': data['description'],
        'price': float(data['price']),
        'coverage': data['coverage'],
        'deductible': float(data.get('deductible', 0))
    }
    
    products.append(new_product)
    save_products(products)
    
    new_product['formatted_price'] = format_currency(new_product['price'])
    return jsonify(new_product), 201


@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id: int):
    """Update an existing product."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    products = load_products()
    product_index = next((i for i, p in enumerate(products) if p['id'] == product_id), None)
    
    if product_index is None:
        return jsonify({'error': 'Product not found'}), 404
    
    error = validate_product(data)
    if error:
        return jsonify({'error': error}), 400
    
    updated_product = products[product_index].copy()
    updated_product.update({
        'name': data['name'],
        'description': data['description'],
        'price': float(data['price']),
        'coverage': data['coverage'],
        'deductible': float(data.get('deductible', 0))
    })
    
    products[product_index] = updated_product
    save_products(products)
    
    updated_product['formatted_price'] = format_currency(updated_product['price'])
    return jsonify(updated_product)


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int):
    """Delete a product."""
    products = load_products()
    product_index = next((i for i, p in enumerate(products) if p['id'] == product_id), None)
    
    if product_index is None:
        return jsonify({'error': 'Product not found'}), 404
    
    deleted_product = products.pop(product_index)
    save_products(products)
    
    return jsonify({'message': 'Product deleted successfully', 'product': deleted_product})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
