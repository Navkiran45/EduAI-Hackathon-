from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.static_folder = 'static'

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    from models.student import Student
    db.init_app(app)
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_student(id):
        return Student.query.get(int(id))

    login_manager.login_view = 'auth.login'

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)