# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app_models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=150, message="Username must be between 3 and 150 characters.")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=8, message="Password must be at least 8 characters long.")
    ])
    password2 = PasswordField(
        'Repeat Password', validators=[
            DataRequired(message="Please repeat your password."),
            EqualTo('password', message="Passwords must match.")
        ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required.")
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UploadFileForm(FlaskForm):
    file = FileField('Select File', validators=[
        DataRequired(message="Please select a file to upload.")
    ])
    submit = SubmitField('Upload')

    def validate_file(self, field):
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
        if not ('.' in field.data.filename and field.data.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            raise ValidationError('Unsupported file extension.')

class DeleteFileForm(FlaskForm):
    submit = SubmitField('Delete')

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')
