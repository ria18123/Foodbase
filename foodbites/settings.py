# Import the os module for interacting with the operating system
import os
# Import Path class from pathlib for handling filesystem paths
from pathlib import Path

# Define the base directory of the project, which is two levels up from the current file
BASE_DIR = Path(__file__).resolve().parent.parent

# Security and Debug settings
# Get the secret key from environment variables, with a default for development
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-secret-key')  # Use environment variable for production
# Set debug mode to True for development; remember to set to False in production
DEBUG = True  # Remember to set DEBUG=False in production
# Define allowed hosts for the application, including localhost and Ngrok URL
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '8ba9-2400-1a00-b080-98fa-e40b-636-80e4-f33a.ngrok-free.app']  # Include the Ngrok URL here
# Set the site ID for the Django sites framework
SITE_ID = 1  # Ensure this ID matches your Site entry in the database

# Application definition
# List of installed applications for the Django project
INSTALLED_APPS = [
    # Wagtail-specific apps for content management
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',

    # Third-party apps for additional functionality
    'modelcluster',
    'taggit',
    'channels',
    'social_django',

    # Custom apps developed for this project
    'recipes',

    # Django core apps for basic functionality
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware configuration
# List of middleware components to process requests and responses
MIDDLEWARE = [
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',  # Middleware for handling redirects in Wagtail
    'django.middleware.security.SecurityMiddleware',  # Middleware for security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Middleware for session management
    'django.middleware.common.CommonMiddleware',  # Middleware for common functionalities
    'django.middleware.csrf.CsrfViewMiddleware',  # Middleware for CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Middleware for user authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Middleware for handling messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Middleware to prevent clickjacking
    'social_django.middleware.SocialAuthExceptionMiddleware',  # Middleware for handling social authentication exceptions
]

# URL configuration
# Specify the root URL configuration for the project
ROOT_URLCONF = 'foodbites.urls'

# Templates configuration
# Define the settings for template rendering
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Use Django's template engine
        'DIRS': [BASE_DIR / 'templates'],  # Specify directories to look for templates
        'APP_DIRS': True,  # Enable searching for templates in app directories
        'OPTIONS': {
            'context_processors': [  # List of context processors to include
                'django.template.context_processors.debug',  # Debug context processor
                'django.template.context_processors.request',  # Request context processor
                'django.contrib.auth.context_processors.auth',  # Authentication context processor
                'django.contrib.messages.context_processors.messages',  # Messages context processor
                'social_django.context_processors.backends',  # Social auth backends context processor
                'social_django.context_processors.login_redirect',  # Social auth login redirect context processor
                'django.contrib.messages.context_processors.messages',  # Messages context processor (duplicate)
            ],
        },
    },
]

# WSGI and ASGI configurations
# Specify the WSGI application for the project
WSGI_APPLICATION = 'foodbites.wsgi.application'
# Specify the ASGI application for the project
ASGI_APPLICATION = 'foodbites.asgi.application'

# Channels configuration (using Redis for ASGI)
# Define the channel layers for handling WebSockets and other asynchronous tasks
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',  # Use Redis as the channel layer backend
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],  # Ensure Redis is running on this host and port
        },
    },
}

# Database configuration
# Define the database settings for the project
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite as the database engine
        'NAME': BASE_DIR / 'db.sqlite3',  # Specify the database file location
    }
}

# Password validation settings
# List of password validators to enforce password strength
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Validate similarity to user attributes
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Enforce minimum password length
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Prevent common passwords
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Prevent numeric-only passwords
    },
]

# Localization settings
# Define localization settings for the project
LANGUAGE_CODE = 'en-us'  # Set the default language code
TIME_ZONE = 'UTC'  # Set the default time zone
USE_I18N = True  # Enable internationalization
USE_L10N = True  # Enable localization
USE_TZ = True  # Enable timezone support

# Static and media files settings
# Define URLs and paths for serving static and media files
STATIC_URL = '/static/'  # URL prefix for static files
MEDIA_URL = '/media/'  # URL prefix for media files
MEDIA_ROOT = BASE_DIR / 'media'  # Directory to store uploaded media files
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory to collect static files for deployment
STATICFILES_DIRS = [BASE_DIR / 'static']  # Additional directories to search for static files

# Default primary key field type
# Set the default type for primary key fields in models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Use BigAutoField for primary keys

# Authentication and login settings
# Define URLs for login and redirection after login/logout
LOGIN_REDIRECT_URL = 'recipes:user_dashboard'  # Redirect to user dashboard after login
LOGOUT_REDIRECT_URL = '/'  # Redirect to home page after logout
LOGIN_URL = 'login'  # URL for the login page

# Wagtail-specific settings
# Define settings specific to Wagtail CMS
WAGTAIL_SITE_NAME = 'foodbase'  # Set the name of the Wagtail site
WAGTAILADMIN_BASE_URL = 'http://127.0.0.1:8000/cms/'  # Base URL for Wagtail admin
WAGTAILDOCS_EXTENSIONS = ['csv', 'docx', 'key', 'odt', 'pdf', 'pptx', 'rtf', 'txt', 'xlsx', 'zip']  # Allowed document extensions for Wagtail

# Email backend configuration
# Define settings for sending emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Use SMTP backend for sending emails
EMAIL_HOST = 'smtp.gmail.com'  # SMTP server for Gmail
EMAIL_PORT = 587  # Port for SMTP
EMAIL_USE_TLS = True  # Use TLS for secure email sending
EMAIL_HOST_USER = 'shrestharia08@gmail.com'  # Email address for sending emails
EMAIL_HOST_PASSWORD = 'ria016631358'  # App-specific password for Gmail (should be kept secret)

# Social authentication configuration for Google
# Define authentication backends for social authentication
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',  # Google OAuth2 backend
    'django.contrib.auth.backends.ModelBackend',  # Default Django authentication backend
)

# Google OAuth2 credentials
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '495014393638-upba52j508aast3t1v8hdmlsneegk6g.apps.googleusercontent.com'  # Google OAuth2 client ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'  # Google OAuth2 client secret

# Ensure the SOCIAL_AUTH_URL_NAMESPACE is correct
SOCIAL_AUTH_URL_NAMESPACE = 'social'  # Namespace for social authentication URLs

# Ngrok Redirect URI for Google OAuth2
# Ensure this URI is listed in the Google Console for OAuth2
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'https://8ba9-2400-1a00-b080-98fa-e40b-636-80e4-f33a.ngrok-free.app/complete/google/'  # Redirect URI for Ngrok

# Security settings for cookies and redirects
# Set secure cookie settings based on DEBUG mode
CSRF_COOKIE_SECURE = not DEBUG  # Use secure cookies for CSRF protection in production
SESSION_COOKIE_SECURE = not DEBUG  # Use secure cookies for sessions in production
SECURE_SSL_REDIRECT = not DEBUG  # Redirect all HTTP traffic to HTTPS in production