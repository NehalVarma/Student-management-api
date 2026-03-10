# Student Management API

Simple Django REST API for managing student records. Built during my backend development learning.

## What it does
- Create, read, update, delete students
- REST API with JSON responses  
- PostgreSQL database
- Django admin interface

## Tech Stack
- Django 4.2.9
- PostgreSQL
- Django REST Framework

## How to run

### Setup
```bash
# Install stuff
sudo apt install python3 python3-pip postgresql

# Start postgres
sudo service postgresql start

# Create database
sudo -u postgres createdb student_management_db
```

### Running the app
```bash
# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver
```

## API Endpoints
- `GET /api/students/` - Get all students
- `POST /api/students/` - Add new student
- `GET /api/students/{id}/` - Get specific student
- `PUT /api/students/{id}/` - Update student
- `DELETE /api/students/{id}/` - Delete student

## Testing
Use Postman or curl to test the endpoints.

## Notes
- Change database password in settings.py
- This is for learning purposes