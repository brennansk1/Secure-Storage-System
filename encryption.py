# utils/encryption.py

from cryptography.fernet import Fernet, InvalidToken
import logging
import os

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Retrieve a master key from environment variables or generate a new one
MASTER_KEY = os.environ.get('MASTER_KEY')  # Ensure this is set in Replit Secrets
if not MASTER_KEY:
    logger.warning("MASTER_KEY not found in environment. Generating a temporary one.")
    MASTER_KEY = Fernet.generate_key().decode()

fernet = Fernet(MASTER_KEY.encode())

def generate_key():
    """
    Generates a new encryption key.
    """
    return Fernet.generate_key()

def encrypt_file(data, key):
    """
    Encrypts the given data using the provided key.
    """
    try:
        f = Fernet(key)
        encrypted_data = f.encrypt(data)
        return encrypted_data
    except Exception as e:
        logger.exception(f"Encryption failed: {e}")
        raise

def decrypt_file(encrypted_data, key):
    """
    Decrypts the given data using the provided key.
    """
    try:
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data
    except InvalidToken:
        logger.error("Invalid encryption key or corrupted data.")
        raise
    except Exception as e:
        logger.exception(f"Decryption failed: {e}")
        raise
