import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///C:/Users/Navkiran Kaur/OneDrive/Desktop/EduAI/instance/database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}