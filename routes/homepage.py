
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from models.student import Student
from app import db, login_manager

base_bp = Blueprint('base', __name__)
@base_bp.route('/')
def base():
    return render_template('base.html')
@base_bp.route('/homepage')
def home():
    return render_template('homepage.html')