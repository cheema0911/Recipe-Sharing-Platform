from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config
from flask import render_template, redirect, url_for, flash
from models import User, db, Recipe
from forms import RegistrationForm
from flask import request
from flask import redirect, url_for, flash, request
from forms import CommentForm
from flask_login import current_user, login_required
from flask_login import login_required
from flask import jsonify
from functools import wraps
from dotenv import load_dotenv
from forms import RecipeForm
from forms import RatingForm
import os
import sys

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'path_to_static/uploads'  
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  

    db.init_app(app)
    return app

app = create_app()



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/recipes')
def browse_recipes():
    recipes = Recipe.query.all()  
    return render_template('browse_recipes.html', recipes=recipes)

@app.route('/upload_recipe', methods=['GET', 'POST'])
def upload_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            category=form.category.data,
            user_id=current_user.id
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe uploaded!', 'success')
        return redirect(url_for('home'))
    return render_template('upload_recipe.html', form=form)

@app.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
def recipe_details(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You need to log in to post comments.', 'danger')
            return redirect(url_for('login'))
        comment = Comment(content=form.content.data, recipe=recipe, user=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('recipe_details', recipe_id=recipe_id))
    comments = recipe.comments  
    return render_template('recipe.html', recipe=recipe, form=form, comments=comments)

    average_rating = db.session.query(db.func.avg(Rating.value)).filter_by(recipe_id=recipe_id).scalar()

@app.route('/rate_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def rate_recipe(recipe_id):
    form = RatingForm()
    if form.validate_on_submit():
        rating = Rating(value=form.value.data, recipe_id=recipe_id, user_id=current_user.id)
        db.session.add(rating)
        db.session.commit()
        flash('Your rating has been submitted!', 'success')
    return redirect(url_for('recipe_details', recipe_id=recipe_id))

@app.route('/protected')
@login_required
def protected():
    return "This is only accessible to logged-in users."

@app.route('/api/recipes', methods=['GET'])
def api_get_recipes():
    recipes = Recipe.query.all()
    recipes_list = [{
        'id': r.id,
        'title': r.title,
        'ingredients': r.ingredients,
        'instructions': r.instructions,
        'category': r.category
    } for r in recipes]
    return jsonify(recipes_list)

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def api_get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    comments = [{'user': c.user.username, 'content': c.content} for c in recipe.comments]
    return jsonify({
        'title': recipe.title,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'category': recipe.category,
        'comments': comments
    })

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')  
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            return jsonify({"message": "Invalid or missing API key"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/protected',methods=['POST'])
@require_api_key
def protected_route():
    return jsonify({"message": "Success, you have access!"})

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')

os.getenv()

if sys.platform == 'win32':
    import win32com.client
else:

    pass
