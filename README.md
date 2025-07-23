# Insurance Products API

A secure Flask API for managing insurance products with JWT authentication and role-based authorization.

## Features

- **JWT Authentication**: All endpoints require valid authentication tokens
- **Role-Based Access Control**: 
  - Regular users can read products
  - Admin users can create, update, and delete products
- **Secure by Default**: No endpoints are publicly accessible
- **Token Expiration**: Access tokens expire after 1 hour

## Security Implementation

✅ **All API endpoints require valid JWT token**  
✅ **Read operations require authenticated user**  
✅ **Write operations (POST, PUT, DELETE) require admin role**  
✅ **Proper error responses for unauthorized access**  
✅ **Token expiration and refresh mechanism**

## API Endpoints

### Authentication

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "user": {
    "username": "admin",
    "role": "admin"
  }
}
```

### Products

All product endpoints require `Authorization: Bearer <token>` header.

#### Get All Products
```bash
GET /api/products
Authorization: Bearer <token>
```

#### Get Single Product
```bash
GET /api/products/<id>
Authorization: Bearer <token>
```

#### Create Product (Admin Only)
```bash
POST /api/products
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "name": "Auto Insurance",
  "description": "Comprehensive coverage for your vehicle",
  "price": 125.99,
  "coverage": "Full Coverage",
  "deductible": 500
}
```

#### Update Product (Admin Only)
```bash
PUT /api/products/<id>
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "price": 150.00,
  "description": "Updated description"
}
```

#### Delete Product (Admin Only)
```bash
DELETE /api/products/<id>
Authorization: Bearer <admin-token>
```

## Default Users

- **Admin User**: username: `admin`, password: `admin123`
- **Regular User**: username: `user`, password: `user123`

## Installation and Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. The API will be available at `http://localhost:5000`

## Testing

Run the test suite:
```bash
python -m pytest test_app.py -v
```

## Error Responses

- **401 Unauthorized**: Missing or invalid token
- **403 Forbidden**: Insufficient permissions (admin required)
- **404 Not Found**: Product not found
- **400 Bad Request**: Invalid request data

## Production Notes

- Change the JWT secret key (`JWT_SECRET_KEY` environment variable)
- Use a proper database instead of JSON file storage
- Implement password hashing
- Add rate limiting
- Use HTTPS in production