
# DIGITHAI Notes Management Application

## Overview

The Notes Management Application is a Django web application that allows users to create, view, edit, and delete personal notes. The application enforces user authentication to ensure that users can only manage their own notes. Additionally, it provides a RESTful API for integration with frontend applications.

## Features

- User authentication (registration and login)
- Create, read, update, and delete (CRUD) functionality for notes
- Filtering of notes by title or creation date
- RESTful API for note management
- User-friendly interface using Bootstrap

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: SQLite (or PostgreSQL/MySQL depending on your configuration)
- **Frontend**: Bootstrap
- **Testing**: Django's test framework and DRF's test utilities

## Installation Guide

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/notes_management.git
   cd notes_management
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**: Open your browser and go to `http://127.0.0.1:8000/`.

## Usage

- **Authentication**: Users can register and log in to access the notes functionality.
- **Creating Notes**: Users can create new notes using the provided form on the home page.
- **Viewing Notes**: All notes created by the logged-in user will be displayed on the home page.
- **Editing Notes**: Users can click on the edit button to update the title and content of their notes.
- **Deleting Notes**: Users can delete their notes using the delete button.

## API Documentation

The application exposes a RESTful API for managing notes. Below are the details of the API endpoints.

### Base URL

```
http://127.0.0.1:8000/api/
```

### Endpoints

1. **List All Notes**
   - **URL**: `/notes/`
   - **Method**: `GET`
   - **Authentication**: Required

2. **Create a Note**
   - **URL**: `/notes/`
   - **Method**: `POST`
   - **Authentication**: Required
   - **Request Body**:
     ```json
     {
       "title": "Note Title",
       "content": "Note content."
     }
     ```

3. **Retrieve a Note**
   - **URL**: `/notes/<id>/`
   - **Method**: `GET`
   - **Authentication**: Required

4. **Update a Note**
   - **URL**: `/notes/<id>/`
   - **Method**: `PUT` or `PATCH`
   - **Authentication**: Required
   - **Request Body**:
     ```json
     {
       "title": "Updated Note Title",
       "content": "Updated content."
     }
     ```

5. **Delete a Note**
   - **URL**: `/notes/<id>/`
   - **Method**: `DELETE`
   - **Authentication**: Required

## Testing

Run the test suite to ensure all functionalities work as expected:

```bash
python manage.py test
```
