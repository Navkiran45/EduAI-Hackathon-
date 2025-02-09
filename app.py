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

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.base import base
    from routes.quiz import quiz_bp
    from routes.chapters import chapters_bp
    from routes.code import code_bp
    from routes.chatbot import chatbot_bp
    from routes.level import level_bp
    
    app.register_blueprint(level_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(base)
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(chapters_bp, url_prefix='/chapters')
    app.register_blueprint(code_bp, url_prefix='/code')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

    # Import models for create_all()
    from models.student import Student
    from models.chapter import Chapter, ChapterObjective

    # Create database tables
    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return Student.query.get(int(user_id))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)