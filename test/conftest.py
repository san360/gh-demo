"""
Test configuration and fixtures for the insurance products API.

This module provides pytest fixtures and configuration for testing
the Flask application with proper setup and teardown.
"""

import pytest
import json
import tempfile
import os
from src.backend.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    # Create a temporary file for testing
    test_products = [
        {
            "id": 1,
            "name": "Test Auto Insurance",
            "description": "Test auto coverage",
            "price": 100.00,
            "coverage": "Full Coverage",
            "deductible": 500
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(test_products, f)
        temp_file_path = f.name
    
    # Override the products file path for testing
    app.config['TESTING'] = True
    original_products_file = app.config.get('PRODUCTS_FILE')
    
    # Monkey patch the PRODUCTS_FILE
    import src.backend.app as app_module
    original_path = app_module.PRODUCTS_FILE
    app_module.PRODUCTS_FILE = temp_file_path
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    app_module.PRODUCTS_FILE = original_path
    os.unlink(temp_file_path)


@pytest.fixture
def sample_product():
    """Provide a sample product for testing."""
    return {
        "name": "Sample Insurance",
        "description": "Sample insurance product",
        "price": 150.75,
        "coverage": "Comprehensive",
        "deductible": 750
    }
