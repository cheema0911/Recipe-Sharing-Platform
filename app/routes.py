from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from .forms import RegistrationForm, RecipeForm, CommentForm, RatingForm
from .models import User, Recipe, Comment, Rating
from .extensions import db, bcrypt

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/recipes')
def browse_recipes():
    recipes = Recipe.query.all()
    return render_template('browse_recipes.html', recipes=recipes)

@main.route('/upload_recipe', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('main.browse_recipes'))
    return render_template('upload_recipe.html', form=form)

@main.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
def recipe_details(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You need to log in to post comments.', 'danger')
            return redirect(url_for('main.login'))
        comment = Comment(content=form.content.data, recipe=recipe, user=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
    return render_template('recipe.html', recipe=recipe, form=form)