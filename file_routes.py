# routes/file_routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory, abort
from flask_login import login_required, current_user
from extensions import db
from app_models import File
from forms import UploadFileForm, DeleteFileForm
import os
from werkzeug.utils import secure_filename

file_bp = Blueprint('file', __name__, url_prefix='/file')

@file_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadFileForm()
    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        uploaded_file.save(filepath)

        # Create a new File record
        new_file = File(filename=filename, filepath=filepath, user_id=current_user.id)
        db.session.add(new_file)
        db.session.commit()

        flash('File uploaded successfully.', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('upload_file.html', form=form)

@file_bp.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    if file.owner != current_user and not current_user.is_admin:
        abort(403)  # Forbidden access
    directory = os.path.abspath(os.path.dirname(file.filepath))
    return send_from_directory(directory=directory, filename=file.filename, as_attachment=True)

@file_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    form = DeleteFileForm()
    if form.validate_on_submit():
        file = File.query.get_or_404(file_id)
        if file.owner != current_user and not current_user.is_admin:
            abort(403)  # Forbidden
        try:
            if os.path.exists(file.filepath):
                os.remove(file.filepath)
        except OSError:
            flash('Error deleting the file from the server.', 'danger')
            return redirect(url_for('main.dashboard'))
        db.session.delete(file)
        db.session.commit()
        flash('File has been deleted.', 'success')
        return redirect(url_for('main.dashboard'))
    else:
        flash('Invalid delete request.', 'danger')
        return redirect(url_for('main.dashboard'))
