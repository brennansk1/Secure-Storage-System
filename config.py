# config.py

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
basedir = Path(__file__).resolve().parent
load_dotenv(basedir / '.env')

class Config:
    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    DEBUG = False
    TESTING = False

    # Database Config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + str(basedir / 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configurations
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@demo.com')

    # Flask-Limiter configuration with Redis
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', "redis://localhost:6379/0")

    # File upload configurations
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(basedir, 'uploads'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit

    # Security configurations
    SESSION_COOKIE_SECURE = True  # Ensure cookies are sent over HTTPS
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
