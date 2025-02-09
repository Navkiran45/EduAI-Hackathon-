import os
from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    
    # Use a fixed secret key for development
    SECRET_KEY = 'dev-secret-key-123'  # Only use this for development!
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)  # Session lasts for 31 days
    SESSION_PERMANENT = True  # Make sessions permanent
    SESSION_TYPE = 'filesystem'  # Store sessions in filesystem