from flask import Flask, render_template, redirect, url_for,flash, request
from flask import Blueprint, jsonify, request
from database import db
from modules.models import User, Examquestion, Testsession, Userprogress, Testanswer, Testscore, Userprogress
from flask_login import current_user, logout_user, login_required, login_user, LoginManager
from modules.forms import LoginForm, SignUpForm
from flask import flash


# Initialize Blueprint for routes
bp = Blueprint('routes', __name__)

# Initialize Login Manager
login_manager = LoginManager()

# Load user
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

@bp.route('/', methods=['GET'])
def index():
    return "Hello, World!"

# Health check route
@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

# Register route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = SignUpForm()
    if form.validate_on_submit() and form.validate_passwords():
        name = form.name.data
        email = form.email.data
        # check if this email is already registered:
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return False
        password = form.password.data
        # ADD NEW USER TO THE DATABASE
        new_user = User(email=email, name=name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'You have successfully registered.')
        return "You registered successfully", 200
    return render_template("register.html", form=form)

# Login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if not User.query.filter_by(email=email).first():
            flash('This email address is not registered. Please sign-up')
            return redirect(url_for('routes.login'))
        user = User.query.filter_by(email=email).first()
        if user.check_password_hash(password):
            login_user(user)
            flash(f'You have successfully logged in.')
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))
    return render_template(template_name_or_list="login.html", form=form)