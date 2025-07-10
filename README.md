
"""
# Project Management API

A Django REST API for project management with user authentication, project management, task tracking, and commenting system.

## Features

- User registration and authentication with JWT tokens
- Project management with owner and member roles
- Task management with status tracking and assignment
- Comment system for task discussions
- RESTful API endpoints
- Swagger/OpenAPI documentation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project_management_api
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure settings:
```bash
# Update settings.py with your database configuration
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login user

### Users
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Projects
- `GET /api/projects/` - List projects
- `POST /api/projects/` - Create project
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project
- `GET /api/projects/{id}/tasks/` - Get project tasks

### Tasks
- `GET /api/tasks/` - List tasks
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `GET /api/tasks/{id}/comments/` - Get task comments

### Comments
- `GET /api/comments/` - List comments
- `POST /api/comments/` - Create comment
- `GET /api/comments/{id}/` - Get comment details
- `PUT /api/comments/{id}/` - Update comment
- `DELETE /api/comments/{id}/` - Delete comment

## Documentation

- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## Authentication

The API uses JWT token authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## Database Schema

The application uses the following models:
- User: Extended Django user model
- Project: Project information and ownership
- ProjectMember: Project membership with roles
- Task: Task management with status and priority
- Comment: Comments on tasks

## Testing

Run tests using:
```bash
python manage.py test
```

## Deployment

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure proper database (PostgreSQL recommended)
3. Set up proper static file handling
4. Configure CORS settings
5. Set up environment variables for sensitive data
"""