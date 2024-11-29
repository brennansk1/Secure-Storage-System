# main.py

import os
import warnings
from flask import Flask
from config import Config
from extensions import db, bcrypt, login_manager, limiter, csrf, mail
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)  # Initialize Flask-Mail if used elsewhere

    # Import models to ensure they are registered with SQLAlchemy before migrations
    from app_models import User, File, ActivityLog

    # Initialize Flask-Migrate after models are imported
    migrate = Migrate(app, db)

    # Import and register blueprints
    from routes.auth_routes import auth_bp
    from routes.main_routes import main_bp
    from routes.file_routes import file_bp
    from routes.admin_routes import admin_bp
    from routes.errors import errors_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(errors_bp)

    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Load user by ID

    # Handle Flask-Limiter storage warning
    if not app.config.get('RATELIMIT_STORAGE_URL'):
        warnings.warn(
            "Using the in-memory storage for tracking rate limits as no storage was explicitly specified. "
            "This is not recommended for production use. See: "
            "https://flask-limiter.readthedocs.io#configuring-a-storage-backend for documentation about configuring the storage backend.",
            UserWarning
        )

    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Create tables if they don't exist (for development only)
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
