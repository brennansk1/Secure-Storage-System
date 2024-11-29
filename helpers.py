# utils/helpers.py

import os
from werkzeug.utils import secure_filename
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Define allowed extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """
    Check if the file has an allowed extension.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_file_path(filename, user_id, upload_folder):
    """
    Generate a secure file path for the uploaded file.
    """
    filename = secure_filename(filename)
    user_folder = os.path.join(upload_folder, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    return os.path.join(user_folder, filename)
