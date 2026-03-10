# Student Management API

A Django REST API project for managing student records with full CRUD operations, built with Django, PostgreSQL, and Django REST Framework.

## Project Structure

```
student_management/
├── manage.py
├── requirements.txt
├── student_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── students/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── tests.py
```

## Features

- **CRUD Operations**: Create, Read, Update, Delete students
- **REST API**: JSON-based API endpoints
- **PostgreSQL Integration**: Professional database setup
- **Data Validation**: Email uniqueness and age validation
- **Admin Interface**: Django admin for data management
- **Unit Tests**: Comprehensive test coverage

## API Endpoints

- `GET /api/students/` - List all students
- `POST /api/students/` - Create a new student
- `GET /api/students/{id}/` - Get a specific student
- `PUT /api/students/{id}/` - Update a specific student
- `DELETE /api/students/{id}/` - Delete a specific student

## Setup Instructions (WSL Ubuntu)

### 1. Install Python and pip
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 2. Install PostgreSQL
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
CREATE DATABASE student_management_db;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE student_management_db TO postgres;
\q
```

### 3. Set up Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## Testing with Postman

### 1. Get All Students
- **Method**: GET
- **URL**: `http://127.0.0.1:8000/api/students/`
- **Headers**: `Content-Type: application/json`

### 2. Create Student
- **Method**: POST
- **URL**: `http://127.0.0.1:8000/api/students/`
- **Headers**: `Content-Type: application/json`
- **Body** (JSON):
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 22,
    "course": "Computer Science"
}
```

### 3. Get Specific Student
- **Method**: GET
- **URL**: `http://127.0.0.1:8000/api/students/1/`
- **Headers**: `Content-Type: application/json`

### 4. Update Student
- **Method**: PUT
- **URL**: `http://127.0.0.1:8000/api/students/1/`
- **Headers**: `Content-Type: application/json`
- **Body** (JSON):
```json
{
    "name": "John Updated",
    "email": "john.updated@example.com",
    "age": 23,
    "course": "Software Engineering"
}
```

### 5. Delete Student
- **Method**: DELETE
- **URL**: `http://127.0.0.1:8000/api/students/1/`

## Git Commands Used

```bash
# Initialize repository
git init

# Add files
git add .

# Commit changes
git commit -m "Initial Django project setup with CRUD operations"

# Add remote origin (replace with your repo URL)
git remote add origin https://github.com/your-username/student-management-api.git

# Push to remote
git push -u origin main

# Check status
git status

# View commit history
git log --oneline
```

## Running Tests

```bash
python manage.py test
```

## Database Commands

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser
```