from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os


db = SQLAlchemy()
login_manager = LoginManager()


app = Flask(__name__)
app.config.from_object(Config)

app.static_folder = "static"

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Initialize extensions with the app
db.init_app(app)
login_manager.init_app(app)

# Import models after db initialization
from models.student import Student


@login_manager.user_loader
def load_student(id):
    return Student.query.get(int(id))


login_manager.login_view = "auth.login"

# Register blueprints
from routes.auth import auth_bp

app.register_blueprint(auth_bp)

# Create tables within app context
with app.app_context():
    db.create_all()