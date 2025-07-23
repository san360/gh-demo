import unittest
import json
import os
import tempfile
from typing import Dict, Any

from app import app, users, blocklist


class TestAuthenticationAPI(unittest.TestCase):
    """
    Test cases for the authentication and authorization system.
    """
    
    def setUp(self) -> None:
        """Set up test environment before each test."""
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        self.app = app.test_client()
        
        # Clear the blocklist before each test
        blocklist.clear()
        
        # Create a temporary products file for testing
        self.temp_products = [
            {
                "id": 1,
                "name": "Test Insurance",
                "description": "Test product",
                "price": 100.0,
                "coverage": "Basic",
                "deductible": 500
            }
        ]
        
        with open('products.json', 'w') as f:
            json.dump(self.temp_products, f)
    
    def tearDown(self) -> None:
        """Clean up after each test."""
        # Remove test products file if it exists
        if os.path.exists('products.json'):
            os.remove('products.json')
    
    def get_auth_headers(self, username: str = 'admin', 
                        password: str = 'admin123') -> Dict[str, str]:
        """
        Helper method to get authentication headers.
        
        Parameters:
            username (str): Username for login.
            password (str): Password for login.
        
        Returns:
            Dict[str, str]: Headers with Authorization token.
        """
        response = self.app.post('/api/login', 
                               json={'username': username, 'password': password})
        data = json.loads(response.data.decode())
        token = data.get('access_token')
        return {'Authorization': f'Bearer {token}'}
    
    def test_login_success(self) -> None:
        """Test successful login with valid credentials."""
        response = self.app.post('/api/login', 
                               json={'username': 'admin', 'password': 'admin123'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('access_token', data)
        self.assertEqual(data['user'], 'admin')
        self.assertEqual(data['role'], 'admin')
    
    def test_login_invalid_credentials(self) -> None:
        """Test login with invalid credentials."""
        response = self.app.post('/api/login', 
                               json={'username': 'admin', 'password': 'wrong'})
        
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data.decode())
        self.assertEqual(data['error'], 'Invalid credentials')
    
    def test_login_missing_data(self) -> None:
        """Test login with missing username or password."""
        response = self.app.post('/api/login', json={'username': 'admin'})
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode())
        self.assertEqual(data['error'], 'Username and password required')
    
    def test_logout_success(self) -> None:
        """Test successful logout."""
        headers = self.get_auth_headers()
        response = self.app.post('/api/logout', headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Successfully logged out')
    
    def test_get_products_requires_auth(self) -> None:
        """Test that getting products requires authentication."""
        response = self.app.get('/api/products')
        self.assertEqual(response.status_code, 401)
    
    def test_get_products_with_auth(self) -> None:
        """Test getting products with valid authentication."""
        headers = self.get_auth_headers()
        response = self.app.get('/api/products', headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('products', data)
    
    def test_get_product_by_id_with_auth(self) -> None:
        """Test getting a specific product with authentication."""
        headers = self.get_auth_headers()
        response = self.app.get('/api/products/1', headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('product', data)
        self.assertEqual(data['product']['id'], 1)
    
    def test_create_product_requires_admin(self) -> None:
        """Test that creating products requires admin role."""
        user_headers = self.get_auth_headers('user', 'user123')
        new_product = {
            'name': 'New Insurance',
            'description': 'New test product',
            'price': 200.0,
            'coverage': 'Premium',
            'deductible': 1000
        }
        
        response = self.app.post('/api/products', 
                               json=new_product, headers=user_headers)
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data.decode())
        self.assertEqual(data['error'], 'Admin access required')
    
    def test_create_product_with_admin(self) -> None:
        """Test creating a product with admin role."""
        admin_headers = self.get_auth_headers('admin', 'admin123')
        new_product = {
            'name': 'New Insurance',
            'description': 'New test product',
            'price': 200.0,
            'coverage': 'Premium',
            'deductible': 1000
        }
        
        response = self.app.post('/api/products', 
                               json=new_product, headers=admin_headers)
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn('product', data)
        self.assertEqual(data['product']['name'], 'New Insurance')
    
    def test_update_product_requires_admin(self) -> None:
        """Test that updating products requires admin role."""
        user_headers = self.get_auth_headers('user', 'user123')
        update_data = {'name': 'Updated Name'}
        
        response = self.app.put('/api/products/1', 
                              json=update_data, headers=user_headers)
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data.decode())
        self.assertEqual(data['error'], 'Admin access required')
    
    def test_delete_product_requires_admin(self) -> None:
        """Test that deleting products requires admin role."""
        user_headers = self.get_auth_headers('user', 'user123')
        
        response = self.app.delete('/api/products/1', headers=user_headers)
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data.decode())
        self.assertEqual(data['error'], 'Admin access required')
    
    def test_health_check_public(self) -> None:
        """Test that health check endpoint is publicly accessible."""
        response = self.app.get('/api/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['status'], 'healthy')


if __name__ == '__main__':
    unittest.main()