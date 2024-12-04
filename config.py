import os

class Config:
    SECRET_KEY = os.getenv('ebb315f2347540c21ebf52e538815580')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///recipe.db'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads' 
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True