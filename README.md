# 📚 Library Management System

A Library Management System backend built with Django REST Framework.

## Features

- JWT Authentication
- Role-Based Access (Admin, Librarian, Student)
- Category Management
- Author Management
- Book Management
- Book Copies
- Borrow & Return
- Fine Calculation
- Visitor Management
- Dashboard
- Search & Pagination
- Swagger API Documentation

## Tech Stack

- Python
- Django
- Django REST Framework
- MySQL
- JWT
- drf-spectacular

## Installation

```bash
git clone <repository-url>

cd LibraryManagement

python -m venv env

env\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

Swagger:

```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

## Run Tests

```bash
python manage.py test
```
