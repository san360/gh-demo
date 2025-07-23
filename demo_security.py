#!/usr/bin/env python3
"""
API Security Demonstration Script

This script demonstrates the security features of the Insurance Products API,
showing how authentication and authorization work to protect against
unauthorized access.
"""

import requests
import json
import time
import sys


def print_header(title: str) -> None:
    """Print a formatted header."""
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")


def print_step(step: str) -> None:
    """Print a formatted step."""
    print(f"\n→ {step}")


def make_request(method: str, url: str, **kwargs) -> requests.Response:
    """Make an HTTP request and display the result."""
    print(f"  {method} {url}")
    if kwargs.get('json'):
        print(f"  Data: {json.dumps(kwargs['json'], indent=2)}")
    if kwargs.get('headers'):
        auth_header = kwargs['headers'].get('Authorization', '')
        if auth_header:
            print(f"  Auth: {auth_header[:50]}...")
    
    response = requests.request(method, url, **kwargs)
    print(f"  Status: {response.status_code}")
    
    try:
        response_data = response.json()
        print(f"  Response: {json.dumps(response_data, indent=2)}")
    except:
        print(f"  Response: {response.text}")
    
    return response


def demonstrate_api_security():
    """Demonstrate the API security features."""
    base_url = "http://localhost:5000/api"
    
    print_header("Insurance Products API Security Demonstration")
    print("This demo shows how the API prevents unauthorized access")
    print("and implements proper authentication and role-based access control.")
    
    # Test 1: Try to access products without authentication
    print_header("1. Unauthorized Access Prevention")
    print_step("Attempting to access products without authentication")
    
    response = make_request("GET", f"{base_url}/products")
    if response.status_code == 401:
        print("  ✅ SUCCESS: Unauthorized access properly blocked")
    else:
        print("  ❌ FAILURE: Should have blocked unauthorized access")
        return
    
    # Test 2: Login with admin credentials
    print_header("2. Admin Authentication")
    print_step("Logging in with admin credentials")
    
    admin_login = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = make_request("POST", f"{base_url}/login", json=admin_login)
    if response.status_code != 200:
        print("  ❌ FAILURE: Admin login failed")
        return
    
    admin_token = response.json()['access_token']
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("  ✅ SUCCESS: Admin authenticated successfully")
    
    # Test 3: Access products with admin token
    print_header("3. Authenticated Access")
    print_step("Accessing products with valid admin token")
    
    response = make_request("GET", f"{base_url}/products", headers=admin_headers)
    if response.status_code == 200:
        print("  ✅ SUCCESS: Authenticated access granted")
    else:
        print("  ❌ FAILURE: Authenticated access should be allowed")
        return
    
    # Test 4: Create product as admin
    print_header("4. Admin Role Authorization")
    print_step("Creating new product (admin privilege)")
    
    new_product = {
        "name": "Demo Insurance",
        "description": "Security demonstration product",
        "price": 199.99,
        "coverage": "Demo Coverage",
        "deductible": 500
    }
    
    response = make_request("POST", f"{base_url}/products", 
                          json=new_product, headers=admin_headers)
    if response.status_code == 201:
        print("  ✅ SUCCESS: Admin can create products")
        created_product_id = response.json()['product']['id']
    else:
        print("  ❌ FAILURE: Admin should be able to create products")
        return
    
    # Test 5: Login with regular user
    print_header("5. Regular User Authentication")
    print_step("Logging in with regular user credentials")
    
    user_login = {
        "username": "user",
        "password": "user123"
    }
    
    response = make_request("POST", f"{base_url}/login", json=user_login)
    if response.status_code != 200:
        print("  ❌ FAILURE: User login failed")
        return
    
    user_token = response.json()['access_token']
    user_headers = {"Authorization": f"Bearer {user_token}"}
    print("  ✅ SUCCESS: Regular user authenticated successfully")
    
    # Test 6: Try to create product as regular user
    print_header("6. Role-Based Access Control")
    print_step("Attempting to create product as regular user (should fail)")
    
    response = make_request("POST", f"{base_url}/products", 
                          json=new_product, headers=user_headers)
    if response.status_code == 403:
        print("  ✅ SUCCESS: Regular user properly blocked from admin actions")
    else:
        print("  ❌ FAILURE: Regular user should not be able to create products")
        return
    
    # Test 7: Regular user can read products
    print_step("Regular user accessing products (read-only)")
    
    response = make_request("GET", f"{base_url}/products", headers=user_headers)
    if response.status_code == 200:
        print("  ✅ SUCCESS: Regular user can read products")
    else:
        print("  ❌ FAILURE: Regular user should be able to read products")
        return
    
    # Test 8: Logout functionality
    print_header("7. Secure Logout")
    print_step("Logging out admin user")
    
    response = make_request("POST", f"{base_url}/logout", headers=admin_headers)
    if response.status_code == 200:
        print("  ✅ SUCCESS: Logout successful")
    else:
        print("  ❌ FAILURE: Logout should work")
        return
    
    # Test 9: Try to use logged out token
    print_step("Attempting to use logged-out token (should fail)")
    
    response = make_request("GET", f"{base_url}/products", headers=admin_headers)
    if response.status_code == 401:
        print("  ✅ SUCCESS: Logged-out token properly rejected")
    else:
        print("  ❌ FAILURE: Logged-out token should be rejected")
        return
    
    # Clean up: Delete the demo product
    print_header("8. Cleanup")
    print_step("Logging back in as admin to clean up demo product")
    
    response = make_request("POST", f"{base_url}/login", json=admin_login)
    new_admin_token = response.json()['access_token']
    new_admin_headers = {"Authorization": f"Bearer {new_admin_token}"}
    
    response = make_request("DELETE", f"{base_url}/products/{created_product_id}", 
                          headers=new_admin_headers)
    if response.status_code == 200:
        print("  ✅ Demo product cleaned up successfully")
    
    print_header("Security Demonstration Complete")
    print("✅ All security features working correctly:")
    print("  • Authentication required for all endpoints")
    print("  • Role-based access control implemented")
    print("  • JWT token validation working")
    print("  • Secure logout functionality")
    print("  • Unauthorized access properly blocked")


if __name__ == "__main__":
    try:
        demonstrate_api_security()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to API server.")
        print("Please start the Flask application first with: python app.py")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)