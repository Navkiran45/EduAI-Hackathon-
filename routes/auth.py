from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from models.student import Student
from app import db, login_manager

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        contact_number = request.form.get('contact_number')
        password = request.form.get('password')

        if Student.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        if Student.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))

        student = Student(
            name=name,
            username=username,
            email=email,
            contact_number=contact_number
        )
        student.set_password(password)

        db.session.add(student)
        db.session.commit()

        flash('Registration successful!')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        student = Student.query.filter_by(username=username).first()
        if student and student.check_password(password):
            login_user(student)
            return render_template('index.html')
        
        flash('Invalid username or password')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))