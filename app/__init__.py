import os
from flask import Flask, render_template
from .extensions import db, bcrypt, login_manager
from .routes import main
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'ebb315f2347540c21ebf52e538815580'
    app.config['uploads'] = os.path.join(os.getcwd(), 'app', 'static', 'uploads')

    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)
    bcrypt.init_app(app)

    
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    
    app.register_blueprint(main)

    with app.app_context():
        from . import models
        db.create_all()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app