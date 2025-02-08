import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///C:/Users/jaide/EduAI-Hackathon-/instance/database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}