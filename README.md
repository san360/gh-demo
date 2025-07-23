# Insurance Products API

A secure Flask API for managing insurance products with JWT-based authentication and role-based access control.

## Features

- **JWT Authentication**: Secure token-based authentication system
- **Role-based Access Control**: Admin and user roles with different permissions
- **CRUD Operations**: Full Create, Read, Update, Delete operations for products
- **Secure Endpoints**: All API endpoints require authentication
- **Token Management**: Login/logout functionality with token blocklisting

## Security Implementation

This API addresses critical security vulnerabilities by implementing:

- **Authentication Required**: All product endpoints require valid JWT tokens
- **Role-based Authorization**: Admin-only access for write operations
- **Token Validation**: JWT tokens are validated on every request
- **Secure Logout**: Token blocklisting prevents reuse of logged-out tokens

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment configuration:
   ```bash
   cp .env.example .env
   ```

4. Set your JWT secret key in `.env`:
   ```
   JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
   ```

## Running the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

#### Login
```http
POST /api/login
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}
```

**Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": "admin",
    "role": "admin"
}
```

#### Logout
```http
POST /api/logout
Authorization: Bearer <token>
```

### Products

All product endpoints require authentication via JWT token in the Authorization header.

#### Get All Products
```http
GET /api/products
Authorization: Bearer <token>
```

#### Get Product by ID
```http
GET /api/products/{id}
Authorization: Bearer <token>
```

#### Create Product (Admin Only)
```http
POST /api/products
Authorization: Bearer <token>
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
```http
PUT /api/products/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Updated Auto Insurance",
    "price": 135.99
}
```

#### Delete Product (Admin Only)
```http
DELETE /api/products/{id}
Authorization: Bearer <token>
```

### Health Check
```http
GET /api/health
```

## User Accounts

Default user accounts for testing:

- **Admin User**:
  - Username: `admin`
  - Password: `admin123`
  - Role: `admin` (can perform all operations)

- **Regular User**:
  - Username: `user`
  - Password: `user123`
  - Role: `user` (read-only access)

## Testing

Run the test suite:

```bash
python -m unittest test_auth.py
```

The tests validate:
- Authentication system functionality
- Role-based access control
- JWT token management
- API endpoint security

## Security Features

### JWT Authentication
- All API endpoints (except health check) require valid JWT tokens
- Tokens expire after 1 hour for security
- Invalid or expired tokens return 401 Unauthorized

### Role-based Access Control
- **Admin Role**: Full access to all operations (CRUD)
- **User Role**: Read-only access to products
- Write operations (POST, PUT, DELETE) require admin role

### Token Management
- Secure login with password hashing
- Token blocklisting for logout functionality
- Automatic token validation on protected endpoints

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `JWT_SECRET_KEY` | Secret key for JWT token signing | `dev-secret-key` |
| `FLASK_ENV` | Flask environment | `development` |

**Important**: Change the JWT secret key in production!

## Data Storage

Products are stored in `products.json` file. In a production environment, this should be replaced with a proper database system.

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found