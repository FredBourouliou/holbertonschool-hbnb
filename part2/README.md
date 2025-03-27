# HBnB - Business Logic and API

## Part 2: Implementation of Business Logic and API Endpoints

This part of the HBnB project focuses on implementing the core business logic and creating RESTful API endpoints for the Airbnb clone application. It provides the foundation for property rental management functionality without persistent storage (using in-memory repositories).

### Project Overview

In Part 2, we accomplish the following:

- Develop a clean, layered architecture with proper separation of concerns
- Implement core business entities (User, Place, Review, Amenity)
- Create RESTful API endpoints for all entities
- Establish a service layer using the Facade pattern for coordinating operations
- Provide in-memory data persistence (to be replaced with a database in Part 3)

### Architecture

The application follows a three-layer architecture:

1. **API Layer**: RESTful endpoints for CRUD operations on all entities
2. **Business Logic Layer**: Domain models and business rules
3. **Persistence Layer**: In-memory data storage (temporary implementation)

These layers communicate through a Facade service that handles the coordination between them, ensuring clean separation of concerns.

### Directory Structure

```
hbnb/
├── app/
│   ├── __init__.py          # Flask application instance
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── v1/              # API version 1
│   │       ├── __init__.py
│   │       ├── users.py     # User endpoints
│   │       ├── places.py    # Place endpoints
│   │       ├── reviews.py   # Review endpoints
│   │       ├── amenities.py # Amenity endpoints
│   ├── models/              # Business logic classes
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/            # Service layer with Facade pattern
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/         # Data persistence layer
│       ├── __init__.py
│       ├── repository.py
├── run.py                   # Application entry point
├── config.py                # Configuration settings
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
└── tests/                   # Test files for all components
```

### Key Features

- **User Management**: Create, read, update, and delete user accounts
- **Place Management**: List and manage rental properties with details
- **Review System**: Allow users to create and view property reviews
- **Amenity Tracking**: Manage available amenities for properties

### Setup and Installation

1. Navigate to the project directory:
   ```bash
   cd part2/hbnb
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python run.py
   ```

The application will start in development mode with debugging enabled at http://localhost:5000.

### API Documentation

The API follows RESTful conventions and provides the following endpoints:

- `/api/v1/users` - User management
- `/api/v1/places` - Property listing management
- `/api/v1/reviews` - Review management
- `/api/v1/amenities` - Amenity management

Each endpoint supports standard HTTP methods (GET, POST, PUT, DELETE) for CRUD operations.

### Testing

Comprehensive tests are included to verify API functionality and business logic:

```bash
python -m pytest
```

### Next Steps

This implementation serves as the foundation for Part 3, where we'll add:
- Database persistence with SQLAlchemy
- User authentication and authorization
- Enhanced security features
