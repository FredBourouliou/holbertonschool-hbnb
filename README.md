# HBnB - Holberton Airbnb Clone Project

HBnB is an Airbnb clone project developed as part of the Holberton School curriculum. This project implements a property rental platform with a scalable architecture divided into three parts.

## Project Structure

The project is organized into three main parts representing the development evolution:

```
holbertonschool-hbnb/
├── Project-1/      # Technical documentation and diagrams
├── part2/          # Business logic and API endpoints implementation
├── part3/          # Advanced backend with authentication and database
```

## Project-1: Technical Documentation

This part contains the complete technical documentation of the project:

- **High-Level Package Diagram** - Three-layer architecture
- **Business Logic Layer Class Diagram** - Entity relationships
- **API Sequence Diagrams** - Operation workflows
- **Complete Documentation** - Design decisions and implementation guidelines

## Part 2: Business Logic and API Implementation

This part implements:

- RESTful API for managing users, properties, reviews, and amenities
- Business logic layer with domain base classes
- Service layer using the Facade pattern
- In-memory persistence layer (temporary)

### Installation and Execution (Part 2)

```bash
cd part2/hbnb
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## Part 3: Advanced Backend with Authentication and Database

This part extends the backend by adding:

- JWT-based authentication and role-based access control
- Database integration with SQLAlchemy
- SQLite for development and MySQL configuration for production
- Data persistence and entity relationships

### Installation and Execution (Part 3)

```bash
cd part3/hbnb
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Database initialization
cd sql
./setup_database.sh
cd ..

# Create admin user (optional)
python init_admin.py

# Start the application
python run.py
```

The application will be accessible at http://localhost:5000 with interactive API documentation available at http://localhost:5000/api/v1.

## Main Components

- **API Layer**: RESTful endpoints secured by JWT
- **Business Logic**: Domain models and business rules
- **Service Layer**: Facade pattern to coordinate interactions
- **Persistence Layer**: Repository pattern with SQLite/MySQL database
- **Authentication**: JWT authentication and role-based authorization

## Main Entities

1. **User**: Application users
2. **Place**: Properties/locations for rent
3. **Review**: User evaluations of places
4. **Amenity**: Facilities/amenities available in places

## Diagram Documentation

The `part3/diagrams` folder contains Mermaid.js diagrams describing:

- Entity-Relationship (ER) diagram for the database structure
- Class diagram for SQLAlchemy models
- Architecture diagram for the application

## Environment and Configuration

Configurable environment variables (Part 3):

- `FLASK_ENV`: Operating mode ("development", "testing", or "production")
- `DATABASE_URL`: Database connection string
- `JWT_SECRET_KEY`: Secret key for JWT token generation

## Tests

Comprehensive tests are available for each part of the project:

```bash
# In the part2/hbnb or part3/hbnb folder
pytest
```