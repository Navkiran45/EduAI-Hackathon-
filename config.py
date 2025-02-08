import os

class Config:
    SECRET_KEY = os.urandom(32)
    os.environ['SQLALCHEMY_DATABASE_URI']
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}