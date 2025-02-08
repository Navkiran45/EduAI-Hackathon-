from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from models.student import Student
from app import db, login_manager
from flask_login import current_user

update_bp = Blueprint('update', __name__)

@update_bp.route('/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        contact_number = request.form.get('contact_number')
        password = request.form.get('password')

        # Validate required fields
        if not all([name, username, email]):
            flash('Name, username, and email are required fields')
            return redirect(url_for('auth.update_profile'))

        # Check for existing username/email, excluding current user
        if Student.query.filter(Student.username == username, Student.id != current_user.id).first():
            flash('Username already exists')
            return redirect(url_for('auth.update_profile'))

        if Student.query.filter(Student.email == email, Student.id != current_user.id).first():
            flash('Email already registered')
            return redirect(url_for('auth.update_profile'))

        try:
            # Update user information
            current_user.name = name
            current_user.username = username
            current_user.email = email
            current_user.contact_number = contact_number
            
            if password:
                current_user.set_password(password)

            db.session.commit()
            flash('Profile updated successfully!')
            return redirect(url_for('auth.update_profile'))  # Stay on the same page after update
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile')
            return redirect(url_for('auth.update_profile'))

    # GET request: display the form with current user data
    return render_template('update.html')
