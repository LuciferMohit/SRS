# Student Registration System (SRS)

A full-stack student registration system with a FastAPI backend and HTML frontend.

## Features
- Student registration and management
- PostgreSQL database for data persistence
- RESTful API with FastAPI
- Responsive HTML frontend
- Docker containerization

## Local Development

### Prerequisites
- Docker and Docker Compose
- Python 3.10+

### Running Locally with Docker

```bash
docker-compose up --build
```

The application will be available at:
- **Frontend**: http://localhost (port 80)
- **API**: http://localhost:8000 (port 8000)
- **Database**: PostgreSQL on port 5433

### API Endpoints

#### POST /students/
Register a new student.

Request:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "course": "Computer Science"
}
```

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "course": "Computer Science"
}
```

#### GET /students/
Retrieve all registered students.

Response:
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "course": "Computer Science"
  }
]
```

## Deployment

### Render Deployment

This project is configured for deployment on Render using `render.yaml`:

1. Push code to GitHub
2. Connect your GitHub repository to Render
3. Create a new service and import from repository
4. Render will automatically:
   - Create PostgreSQL database
   - Deploy the FastAPI backend
   - Deploy the static frontend
   - Set up environment variables

## Project Structure

```
.
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   └── ...
├── docker-compose.yml
├── render.yaml
└── SRS.html
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string

## Backend Stack
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Pydantic for validation

## Frontend
- HTML5
- Responsive design
- Fetch API for backend communication
