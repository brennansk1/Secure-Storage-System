# routes/main_routes.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from forms import DeleteFileForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    delete_form = DeleteFileForm()
    return render_template('dashboard.html', user=current_user, delete_form=delete_form)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
