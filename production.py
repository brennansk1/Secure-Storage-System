# config/production.py

from . import Config

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Ensure cookies are only sent over HTTPS
