# utils/email_utils.py

import os
import logging
from mailjet_rest import Client

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def send_email(to_email, subject, html_content):
    api_key = os.environ.get('MAILJET_API_KEY')
    api_secret = os.environ.get('MAILJET_SECRET_KEY')
    default_sender = os.environ.get('MAIL_DEFAULT_SENDER')

    if not api_key or not api_secret:
        logger.error("Mailjet API credentials are not set.")
        return False

    if not default_sender:
        logger.error("MAIL_DEFAULT_SENDER is not set.")
        return False

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    data = {
        'Messages': [
            {
                "From": {
                    "Email": default_sender,
                    "Name": "Secure Storage App"
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": to_email.split('@')[0]  # Extract name from email
                    }
                ],
                "Subject": subject,
                "HTMLPart": html_content
            }
        ]
    }

    try:
        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            logger.info(f"Email sent to {to_email}.")
            return True
        else:
            logger.error(f"Failed to send email to {to_email}. Status Code: {result.status_code}")
            logger.error(f"Error: {result.json()}")
            return False
    except Exception as e:
        logger.exception(f"An error occurred while sending email to {to_email}: {e}")
        return False
