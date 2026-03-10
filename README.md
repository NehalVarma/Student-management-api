# Student Management API

Basic Django REST API I built to learn backend stuff.

## What it does
- CRUD operations for students
- JSON API endpoints 
- Uses PostgreSQL

## Stack
- Django
- PostgreSQL
- DRF

## Setup
```bash
sudo apt install python3 postgresql
sudo service postgresql start
sudo -u postgres createdb student_management_db

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

## Endpoints
- GET `/api/students/` - list students
- POST `/api/students/` - add student
- GET `/api/students/1/` - get student
- PUT `/api/students/1/` - update student  
- DELETE `/api/students/1/` - delete student
- GET `/api/students/search/?q=term` - search students

**Search options:**
- `/api/students/?search=name` - filter by name
- `/api/students/?course=course` - filter by course  
- `/api/students/?age=22` - filter by age

Test with Postman or curl.

**Note:** Change DB password in settings.py

