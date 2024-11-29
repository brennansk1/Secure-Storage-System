# models/file.py

from extensions import db
from datetime import datetime
import os

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<File {self.filename}>"

    @property
    def relative_path(self):
        upload_folder = db.app.config['UPLOAD_FOLDER']
        return os.path.relpath(self.filepath, upload_folder)
