from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.student import Student
from app import db, login_manager
from werkzeug.security import generate_password_hash


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('base.home'))

    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        contact_number = request.form.get('contact_number')
        password = request.form.get('password')

        # Validate required fields
        if not all([name, username, email, contact_number, password]):
            flash('All fields are required')
            return redirect(url_for('auth.register'))
        return render_template('homepage.html')

        # Validate password strength
        if len(password) < 6:
            flash('Password must be at least 6 characters long')
            return redirect(url_for('auth.register'))

        # Check if username or email already exists
        if Student.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        if Student.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))

        try:
            # Create new student
            student = Student(
                name=name,
                username=username,
                email=email,
                contact_number=contact_number
            )
            student.set_password(password)

            # Save to database
            db.session.add(student)
            db.session.commit()

            # Log in the new user
            login_user(student)
            flash('Registration successful! Welcome to EduAI!')
            return redirect(url_for('base.home'))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.')
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password')
            return redirect(url_for('auth.login'))

        student = Student.query.filter_by(username=username).first()
        
        if student and student.check_password(password):
            login_user(student)
            flash('Welcome back!')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('base.home'))
        
        flash('Invalid username or password')
        return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully')
    return redirect(url_for('auth.register'))