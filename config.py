import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))  # Use .env SECRET_KEY if available
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///recipe.db')  # Use DATABASE_URL from .env if available
    SQLALCHEMY_TRACK_MODIFICATIONS = False