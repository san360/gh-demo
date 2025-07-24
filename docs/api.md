# API Documentation

## Insurance Products REST API

Base URL: `http://localhost:5000/api`

### Endpoints

#### GET /products
Get all insurance products.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Auto Insurance",
    "description": "Comprehensive coverage for your vehicle",
    "price": 125.99,
    "coverage": "Full Coverage",
    "deductible": 500,
    "formatted_price": "$125.99"
  }
]
```

#### GET /products/{id}
Get a specific product by ID.

**Parameters:**
- `id` (integer): Product ID

**Response:**
```json
{
  "id": 1,
  "name": "Auto Insurance",
  "description": "Comprehensive coverage for your vehicle",
  "price": 125.99,
  "coverage": "Full Coverage",
  "deductible": 500,
  "formatted_price": "$125.99"
}
```

**Error Response (404):**
```json
{
  "error": "Product not found"
}
```

#### POST /products
Create a new insurance product.

**Request Body:**
```json
{
  "name": "Life Insurance",
  "description": "Term life insurance for peace of mind",
  "price": 45.75,
  "coverage": "$500,000 Coverage",
  "deductible": 0
}
```

**Response (201):**
```json
{
  "id": 5,
  "name": "Life Insurance",
  "description": "Term life insurance for peace of mind",
  "price": 45.75,
  "coverage": "$500,000 Coverage",
  "deductible": 0,
  "formatted_price": "$45.75"
}
```

**Error Response (400):**
```json
{
  "error": "Missing required field: name"
}
```

#### PUT /products/{id}
Update an existing product.

**Parameters:**
- `id` (integer): Product ID

**Request Body:** Same as POST request

**Response:** Updated product object

#### DELETE /products/{id}
Delete a product.

**Parameters:**
- `id` (integer): Product ID

**Response:**
```json
{
  "message": "Product deleted successfully",
  "product": {
    "id": 1,
    "name": "Auto Insurance",
    ...
  }
}
```

### Validation Rules

- **name**: Required, string
- **description**: Required, string
- **price**: Required, non-negative number
- **coverage**: Required, string
- **deductible**: Optional, non-negative number (default: 0)

### Error Handling

All endpoints return appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request (validation errors)
- 404: Not Found
- 500: Internal Server Error

Error responses include a descriptive message:
```json
{
  "error": "Description of the error"
}
```
