# 🏥 Solum Health API

A comprehensive healthcare call management and evaluation system built with FastAPI, designed to handle patient calls, clinic management, and call quality evaluations.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)

## 🎯 Overview

Solum Health API is a robust healthcare management system that provides:

- **Call Management**: Track and manage patient calls with detailed metadata
- **Clinic Management**: Organize healthcare facilities and their relationships
- **Call Evaluation**: Quality assessment system for call recordings
- **User Management**: Secure authentication and role-based access control
- **Metrics & Analytics**: Performance insights and reporting capabilities

The system is built using a clean architecture pattern with clear separation of concerns between domain models, data access, and API layers.

## ✨ Features

### 🔐 Authentication & Authorization
- JWT-based authentication
- Role-based access control (Admin, User, Manager)
- Secure password hashing with bcrypt
- Session management

### 📞 Call Management
- Create and track patient calls
- Associate calls with clinics and assistants
- Store call metadata (duration, recording URLs, summaries)
- Multiple call statuses (in_progress, completed, failed, cancelled)
- Customer information tracking

### 🏥 Clinic Management
- Clinic registration and management
- Associate calls with specific clinics
- Clinic-based reporting and analytics

### 📊 Call Evaluation System
- Human and LLM-based evaluations
- Quality scoring (0-10 scale)
- Detailed feedback and comments
- Engineer review workflow
- Quality level classification

### 📈 Metrics & Analytics
- Performance metrics
- Call quality analytics
- Clinic performance tracking
- User activity monitoring

## 🏗️ Architecture

The project follows a clean architecture pattern with the following layers:

```
app/
├── domain/          # Business logic and domain models
├── data_acess/      # Database models and data access
├── repositories/    # Data access abstraction layer
├── services/        # Business logic services
├── routers/         # API endpoints and routing
├── utils/           # Utilities and helpers
└── main.py         # Application entry point
```

### Key Design Principles:
- **Domain-Driven Design**: Business logic encapsulated in domain models
- **Repository Pattern**: Abstract data access layer
- **Dependency Injection**: Clean service dependencies
- **Separation of Concerns**: Clear boundaries between layers

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.115.14
- **Database**: PostgreSQL with SQLAlchemy 2.0.41
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Authentication**: JWT with PyJWT
- **Password Hashing**: bcrypt via passlib
- **Migrations**: Alembic
- **Documentation**: Auto-generated OpenAPI/Swagger docs
- **Validation**: Pydantic models
- **CORS**: Cross-origin resource sharing enabled

## 📋 Prerequisites

Before running this application, ensure you have:

- **Python 3.8+** installed
- **PostgreSQL** database server running
- **pip** package manager
- **Git** for version control

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd back
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment**
   ```bash
   # Windows
   env\Scripts\activate
   
   # macOS/Linux
   source env/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Create environment file**
   ```bash
   cp .env.example .env
   ```

2. **Configure environment variables**
   ```bash
   # Database Configuration
   DB_TYPE=postgres
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=solum_health
   
   # JWT Configuration
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Application Configuration
   DEBUG=True
   CORS_ORIGINS=["*"]
   ```

## 🗄️ Database Setup

1. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE solum_health;
   ```

2. **Run database migrations**
   ```bash
   # Initialize Alembic (if not already done)
   alembic init alembic
   
   # Create initial migration
   alembic revision --autogenerate -m "Initial migration"
   
   # Apply migrations
   alembic upgrade head
   ```

For detailed migration instructions, see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md).

## 🏃‍♂️ Running the Application

### Development Server
```bash
# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server
```bash
# Run production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The application will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Documentation

The API provides comprehensive endpoints for all features:

### Authentication Endpoints
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/refresh` - Refresh access token

### User Management
- `GET /api/v1/users` - List users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{id}` - Get user details
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Clinic Management
- `GET /api/v1/clinics` - List clinics
- `POST /api/v1/clinics` - Create clinic
- `GET /api/v1/clinics/{id}` - Get clinic details
- `PUT /api/v1/clinics/{id}` - Update clinic
- `DELETE /api/v1/clinics/{id}` - Delete clinic

### Call Management
- `GET /api/v1/calls` - List calls
- `POST /api/v1/calls` - Create call
- `GET /api/v1/calls/{id}` - Get call details
- `PUT /api/v1/calls/{id}` - Update call
- `DELETE /api/v1/calls/{id}` - Delete call

### Evaluation System
- `GET /api/v1/evaluations` - List evaluations
- `POST /api/v1/evaluations` - Create evaluation
- `GET /api/v1/evaluations/{id}` - Get evaluation details
- `PUT /api/v1/evaluations/{id}` - Update evaluation

### Metrics & Analytics
- `GET /api/v1/metrics` - Get system metrics
- `GET /api/v1/metrics/calls` - Call analytics
- `GET /api/v1/metrics/quality` - Quality metrics

## 📁 Project Structure

```
back/
├── alembic/                 # Database migrations
├── app/
│   ├── data_acess/         # Database models
│   │   └── models.py       # SQLAlchemy models
│   ├── domain/             # Business logic models
│   │   ├── user_models.py  # User domain models
│   │   ├── clinics_models.py # Clinic & Call models
│   │   └── evaluation_models.py # Evaluation models
│   ├── repositories/       # Data access layer
│   │   ├── repository.py   # Base repository
│   │   ├── user_repository.py
│   │   ├── clinic_repository.py
│   │   ├── call_repository.py
│   │   └── evaluation_repository.py
│   ├── routers/            # API endpoints
│   │   ├── auth_router.py
│   │   ├── user_router.py
│   │   ├── clinic_router.py
│   │   ├── call_router.py
│   │   ├── evaluation_router.py
│   │   └── metrics_router.py
│   ├── services/           # Business logic
│   │   ├── user_services.py
│   │   ├── clinic_services.py
│   │   ├── call_services.py
│   │   └── evaluation_services.py
│   ├── utils/              # Utilities
│   │   ├── auth.py         # Authentication utilities
│   │   ├── dependencies.py # Dependency injection
│   │   ├── logger.py       # Logging configuration
│   │   └── mappers.py      # Data mappers
│   └── main.py            # Application entry point
├── env/                    # Virtual environment
├── migrations/             # Additional migrations
├── scripts/                # Utility scripts
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## 🛠️ Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints throughout the codebase
- Write docstrings for all functions and classes
- Use meaningful variable and function names

### Testing
```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=app
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Logging
The application uses structured logging with different levels:
- **DEBUG**: Detailed information for debugging
- **INFO**: General information about application flow
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failed operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Write clear commit messages
- Add tests for new features
- Update documentation as needed
- Follow the existing code style
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the migration guide in `MIGRATION_GUIDE.md`
- Open an issue in the repository

## 🔄 Version History

- **v1.0.0**: Initial release with core functionality
  - User authentication and management
  - Clinic and call management
  - Call evaluation system
  - Basic metrics and analytics

---

**Built with ❤️ for the healthcare community** 