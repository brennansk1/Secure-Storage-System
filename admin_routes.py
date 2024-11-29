# routes/admin_routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from extensions import db
from app_models import User, File, ActivityLog
from forms import DeleteForm
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        abort(403)  # Forbidden access for non-admin users
    delete_form = DeleteForm()
    users = User.query.all()
    files = File.query.all()
    activity_logs = ActivityLog.query.all()
    return render_template('admin_dashboard.html', users=users, files=files, activity_logs=activity_logs, delete_form=delete_form)

# Route to delete a user
@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden access for non-admin users
    user = User.query.get_or_404(user_id)
    form = DeleteForm()
    if form.validate_on_submit():
        try:
            # Delete user's files
            for file in user.files:
                if os.path.exists(file.filepath):
                    os.remove(file.filepath)
                db.session.delete(file)
            # Delete user's activity logs
            for log in user.activity_logs:
                db.session.delete(log)
            # Delete the user
            db.session.delete(user)
            db.session.commit()
            flash('User and associated data have been deleted.', 'success')
        except Exception:
            db.session.rollback()
            flash('An error occurred while deleting the user.', 'danger')
    else:
        flash('Invalid delete request.', 'danger')
    return redirect(url_for('admin.dashboard'))
