# create_admin.py

import os
from flask import Flask
from extensions import db
from app_models import User, File, ActivityLog  # Updated import
from config import Config
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Import models
    from app_models import User, File, ActivityLog

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    return app

def create_admin():
    app = create_app()
    with app.app_context():
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        admin_login_token = os.environ.get('ADMIN_LOGIN_TOKEN')

        if not admin_password or not admin_login_token:
            raise ValueError("Please set the ADMIN_PASSWORD and ADMIN_LOGIN_TOKEN environment variables.")

        existing_admin = User.query.filter_by(email=admin_email).first()
        if existing_admin:
            print("Admin user already exists.")
        else:
            admin_user = User(
                username=admin_username,
                email=admin_email,
                is_admin=True
            )
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully.")

if __name__ == '__main__':
    create_admin()
