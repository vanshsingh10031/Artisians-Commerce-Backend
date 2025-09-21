from .settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update secret key to use environment variable
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# Allow Railway's domain and your frontend domain
ALLOWED_HOSTS = [
    '.railway.app',  # Allow all railway.app subdomains
    'localhost',
    '127.0.0.1',
    '*',  # Temporarily allow all hosts - make sure to update this with your specific domains
]

# Configure static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Configure CORS
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.vercel.app",  # Replace with your Vercel frontend domain
]
CORS_ALLOW_ALL_ORIGINS = True  # Only for development, set to False in production

# Add whitenoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Database configuration - using environment variables
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.environ.get('DB_NAME', 'ArtisanEcommerce_New'),
        'USER': os.environ.get('DB_USER', 'Dev3v'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'gqJyJXW47CcH788'),
        'HOST': os.environ.get('DB_HOST', '103.180.120.47'),
        'PORT': os.environ.get('DB_PORT', ''),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True