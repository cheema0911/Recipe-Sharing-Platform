from datetime import datetime
from uuid import uuid4
from .extensions import db, bcrypt
from flask_login import UserMixin

favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
)

reposts = db.Table('reposts',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    recipes = db.relationship('Recipe', backref='user', lazy=True)
    favorite_recipes = db.relationship('Recipe', secondary=favorites, backref=db.backref('saved_by', lazy='dynamic'))

class Recipe(db.Model):
    __tablename__ = 'recipes'  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    dietary = db.Column(db.String(100))  
    difficulty = db.Column(db.String(50)) 
    image_path = db.Column(db.String(150))
    ratings = db.relationship('Rating', backref='recipe', lazy=True)
    reposts = db.Column(db.Integer, default=0)  

    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    is_predefined = db.Column(db.Boolean, default=False)  
    ratings = db.relationship('Rating', backref='recipe', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('comments', lazy=True))

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)