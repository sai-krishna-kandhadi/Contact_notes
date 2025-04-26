# Contact Notes System

A FastAPI-based backend service for managing contact notes with JWT authentication and full CRUD operations.

## Features

- JWT-based authentication
- Full CRUD operations for Contacts and Notes
- Field normalization for note data
- Asynchronous note processing using Celery
- RESTful API endpoints
- SQLAlchemy ORM with PostgreSQL
- Automated testing

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=postgresql://user:password@localhost:5432/contact_notes_system
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379/0
```

4. Initialize the database:
```bash
alembic upgrade head
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

6. Start Celery worker (in a separate terminal):
```bash
celery -A app.worker worker --loglevel=info
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests using:
```bash
pytest
```

## Project Structure

```
contact-notes-system/
├── app/
│   ├── api/           # API routes
│   ├── core/          # Core functionality
│   ├── db/            # Database models and session
│   ├── models/        # Pydantic models
│   ├── schemas/       # Data schemas
│   ├── services/      # Business logic
│   ├── worker.py      # Celery worker configuration
│   └── main.py        # Application entry point
├── tests/             # Test files
├── alembic/           # Database migrations
├── .env               # Environment variables
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```

## Key Decisions and Tradeoffs

1. **Authentication**: Using JWT for stateless authentication, which is scalable but requires careful token management.

2. **Database**: PostgreSQL with SQLAlchemy ORM for robust data handling and migrations.

3. **Async Processing**: Using Celery for background tasks to decouple note processing from the main application flow.

4. **API Design**: RESTful endpoints with proper HTTP methods and status codes.