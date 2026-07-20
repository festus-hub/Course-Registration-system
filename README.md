# CourseHub — Course Registration System

A Django-based course registration platform with separate self-service and admin experiences, a Tailwind-styled UI, a themed Django admin (django-unfold), and a REST API with interactive Swagger/Redoc documentation.

## Features

**Student self-service**
- Dashboard with registration summary and credit hours
- Browse available courses and register (with duplicate-registration prevention)
- View own registered courses and their approval status
- Profile management

**Admin / Staff**
- Manage departments, courses, students, and registrations (custom Tailwind CRUD pages under `/*/manage/`)
- Approve, reject, edit, or delete any registration
- Download a registration as a PDF
- Full Django admin at `/admin/`, themed with [django-unfold](https://github.com/unfoldadmin/django-unfold)

**API**
- REST API for all core models (Departments, Courses, Students, Registrations)
- Token-based authentication, with separate register/login/logout endpoints
- Interactive API docs via Swagger UI and Redoc (`drf-spectacular`)

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Frontend:** Django templates + Tailwind CSS (CDN), Bootstrap Icons
- **Admin theme:** django-unfold
- **API docs:** drf-spectacular (OpenAPI 3 / Swagger / Redoc)
- **PDF generation:** ReportLab
- **Auth:** Django's built-in auth system with a custom `CustomUser` model, token auth for the API

## Project Structure

```
config/                 # Project settings and root urls.py
accounts/               # CustomUser model, auth (register/login/logout), password reset
dashboard/              # Announcements
departments/            # Department model + CRUD
courses/                # Course model, self-service browsing, admin CRUD
students/               # Student model, self-service dashboard, admin management
registrations/          # CourseRegistration model, admin approval workflow
core/                   # Shared API routing and permission classes
```

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <your-repo-url>
cd "Course registration system"
python -m venv venv
```

Activate it:
```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, generate one from your current environment:
```bash
pip freeze > requirements.txt
```

It should include at least:
```
Django
djangorestframework
djangorestframework-authtoken
drf-spectacular
django-unfold
reportlab
```

### 3. Environment variables

Create a `.env` file in the project root (or set these however your `settings.py` reads them):

```
SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

The email settings are required for the password reset flow (`accounts/views.py` sends reset links via `send_mail`).

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create an admin/staff account

Public signup always creates a **student** account — admin accounts are created only through Django admin, for security. Create your first one with:

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

## Key URLs

| URL | Purpose |
|---|---|
| `/` | Landing page |
| `/register/`, `/login/` | Student signup / login (template-based) |
| `/students/` | Student dashboard (self-service) |
| `/students/manage/` | Student management (staff only) |
| `/courses/` | Browse courses (self-service) |
| `/courses/manage/` | Course management (staff only) |
| `/departments/` | Department management (staff only) |
| `/registrations/` | Registration management (staff only) |
| `/admin/` | Django admin (Unfold theme) |
| `/api/` | REST API root |
| `/api/auth/register/`, `/api/auth/login/` | API authentication |
| `/api/schema/swagger-ui/` | Interactive API docs |
| `/api/schema/redoc/` | Alternative API docs (Redoc) |

## Roles & Permissions

- **Student** (`is_staff=False`): can only access their own dashboard, courses, and registrations.
- **Admin/Staff** (`is_staff=True`): full access to management pages and the Django admin. Staff accounts can only be created via Django admin — there is no self-service path to becoming staff.

## Running Tests

```bash
python manage.py test
```

## License

Add your license here.
