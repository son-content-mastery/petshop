# Django Petshop Project Setup and Recovery Guide

This guide provides detailed step-by-step instructions for setting up and running the Django petshop project from scratch.

## Prerequisites

- Python 3.8 or higher installed on your system
- Git (for cloning the repository)
- Windows PowerShell or Command Prompt

## Step 1: Clone or Navigate to the Project Directory

If you haven't cloned the repository yet:

```bash
git clone https://github.com/son-content-mastery/petshop.git
cd petshop
```

If you already have the project:

```powershell
cd C:\Users\[YourUsername]\OneDrive\Documents\GitHub\uncle-engineer_petshop
```

## Step 2: Create a Virtual Environment

Create an isolated Python environment for the project:

```powershell
python -m venv .venv
```

This creates a `.venv` folder in your project directory.

## Step 3: Activate the Virtual Environment

Activate the virtual environment to isolate project dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` at the beginning of your command prompt after activation.

**Note:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

## Step 4: Install Project Dependencies

Install all required Python packages:

```powershell
pip install -r requirements.txt
```

If dependency build errors occur on Windows, use these exact commands to install known working packages:

```powershell
python -m pip install django-summernote
python -m pip install Pillow
python -m pip install psycopg2-binary
```

This installs Django, PostgreSQL driver, and other dependencies listed in `requirements.txt`.

## Step 5: Configure Environment Variables

Create a `.env` file in the project root with the following content:

```env
SECRET_KEY=django-insecure-development-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DB_NAME=petshop
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

**Important:** The `.env` file contains sensitive information. Never commit it to version control.

## Step 6: Run Database Migrations

Apply database migrations to set up the database schema:

```powershell
python manage.py migrate
```

You should see output like:
```
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, django_summernote, products, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  ...
```

## Step 7: Start the Development Server

Launch the Django development server:

```powershell
python manage.py runserver
```

The server will start on `http://127.0.0.1:8000/` by default.

## Step 8: Access the Application

Open your web browser and navigate to:
- **Home Page:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## Troubleshooting

### Common Issues and Solutions

#### 1. "ModuleNotFoundError: No module named 'django'"
- **Cause:** Django not installed or virtual environment not activated
- **Solution:** Ensure virtual environment is activated and run `pip install -r requirements.txt`

#### 2. "ImproperlyConfigured: Set the SECRET_KEY environment variable"
- **Cause:** Missing `.env` file
- **Solution:** Create the `.env` file as described in Step 5

#### 3. "ModuleNotFoundError: No module named 'psycopg2'"
- **Cause:** PostgreSQL driver not installed or not built because `pg_config` is missing (common on Windows)
- **Solution:** Install binary package with `python -m pip install psycopg2-binary` and retry.

#### 4. "Cannot use ImageField because Pillow is not installed"
- **Cause:** Pillow dependency missing
- **Solution:** `python -m pip install Pillow`

#### 5. Database connection errors
- **Cause:** PostgreSQL not running or misconfigured
- **Solution:** The project is configured to use SQLite for development in `mysite/settings/dev.py`

#### 5. Port 8000 already in use
- **Cause:** Another process using port 8000
- **Solution:** Use a different port: `python manage.py runserver 8001`

### Checking Python Environment

To verify your setup:

```powershell
# Check Python version
python --version

# Check if Django is installed
python -c "import django; print(django.__version__)"

# Check if virtual environment is active
which python  # Should point to .venv\Scripts\python.exe
```

### VS Code Configuration

For VS Code users:

1. Open the project folder in VS Code
2. Open Command Palette (Ctrl+Shift+P)
3. Select "Python: Select Interpreter"
4. Choose the interpreter from `.venv\Scripts\python.exe`

## Project Structure

```
petshop/
├── blog/                 # Blog app
├── products/             # Products app
├── mysite/               # Main project settings
│   └── settings/
│       ├── base.py       # Base settings
│       ├── dev.py        # Development settings
│       └── prod.py       # Production settings
├── .env                  # Environment variables (create this)
├── .venv/                # Virtual environment (created by venv)
├── requirements.txt      # Python dependencies
├── manage.py             # Django management script
├── Dockerfile            # Docker configuration
└── docker-compose.yml    # Docker Compose configuration
```

## Additional Commands

### Create Superuser

To access the Django admin:

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### Load Sample Data

If sample data fixtures exist:

```powershell
python manage.py loaddata blog/fixtures/blog_data.json
python manage.py loaddata products/fixtures/products_data.json
```

### Run Tests

```powershell
python manage.py test
```

### Collect Static Files (for production)

```powershell
python manage.py collectstatic
```

## Production Deployment

For production deployment, use the provided Docker configuration:

```powershell
docker-compose -f docker-compose.prod.yml up -d
```

This uses Gunicorn and Nginx for production-ready deployment.

## Support

If you encounter issues not covered in this guide, check:
- Django documentation: https://docs.djangoproject.com/
- Project README.md (if available)
- GitHub issues for this repository