# Insurance Products Application

A full-stack application for managing insurance products with a Flask backend API and JavaScript frontend.

## Project Structure

```
├── src/                    # Source code
│   ├── backend/           # Flask API backend
│   └── frontend/          # JavaScript frontend
├── test/                  # Test files
├── docs/                  # Documentation
├── assets/               # Static assets
├── products.json         # Product data
└── README.md            # This file
```

## Features

- Insurance product catalog management
- RESTful API with Flask
- Responsive frontend with Bootstrap
- Currency formatting (USD with two decimals)
- Comprehensive testing with pytest and Vitest

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 20+

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask development server:
```bash
python src/backend/app.py
```

### Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

### Testing

- Backend tests: `pytest`
- Frontend tests: `npm test`

## API Endpoints

- `GET /api/products` - Get all products
- `GET /api/products/{id}` - Get product by ID
- `POST /api/products` - Create new product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

## Contributing

1. Create feature branch from `dev`
2. Follow coding guidelines in `.github/instructions/`
3. Write tests for new features
4. Submit pull request with clear commit messages
