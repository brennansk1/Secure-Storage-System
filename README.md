# Secure-Storage-System
# SecureStorage

SecureStorage is a robust and secure Flask-based web application designed for safe file storage and management. It offers user authentication, file upload/download capabilities, administrative controls, and comprehensive security measures to protect user data and ensure the integrity of the system.

## Table of Contents

- [Features](#features)
- [Security](#security)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

## Features

- **User Authentication:**
  - User registration and login with secure password hashing.
  - Session management with secure cookies.
  
- **File Management:**
  - Upload, download, and delete files.
  - File type validation and size restrictions to prevent malicious uploads.
  
- **Admin Dashboard:**
  - Manage users, files, and view activity logs.
  - Delete users along with their associated files and logs.
  
- **Activity Logging:**
  - Track and log user activities for monitoring and auditing purposes.
  
- **Security Enhancements:**
  - CSRF protection on all forms.
  - Rate limiting to prevent brute-force and DoS attacks.
  - HTTP security headers to mitigate common web vulnerabilities.
  - Input validation and sanitization to prevent injection attacks.
  - Secure error handling and logging practices.

## Security

SecureStorage adheres to industry-standard security best practices to ensure the protection of user data and the application's integrity. Key security features include:

- **Environment Variable Management:** Sensitive information like `SECRET_KEY`, database URIs, and email credentials are stored securely using environment variables.
  
- **Password Security:** User passwords are hashed using `bcrypt` with strong salts, ensuring they are stored securely.
  
- **CSRF Protection:** All forms are protected against Cross-Site Request Forgery attacks using `Flask-WTF`.
  
- **Rate Limiting:** Implemented using `Flask-Limiter` with Redis as a persistent storage backend to prevent brute-force and DoS attacks.
  
- **HTTP Security Headers:** Configured using `Flask-Talisman` to set Content Security Policy (CSP), `X-Frame-Options`, and other essential headers.
  
- **File Handling Security:** Uploaded files are sanitized using `secure_filename`, validated for allowed extensions, and limited in size to prevent malicious uploads.
  
- **Session Security:** Configured secure session cookies with `Secure`, `HttpOnly`, and `SameSite` attributes to reduce session hijacking risks.
  
- **Error Handling:** Custom error pages prevent the exposure of sensitive application details, while secure logging ensures detailed errors are logged internally without leaking information to users.

## Technologies Used

- **Backend:**
  - [Flask](https://flask.palletsprojects.com/) - Web framework.
  - [Flask-Login](https://flask-login.readthedocs.io/) - User session management.
  - [Flask-WTF](https://flask-wtf.readthedocs.io/) - Form handling and CSRF protection.
  - [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/) - Password hashing.
  - [Flask-Limiter](https://flask-limiter.readthedocs.io/) - Rate limiting.
  - [Flask-Talisman](https://github.com/GoogleCloudPlatform/flask-talisman) - Security headers.
  - [Flask-Mail](https://pythonhosted.org/Flask-Mail/) - Email handling.
  - [Flask-Migrate](https://flask-migrate.readthedocs.io/) - Database migrations.
  
- **Database:**
  - [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for database interactions.
  - [SQLite](https://www.sqlite.org/index.html) - Default database (configurable).

- **Others:**
  - [Redis](https://redis.io/) - In-memory data structure store for rate limiting.
  - [Gunicorn](https://gunicorn.org/) - WSGI HTTP server for UNIX.

## Installation

### Prerequisites

- Python 3.7 or higher
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (optional but recommended)
- [Redis](https://redis.io/) for rate limiting
- Git

### Steps

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/SecureStorage.git
    cd SecureStorage
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Redis:**

    Ensure Redis is installed and running. For installation instructions, visit [Redis Installation](https://redis.io/download).

    ```bash
    # Start Redis server
    redis-server
    ```

## Configuration

### Environment Variables

Create a `.env` file in the project's root directory and populate it with the following variables:

```env
# Secret key for Flask sessions and CSRF protection
SECRET_KEY=your-very-secure-secret-key

# Database configuration
DATABASE_URL=sqlite:///app.db  # Or your preferred database URI


# Flask-Limiter configuration with Redis
RATELIMIT_STORAGE_URL=redis://localhost:6379/0

# File upload configurations
UPLOAD_FOLDER=/path/to/your/upload/folder
MAX_CONTENT_LENGTH=16777216  # 16 MB in bytes
