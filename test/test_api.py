"""
Test cases for the insurance products API endpoints.

This module contains comprehensive tests for all API endpoints
including CRUD operations, validation, and error handling.
"""

import json
import pytest


class TestProductsAPI:
    """Test class for products API endpoints."""
    
    def test_get_products_success(self, client):
        """Test getting all products returns correct data."""
        response = client.get('/api/products')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['name'] == 'Test Auto Insurance'
        assert 'formatted_price' in data[0]
        assert data[0]['formatted_price'] == '$100.00'
    
    def test_get_product_by_id_success(self, client):
        """Test getting a specific product by ID."""
        response = client.get('/api/products/1')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 1
        assert data['name'] == 'Test Auto Insurance'
        assert 'formatted_price' in data
    
    def test_get_product_not_found(self, client):
        """Test getting non-existent product returns 404."""
        response = client.get('/api/products/999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Product not found'
    
    def test_create_product_success(self, client, sample_product):
        """Test creating a new product."""
        response = client.post('/api/products', 
                             data=json.dumps(sample_product),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == sample_product['name']
        assert data['price'] == sample_product['price']
        assert 'id' in data
        assert data['id'] == 2  # Should be assigned next available ID
        assert 'formatted_price' in data
    
    def test_create_product_missing_field(self, client):
        """Test creating product with missing required field."""
        incomplete_product = {
            "name": "Incomplete Product",
            "price": 100.00
            # Missing description and coverage
        }
        
        response = client.post('/api/products',
                             data=json.dumps(incomplete_product),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Missing required field' in data['error']
    
    def test_create_product_invalid_price(self, client):
        """Test creating product with invalid price."""
        invalid_product = {
            "name": "Invalid Product",
            "description": "Product with negative price",
            "price": -50.00,
            "coverage": "Basic"
        }
        
        response = client.post('/api/products',
                             data=json.dumps(invalid_product),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Price must be a non-negative number' in data['error']
    
    def test_update_product_success(self, client, sample_product):
        """Test updating an existing product."""
        updated_data = sample_product.copy()
        updated_data['name'] = 'Updated Insurance Product'
        updated_data['price'] = 200.00
        
        response = client.put('/api/products/1',
                            data=json.dumps(updated_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'Updated Insurance Product'
        assert data['price'] == 200.00
        assert data['id'] == 1
    
    def test_update_product_not_found(self, client, sample_product):
        """Test updating non-existent product."""
        response = client.put('/api/products/999',
                            data=json.dumps(sample_product),
                            content_type='application/json')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Product not found'
    
    def test_delete_product_success(self, client):
        """Test deleting a product."""
        response = client.delete('/api/products/1')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'Product deleted successfully'
        assert 'product' in data
        
        # Verify product is actually deleted
        get_response = client.get('/api/products/1')
        assert get_response.status_code == 404
    
    def test_delete_product_not_found(self, client):
        """Test deleting non-existent product."""
        response = client.delete('/api/products/999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Product not found'
    
    def test_create_product_no_data(self, client):
        """Test creating product with no data."""
        response = client.post('/api/products',
                             data='',
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'No data provided'
    
    def test_update_product_no_data(self, client):
        """Test updating product with no data."""
        response = client.put('/api/products/1',
                            data='',
                            content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'No data provided'


class TestUtilityFunctions:
    """Test class for utility functions."""
    
    def test_format_currency(self):
        """Test currency formatting function."""
        from src.backend.app import format_currency
        
        assert format_currency(100) == '$100.00'
        assert format_currency(99.99) == '$99.99'
        assert format_currency(0) == '$0.00'
        assert format_currency(1234.567) == '$1234.57'
    
    def test_validate_product_success(self):
        """Test product validation with valid data."""
        from src.backend.app import validate_product
        
        valid_product = {
            'name': 'Test Product',
            'description': 'Test description',
            'price': 100.00,
            'coverage': 'Full Coverage',
            'deductible': 500
        }
        
        error = validate_product(valid_product)
        assert error is None
    
    def test_validate_product_missing_field(self):
        """Test product validation with missing field."""
        from src.backend.app import validate_product
        
        invalid_product = {
            'name': 'Test Product',
            'price': 100.00
            # Missing description and coverage
        }
        
        error = validate_product(invalid_product)
        assert error is not None
        assert 'Missing required field' in error
    
    def test_validate_product_invalid_price(self):
        """Test product validation with invalid price."""
        from src.backend.app import validate_product
        
        invalid_product = {
            'name': 'Test Product',
            'description': 'Test description',
            'price': -100,
            'coverage': 'Full Coverage'
        }
        
        error = validate_product(invalid_product)
        assert error is not None
        assert 'Price must be a non-negative number' in error
