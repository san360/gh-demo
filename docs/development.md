# Development Guide

## Project Structure

```
├── src/
│   ├── backend/          # Flask API backend
│   │   └── app.py        # Main Flask application
│   └── frontend/         # JavaScript frontend
│       ├── index.html    # Main HTML file
│       ├── app.js        # Main JavaScript application
│       └── styles.css    # Custom CSS styles
├── test/                 # Test files
│   ├── conftest.py       # pytest configuration
│   ├── test_api.py       # Backend API tests
│   ├── setup.js          # Vitest setup
│   └── frontend.test.js  # Frontend tests
├── docs/                 # Documentation
├── assets/               # Static assets
├── products.json         # Product data storage
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies
└── vite.config.js        # Vite configuration
```

## Development Workflow

### 1. Environment Setup

**Python Environment:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Node.js Environment:**
```bash
npm install
```

### 2. Running the Application

**Backend (Terminal 1):**
```bash
cd src/backend
python app.py
```
Backend will run on: http://localhost:5000

**Frontend (Terminal 2):**
```bash
npm run dev
```
Frontend will run on: http://localhost:3000

### 3. Testing

**Backend Tests:**
```bash
pytest
pytest --coverage  # With coverage report
```

**Frontend Tests:**
```bash
npm test
npm run test:ui      # With UI
npm run test:coverage # With coverage
```

## Code Style Guidelines

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write descriptive docstrings for all functions
- Handle exceptions appropriately
- Use descriptive variable and function names

### JavaScript (Frontend)
- Use ES2022 features and ESM modules
- Prefer async/await over promises
- Use descriptive variable and function names
- Keep functions focused and small
- Avoid comments unless absolutely necessary

## API Integration

The frontend communicates with the backend via REST API calls:

```javascript
// Example API call
const response = await fetch(`${API_BASE_URL}/products`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(productData)
});
```

## Data Storage

Products are stored in `products.json` file. The structure is:

```json
[
  {
    "id": 1,
    "name": "Product Name",
    "description": "Product description",
    "price": 99.99,
    "coverage": "Coverage details",
    "deductible": 500
  }
]
```

## Adding New Features

1. **Backend Changes:**
   - Add new endpoints in `src/backend/app.py`
   - Add validation logic if needed
   - Write tests in `test/test_api.py`

2. **Frontend Changes:**
   - Update `src/frontend/app.js` for new functionality
   - Add UI components in `index.html`
   - Add styles in `styles.css`
   - Write tests in `test/frontend.test.js`

3. **Documentation:**
   - Update API documentation in `docs/api.md`
   - Update README.md if needed

## Debugging Tips

1. **Backend Issues:**
   - Check Flask debug output in terminal
   - Use print statements or logging
   - Test API endpoints with curl or Postman

2. **Frontend Issues:**
   - Use browser developer tools
   - Check network tab for API calls
   - Use console.log for debugging

3. **CORS Issues:**
   - Ensure Flask-CORS is properly configured
   - Check browser console for CORS errors

## Performance Considerations

- **Backend:** Use proper HTTP status codes and error handling
- **Frontend:** Implement loading states and error handling
- **Data:** Consider pagination for large datasets
- **Caching:** Implement client-side caching for better UX
