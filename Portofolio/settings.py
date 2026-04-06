"""
Django settings for Portofolio project.

Configuration professionnelle avec chargement automatique des variables d'environnement.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CHARGEMENT DES VARIABLES D'ENVIRONNEMENT
# ==============================================================================
# Charge le fichier .env depuis le répertoire du projet
env_path = BASE_DIR / '.env'
load_dotenv(env_path)

# ==============================================================================
# CONFIGURATION DE BASE
# ==============================================================================

# SECRET_KEY - Obligatoire, chargée depuis .env
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# DEBUG - False en production par défaut
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes', 'on')

# ALLOWED_HOSTS - Liste des hôtes autorisés
# Hôtes par défaut (toujours inclus)
DEFAULT_ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']
allowed_hosts_str = os.getenv('DJANGO_ALLOWED_HOSTS', '')
if allowed_hosts_str:
    # Fusionner les hôtes par défaut avec ceux de l'environnement
    ALLOWED_HOSTS = DEFAULT_ALLOWED_HOSTS + [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]
else:
    ALLOWED_HOSTS = DEFAULT_ALLOWED_HOSTS

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise pour les fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Portofolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'Portofolio.wsgi.application'

# ==============================================================================
# BASE DE DONNÉES
# ==============================================================================
# SQLite par défaut, PostgreSQL si DATABASE_URL est configuré (Render)

DATABASE_URL = os.getenv('DATABASE_URL', '')

if DATABASE_URL:
    # Configuration PostgreSQL via DATABASE_URL (Render)
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
else:
    # SQLite pour le développement
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==============================================================================
# VALIDATION DE MOTS DE PASSE
# ==============================================================================

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

# ==============================================================================
# CONFIGURATION INTERNATIONALE
# ==============================================================================

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Conakry'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# FICHIERS STATIQUES
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'home' / 'static',
    BASE_DIR / 'home' / 'asset',
]

# Configuration WhiteNoise pour la production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================================================================
# CONFIGURATION EMAIL (SMTP GMAIL)
# ==============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER', '')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'castrohounmenou@gmail.com')
EMAIL_TIMEOUT = 30
EMAIL_USE_LOCALTIME = True

# Forcer le hostname pour éviter l'erreur HELO 501 (Google)
import socket
try:
    socket.gethostname = lambda: 'localhost'
except:
    pass

# ==============================================================================
# API GEMINI (ASSISTANT AI)
# ==============================================================================

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_API_URL = os.getenv('GEMINI_API_URL', 'https://generativelanguage.googleapis.com/v1beta/models')
GEMINI_API_MODEL = os.getenv('GEMINI_API_MODEL', 'gemini-2.5-flash')

# ==============================================================================
# CONFIGURATION GITHUB
# ==============================================================================

GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'castro2026')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')

# ==============================================================================
# SÉCURITÉ (PRODUCTION)
# ==============================================================================

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = []
csrf_origins_str = os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', '')
if csrf_origins_str:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins_str.split(',') if origin.strip()]

# Paramètres de sécurité optionnels pour la production
if not DEBUG:
    # HTTPS
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() in ('true', '1', 'yes', 'on')
    
    # Cookies sécurisés
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1', 'yes', 'on')
    CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False').lower() in ('true', '1', 'yes', 'on')
    
    # Autres paramètres de sécurité
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ==============================================================================
# LOGGING
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'home': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ==============================================================================
# AUTHENTICATION REDIRECTS
# ==============================================================================

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home_portfolio'

# ==============================================================================
# DEFAULT AUTO FIELD
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
