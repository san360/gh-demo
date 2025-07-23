"""
Test cases for Flask API authentication and authorization
"""
import json
import os
import shutil
import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    
    # Backup original products.json
    if os.path.exists('products.json'):
        shutil.copy('products.json', 'products.json.backup')
    
    with app.test_client() as client:
        yield client
    
    # Restore original products.json
    if os.path.exists('products.json.backup'):
        shutil.move('products.json.backup', 'products.json')


def test_login_success(client):
    """Test successful login with valid credentials."""
    response = client.post('/api/auth/login', 
                          json={'username': 'admin', 'password': 'admin123'})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['username'] == 'admin'
    assert data['user']['role'] == 'admin'


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post('/api/auth/login',
                          json={'username': 'admin', 'password': 'wrong'})
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Invalid credentials' in data['error']


def test_login_missing_credentials(client):
    """Test login with missing credentials."""
    response = client.post('/api/auth/login', json={'username': 'admin'})
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Username and password required' in data['error']


def test_get_products_without_token(client):
    """Test accessing products endpoint without authentication token."""
    response = client.get('/api/products')
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Authentication token required' in data['error']


def test_get_products_with_valid_token(client):
    """Test accessing products endpoint with valid authentication token."""
    # First, get a token
    login_response = client.post('/api/auth/login',
                                json={'username': 'user', 'password': 'user123'})
    token = json.loads(login_response.data)['access_token']
    
    # Then use the token to access products
    response = client.get('/api/products',
                         headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_get_single_product_with_valid_token(client):
    """Test accessing single product endpoint with valid authentication token."""
    # First, get a token
    login_response = client.post('/api/auth/login',
                                json={'username': 'user', 'password': 'user123'})
    token = json.loads(login_response.data)['access_token']
    
    # Then use the token to access a specific product
    response = client.get('/api/products/1',
                         headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == 1


def test_get_nonexistent_product(client):
    """Test accessing non-existent product."""
    # First, get a token
    login_response = client.post('/api/auth/login',
                                json={'username': 'user', 'password': 'user123'})
    token = json.loads(login_response.data)['access_token']
    
    # Then try to access a non-existent product
    response = client.get('/api/products/999',
                         headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Product not found' in data['error']


def test_create_product_without_token(client):
    """Test creating product without authentication token."""
    new_product = {
        'name': 'Test Insurance',
        'description': 'Test product',
        'price': 100.0,
        'coverage': 'Test Coverage',
        'deductible': 500.0
    }
    
    response = client.post('/api/products', json=new_product)
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Authentication token required' in data['error']


def test_create_product_user_role(client):
    """Test creating product with user role (should fail)."""
    # Get token for regular user
    login_response = client.post('/api/auth/login',
                                json={'username': 'user', 'password': 'user123'})
    token = json.loads(login_response.data)['access_token']
    
    new_product = {
        'name': 'Test Insurance',
        'description': 'Test product',
        'price': 100.0,
        'coverage': 'Test Coverage',
        'deductible': 500.0
    }
    
    response = client.post('/api/products', 
                          json=new_product,
                          headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 403
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Admin access required' in data['error']


def test_create_product_admin_role(client):
    """Test creating product with admin role (should succeed)."""
    # Get token for admin user
    login_response = client.post('/api/auth/login',
                                json={'username': 'admin', 'password': 'admin123'})
    token = json.loads(login_response.data)['access_token']
    
    new_product = {
        'name': 'Test Insurance',
        'description': 'Test product',
        'price': 100.0,
        'coverage': 'Test Coverage',
        'deductible': 500.0
    }
    
    response = client.post('/api/products',
                          json=new_product,
                          headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Test Insurance'
    assert data['price'] == 100.0


def test_create_product_missing_fields(client):
    """Test creating product with missing required fields."""
    # Get token for admin user
    login_response = client.post('/api/auth/login',
                                json={'username': 'admin', 'password': 'admin123'})
    token = json.loads(login_response.data)['access_token']
    
    incomplete_product = {
        'name': 'Test Insurance',
        'price': 100.0
        # Missing other required fields
    }
    
    response = client.post('/api/products',
                          json=incomplete_product,
                          headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Missing required field' in data['error']


def test_update_product_admin_role(client):
    """Test updating product with admin role (should succeed)."""
    # Get token for admin user
    login_response = client.post('/api/auth/login',
                                json={'username': 'admin', 'password': 'admin123'})
    token = json.loads(login_response.data)['access_token']
    
    update_data = {
        'price': 150.0,
        'description': 'Updated description'
    }
    
    response = client.put('/api/products/1',
                         json=update_data,
                         headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['price'] == 150.0
    assert data['description'] == 'Updated description'


def test_delete_product_admin_role(client):
    """Test deleting product with admin role (should succeed)."""
    # Get token for admin user
    login_response = client.post('/api/auth/login',
                                json={'username': 'admin', 'password': 'admin123'})
    token = json.loads(login_response.data)['access_token']
    
    response = client.delete('/api/products/1',
                           headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'Product deleted successfully' in data['message']


def test_delete_product_user_role(client):
    """Test deleting product with user role (should fail)."""
    # Get token for regular user
    login_response = client.post('/api/auth/login',
                                json={'username': 'user', 'password': 'user123'})
    token = json.loads(login_response.data)['access_token']
    
    response = client.delete('/api/products/1',
                           headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 403
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Admin access required' in data['error']