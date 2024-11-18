from flask import Flask
from .extensions import db, bcrypt
from .models import User, Recipe, Comment, Rating

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app