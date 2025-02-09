from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

base = Blueprint('base', __name__)

@base.route('/')
def home():
    # If user is not logged in, show the landing/auth page
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    # If user is logged in, show the homepage with language selection
    return render_template('home.html')

@base.route('/level/<language>')
@login_required
def level(language):
    # Validate language
    valid_languages = ['python', 'javascript', 'java', 'cpp']
    if language.lower() not in valid_languages:
        flash('Invalid programming language selected')
        return redirect(url_for('base.home'))
    
    return render_template('level.html', language=language) 