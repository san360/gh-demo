# Project Architecture Diagram

This diagram represents the overall architecture and data flow of the Insurance Products application, which is a full-stack web application for managing insurance products with a Flask backend API and JavaScript frontend.

## System Overview

The application follows a typical client-server architecture with the following main components:

- **Frontend**: JavaScript-based SPA using Bootstrap for UI
- **Backend**: Flask REST API server
- **Data Storage**: JSON file-based storage
- **Testing**: Comprehensive test suites for both frontend and backend

## Architecture Diagram

```mermaid
graph TB
    %% User Interface Layer
    subgraph "Client-Side (Port 3000)"
        Browser[Web Browser]
        Frontend[Frontend Application]
        subgraph "Frontend Components"
            HTML[index.html<br/>Main UI Structure]
            JS[app.js<br/>ProductManager Class]
            CSS[styles.css<br/>Bootstrap + Custom Styles]
        end
    end

    %% API Layer
    subgraph "Server-Side (Port 5000)"
        API[Flask REST API]
        subgraph "Backend Components"
            FlaskApp[app.py<br/>Flask Application]
            Routes[API Routes<br/>CRUD Operations]
            Validation[Data Validation<br/>Input Sanitization]
        end
    end

    %% Data Layer
    subgraph "Data Storage"
        JSON[products.json<br/>Product Data Storage]
    end

    %% Testing Infrastructure
    subgraph "Testing Layer"
        subgraph "Frontend Tests"
            VitestTests[frontend.test.js<br/>Vitest Tests]
            TestSetup[setup.js<br/>Test Configuration]
        end
        subgraph "Backend Tests"
            PytestTests[test_api.py<br/>Pytest Tests]
            Conftest[conftest.py<br/>Test Fixtures]
        end
    end

    %% Development Tools
    subgraph "Development Environment"
        Vite[Vite Dev Server<br/>Frontend Development]
        DevServer[dev_server.py<br/>Development Orchestration]
        PackageJSON[package.json<br/>Node.js Dependencies]
        Requirements[requirements.txt<br/>Python Dependencies]
    end

    %% User Interactions and Data Flow
    Browser --> Frontend
    Frontend --> HTML
    Frontend --> JS
    Frontend --> CSS
    
    JS -->|HTTP Requests| API
    API --> FlaskApp
    FlaskApp --> Routes
    Routes --> Validation
    Validation --> JSON
    JSON -->|Data Response| Routes
    Routes -->|JSON Response| JS

    %% API Endpoints
    Routes -->|GET /api/products| JSON
    Routes -->|POST /api/products| JSON
    Routes -->|PUT /api/products/:id| JSON
    Routes -->|DELETE /api/products/:id| JSON

    %% Development Workflow
    DevServer --> Vite
    DevServer --> FlaskApp
    
    %% Testing Relationships
    VitestTests -.->|Tests| JS
    PytestTests -.->|Tests| FlaskApp
    TestSetup -.->|Configures| VitestTests
    Conftest -.->|Provides Fixtures| PytestTests

    %% Styling
    classDef frontend fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef backend fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef data fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef testing fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef dev fill:#fafafa,stroke:#424242,stroke-width:2px

    class Browser,Frontend,HTML,JS,CSS frontend
    class API,FlaskApp,Routes,Validation backend
    class JSON data
    class VitestTests,TestSetup,PytestTests,Conftest testing
    class Vite,DevServer,PackageJSON,Requirements dev
```

## API Data Flow Diagram

```mermaid
sequenceDiagram
    participant User as User
    participant UI as Frontend (JS)
    participant API as Flask API
    participant Data as products.json

    Note over User,Data: Product Management Workflow

    %% Load Products
    User->>UI: Opens Application
    UI->>API: GET /api/products
    API->>Data: load_products()
    Data-->>API: Product List
    API-->>UI: JSON Response with formatted_price
    UI-->>User: Display Product Cards

    %% Create Product
    User->>UI: Clicks "Add New Product"
    UI->>User: Shows Modal Form
    User->>UI: Fills Form & Clicks Save
    UI->>API: POST /api/products + JSON data
    API->>API: validate_product()
    API->>Data: save_products()
    Data-->>API: Success
    API-->>UI: New Product with ID + formatted_price
    UI-->>User: Updates UI & Shows Success Toast

    %% Edit Product
    User->>UI: Clicks Edit on Product
    UI->>User: Shows Pre-filled Modal
    User->>UI: Modifies Data & Saves
    UI->>API: PUT /api/products/{id} + JSON data
    API->>API: validate_product()
    API->>Data: save_products()
    Data-->>API: Success
    API-->>UI: Updated Product Data
    UI-->>User: Updates UI & Shows Success Toast

    %% Delete Product
    User->>UI: Clicks Delete on Product
    UI->>User: Shows Confirmation Dialog
    User->>UI: Confirms Deletion
    UI->>API: DELETE /api/products/{id}
    API->>Data: save_products()
    Data-->>API: Success
    API-->>UI: Delete Confirmation
    UI-->>User: Removes from UI & Shows Success Toast
```

## File Structure Overview

```mermaid
graph LR
    subgraph "Project Root"
        Root[gh-demo/]
        
        subgraph "Source Code"
            SrcDir[src/]
            Backend[backend/app.py]
            Frontend[frontend/]
            FrontendFiles[index.html<br/>app.js<br/>styles.css]
        end
        
        subgraph "Tests"
            TestDir[test/]
            BackendTests[test_api.py<br/>conftest.py]
            FrontendTests[frontend.test.js<br/>setup.js]
        end
        
        subgraph "Documentation"
            DocsDir[docs/]
            APIDocs[api.md]
            DevDocs[development.md]
        end
        
        subgraph "Configuration"
            Config[package.json<br/>requirements.txt<br/>vite.config.js]
            Data[products.json]
            DevScript[dev_server.py]
        end
    end

    Root --> SrcDir
    Root --> TestDir
    Root --> DocsDir
    Root --> Config
    Root --> Data
    Root --> DevScript
    
    SrcDir --> Backend
    SrcDir --> Frontend
    Frontend --> FrontendFiles
    
    TestDir --> BackendTests
    TestDir --> FrontendTests

    DocsDir --> APIDocs
    DocsDir --> DevDocs
```

## Technology Stack

- **Frontend**:
  - JavaScript ES2022 with ESM modules
  - Bootstrap 5.3.2 for responsive UI
  - Vite for development server and build tooling
  - Vitest for testing with JSDOM environment

- **Backend**:
  - Python 3.11+ with Flask framework
  - Flask-CORS for cross-origin request handling
  - JSON file-based data persistence
  - Pytest for comprehensive API testing

- **Development Tools**:
  - Custom development server orchestration script
  - Comprehensive test coverage for both layers
  - Modular project structure following best practices

## Key Features Illustrated

1. **CRUD Operations**: Complete Create, Read, Update, Delete functionality for insurance products
2. **Real-time UI Updates**: Frontend immediately reflects backend changes
3. **Input Validation**: Both client-side and server-side validation
4. **Currency Formatting**: Consistent USD formatting with two decimal places
5. **Error Handling**: Comprehensive error handling with user-friendly messages
6. **Responsive Design**: Bootstrap-based responsive UI components
7. **Testing Coverage**: Unit tests for both frontend and backend components
