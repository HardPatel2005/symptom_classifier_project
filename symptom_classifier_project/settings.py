import os
from pathlib import Path
import dotenv
import dj_database_url # <--- Make sure you have this installed: pip install dj-database-url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
# This is mainly for local development. On Render, environment variables are set directly.
dotenv.load_dotenv(dotenv_path=BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "insecure-default-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Accept the domain from Render or localhost in dev
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'classifier_app',
    # Add WhiteNoise to INSTALLED_APPS for proper static file handling if not already there
    'whitenoise.runserver_nostatic', # Only if you want WhiteNoise to handle static files in development as well. Remove if causing issues.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # for static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'symptom_classifier_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'symptom_classifier_project.wsgi.application'

# Database
# This section is CHANGED to use DATABASE_URL from environment variables
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600 # Optional: maintain persistent connections
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # This is where 'collectstatic' will put files

# WhiteNoise configuration
# Ensure WhiteNoise is properly configured for production
# This should be above django.contrib.staticfiles in your INSTALLED_APPS if using runserver_nostatic
# Ensure STATIC_ROOT is set correctly for collectstatic to work.

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Custom Settings for your application ---
# Assuming you have a GOOGLE_API_KEY for your Gemini integration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# You might want to add logging configuration for production errors
# LOGGING = { ... }