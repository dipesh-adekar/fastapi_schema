# FastAPI Schema Application

A modern, production-ready FastAPI application with MongoDB, Redis caching, and JWT authentication.

## Features

- 🚀 **FastAPI** - High-performance async web framework
- 🍃 **MongoDB** - NoSQL database with Motor async driver
- 🔴 **Redis** - In-memory caching layer
- 🔐 **JWT Authentication** - Secure token-based authentication
- 🔒 **Password Hashing** - Bcrypt password encryption
- 📝 **Pydantic v2** - Data validation and serialization
- 🧪 **Pytest** - Comprehensive test suite
- 🐳 **Docker** - Containerized deployment
- 📊 **Type Safety** - Full type hints with Pyright

## Project Structure

```
fastapi_schema/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/
│   │       │   └── users.py      # User API endpoints
│   │       └── schemas/
│   │           └── user.py       # API response schemas
│   ├── core/
│   │   ├── cache.py              # Caching decorators
│   │   └── security.py           # Authentication & password hashing
│   ├── db/
│   │   ├── mongo_db.py            # MongoDB connection manager
│   │   └── redis.py               # Redis connection manager
│   ├── models/
│   │   ├── base.py                # Base MongoDB model
│   │   └── user.py                # User model
│   ├── schemas/
│   │   └── user.py                # Pydantic schemas
│   └── services/
│       └── user_service.py        # Business logic
├── tests/
│   ├── conftest.py                # Pytest configuration
│   └── users/
│       └── test_users.py          # User API tests
├── config.py                      # Application configuration
├── main.py                        # FastAPI application entry point
├── docker-compose.yml             # Docker services
├── Dockerfile                     # Application container
└── requirements.txt               # Python dependencies
```

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for local development)
- MongoDB 6.0+
- Redis 7.0+

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi_schema
   ```

2. **Start services**
   ```bash
   docker-compose up -d
   ```
   This will start:
   - MongoDB on port 27017
   - Redis on port 6379
   - Mongo Express on port 8081

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API**
   - API Documentation: http://localhost:8000/api/v1/sample-app/docs
   - Mongo Express: http://localhost:8081 (admin/password)

### Manual Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables** (optional, defaults provided)
   ```bash
   export MONGO_URL="mongodb://root:password@localhost:27017/fastapi_db?authSource=admin"
   export MONGO_DB_NAME="fastapi_db"
   export REDIS_URL="redis://localhost:6379"
   export SECRET_KEY="your-secret-key"
   export CACHE_ENABLED="true"
   ```

3. **Start MongoDB and Redis** (if not using Docker)
   ```bash
   # MongoDB
   mongod --auth

   # Redis
   redis-server
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## Configuration

Configuration is managed through environment variables in `config.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGO_URL` | `mongodb://root:password@localhost:27017/fastapi_db?authSource=admin` | MongoDB connection string |
| `MONGO_DB_NAME` | `fastapi_db` | Database name |
| `REDIS_URL` | `redis://localhost:6379` | Redis connection string |
| `SECRET_KEY` | `secret` | JWT secret key (change in production!) |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration time |
| `CACHE_ENABLED` | `true` | Enable/disable caching |
| `CACHE_TTL` | `60` | Cache time-to-live in seconds |

## API Endpoints

### Authentication

#### Register User
```http
POST /api/v1/sample-app/users/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

#### Login
```http
POST /api/v1/sample-app/users/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Users

#### List Users
```http
GET /api/v1/sample-app/users/?skip=0&limit=100&active_only=true
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 100, max: 1000)
- `active_only` (bool): Filter active users only (default: true)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "507f1f77bcf86cd799439011",
      "username": "johndoe",
      "email": "john@example.com",
      "full_name": "John Doe",
      "is_active": true,
      "created_at": "2026-01-27T10:00:00Z",
      "updated_at": "2026-01-27T10:00:00Z"
    }
  ],
  "pagination": {
    "skip": 0,
    "limit": 100,
    "has_more": false
  },
  "timestamp": "2026-01-27T10:00:00Z"
}
```

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/users/test_users.py

# Run with verbose output
pytest -v
```

## Development

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pre-commit install
```

Hooks include:
- **Ruff** - Fast Python linter and formatter
- **Type checking** - Pyright static type checking

### Code Quality

```bash
# run checks on all files
pre-commit run --all-files

# Format code
ruff format .

# Lint code
ruff check .

```

## Architecture

### Database Layer

- **MongoDB**: Primary data store using Motor async driver
- **Redis**: Caching layer for improved performance
- **Connection Pooling**: Configured for optimal performance

### Service Layer

- **UserService**: Business logic for user operations
- **Caching**: Decorator-based caching with Redis
- **Authentication**: JWT token generation and validation

### API Layer

- **FastAPI**: RESTful API with automatic OpenAPI documentation
- **Pydantic**: Request/response validation
- **Dependency Injection**: Database connections via FastAPI dependencies

## Security

- **Password Hashing**: Bcrypt with automatic handling of passwords > 72 bytes
- **JWT Tokens**: Secure token-based authentication
- **CORS**: Configurable CORS middleware
- **Input Validation**: Pydantic schema validation

## Caching

The application uses Redis for response caching:

- **Cache Decorator**: `@cache_response(ttl=60, key_prefix="user")`
- **Automatic Cache Invalidation**: On user creation/updates
- **Configurable TTL**: Per-endpoint cache expiration

## Docker

### Build Image

```bash
docker build -t fastapi-schema .
```

### Run Container

```bash
docker run -p 8000:8000 fastapi-schema
```

## Environment Variables

Create a `.env` file (optional):

```env
MONGO_URL=mongodb://root:password@localhost:27017/fastapi_db?authSource=admin
MONGO_DB_NAME=fastapi_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
CACHE_ENABLED=true
CACHE_TTL=60
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License

```
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

