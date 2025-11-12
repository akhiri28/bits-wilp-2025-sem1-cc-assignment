# forms.py

# Import the base form class and field types
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, DataRequired, Optional, Length, EqualTo
from models import User


# Define a LoginForm class that inherits from FlaskForm
class LoginForm(FlaskForm):
    # Username field with a "required" validator
    username = StringField('Username', validators=[InputRequired()])

    # Password field with a "required" validator
    password = PasswordField('Password', validators=[InputRequired()])

    # Submit button
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')


class BookForm(FlaskForm):
    book_name = StringField('Book Name', validators=[DataRequired()])
    book_type = StringField('Book Type', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    location_in_library = StringField('Location in Library', validators=[Optional()])
    status = SelectField('Status', choices=[('Available', 'Available'), ('Checked Out', 'Checked Out'), ('Checked In', 'Checked In')], validators=[DataRequired()])
    submit_add = SubmitField('Add Book')
    submit_edit = SubmitField('Update Book')

