from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired
from flask import flash

class SignUpForm(FlaskForm):
    name = StringField('Your First Name', validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_passwords(self):
        if self.confirm_password.data != self.password.data:
            flash('Passwords do not match')
            return False
        return True

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')