from flask import Flask
from .extensions import db, bcrypt
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'

    db.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
