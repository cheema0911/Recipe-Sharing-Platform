import os
import random
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required, current_user, login_user, logout_user
from .forms import RegistrationForm, RecipeForm, CommentForm, RatingForm, LoginForm
from .models import User, Recipe, Comment, Rating
from .extensions import db, bcrypt
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from .models import reposts

main = Blueprint('main', __name__)

def get_random_recipes(recipes, count):
    return random.sample(recipes, min(len(recipes), count))

@main.route('/')
def home():
    """Display suggested recipes."""
    suggested_recipes = Recipe.query.order_by(db.func.random()).limit(10).all()  
    all_recipes = Recipe.query.all()
    random_recipes = get_random_recipes(all_recipes, 4)
    return render_template('home.html', suggested_recipes=suggested_recipes, recipes=random_recipes)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('Username or email already exists. Please choose different ones.', 'danger')
        else:
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            try:
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('main.login'))
            except IntegrityError:
                db.session.rollback()
                flash('An error occurred. Please try again.', 'danger')
    return render_template('register.html', form=form)

@main.route('/browse_recipes')
def browse_recipes():
    keyword = request.args.get('keyword', '')
    category = request.args.get('category', '')
    dietary = request.args.get('dietary', '')
    difficulty = request.args.get('difficulty', '')
    query = Recipe.query
    if keyword:
        query = query.filter(Recipe.title.ilike(f'%{keyword}%') | Recipe.description.ilike(f'%{keyword}%'))
    if category:
        query = query.filter_by(category=category)
    if dietary:
        query = query.filter_by(dietary=dietary)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    recipes = query.all()
    return render_template('browse_recipes.html', recipes=recipes)

@main.route('/upload_recipe', methods=['GET', 'POST'])
@login_required
def upload_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(current_app.config['uploads'], filename)
            form.image.data.save(image_path)

            image_path = f'static/uploads/{filename}'

        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            category=form.category.data,
            dietary=form.dietary.data,
            difficulty=form.difficulty.data,
            image_path=image_path,
            user_id=current_user.id
        )

        db.session.add(recipe)
        db.session.commit()
        flash('Recipe uploaded successfully!', 'success')
        return redirect(url_for('main.profile', user_id=current_user.id))
    else:
        if form.errors:
            flash('Form validation failed. Please check your inputs.', 'danger')
    return render_template('upload_recipe.html', form=form)

@main.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    if recipe.user_id != current_user.id:
        flash('You are not authorized to delete this recipe.', 'danger')
        return redirect(url_for('main.profile', user_id=current_user.id))
    
    if recipe.image_path:
        image_path = os.path.join(current_app.root_path, recipe.image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(recipe)
    db.session.commit()

    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('main.profile', user_id=current_user.id))

@main.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    reposted = db.session.query(reposts).filter_by(user_id=current_user.id, recipe_id=recipe.id).first()

    form = CommentForm()
    rating_form = RatingForm()
    comments = Comment.query.filter_by(recipe_id=recipe.id).order_by(Comment.date_posted.desc()).all()
    average_rating = db.session.query(db.func.avg(Rating.value)).filter_by(recipe_id=recipe_id).scalar() or 'Not rated yet'

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You need to log in to post comments.', 'danger')
            return redirect(url_for('main.login'))

        comment = Comment(content=form.content.data, recipe_id=recipe.id, user=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('main.recipe', recipe_id=recipe.id))

    return render_template(
        'recipe.html',
        recipe=recipe,
        form=form,
        rating_form=rating_form,
        comments=comments,
        average_rating=average_rating,
        reposted=reposted
    )

@main.route('/save_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe not in current_user.favorite_recipes:
        current_user.favorite_recipes.append(recipe)
        db.session.commit()
        flash('Recipe saved to favorites!', 'success')
    else:
        flash('Recipe is already in your favorites.', 'info')
    return redirect(url_for('main.recipe', recipe_id=recipe_id))

@main.route('/unsave_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def unsave_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe in current_user.favorite_recipes:
        current_user.favorite_recipes.remove(recipe)
        db.session.commit()
        flash('Recipe removed from favorites!', 'success')
    else:
        flash('Recipe was not in your favorites.', 'info')
    return redirect(url_for('main.recipe', recipe_id=recipe_id))

@main.route('/saved_recipes')
@login_required
def saved_recipes():
    saved_recipes = current_user.favorite_recipes
    return render_template('saved_recipes.html', recipes=saved_recipes)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logout_user()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@main.route('/recipe/<int:recipe_id>/repost', methods=['POST'])
@login_required
def repost_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    repost_exists = db.session.query(reposts).filter_by(
        user_id=current_user.id, recipe_id=recipe_id
    ).first()
    
    if repost_exists:
        flash('You have already reposted this recipe.', 'info')
        return redirect(url_for('main.recipe', recipe_id=recipe_id))
    
    repost_entry = {"user_id": current_user.id, "recipe_id": recipe_id}
    db.session.execute(reposts.insert().values(repost_entry))
    recipe.reposts += 1
    db.session.commit()
    
    flash('Recipe reposted successfully!', 'success')
    return redirect(url_for('main.recipe', recipe_id=recipe_id))

@main.route('/recipe/<int:recipe_id>/remove_repost', methods=['POST'])
@login_required
def remove_repost(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    repost_exists = db.session.query(reposts).filter_by(
        user_id=current_user.id, recipe_id=recipe_id
    ).first()
    
    if not repost_exists:
        flash('You have not reposted this recipe.', 'info')
        return redirect(url_for('main.recipe', recipe_id=recipe_id))
    
    db.session.execute(reposts.delete().where(
        reposts.c.user_id == current_user.id,
        reposts.c.recipe_id == recipe_id
    ))
    recipe.reposts -= 1
    db.session.commit()
    
    flash('Repost removed successfully!', 'success')
    return redirect(url_for('main.recipe', recipe_id=recipe_id))

@main.route('/rate_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def rate_recipe(recipe_id):
    rating_value = request.form.get('rating')  
    recipe = Recipe.query.get_or_404(recipe_id)
    
    new_rating = Rating(value=rating_value, recipe_id=recipe.id, user_id=current_user.id)
    db.session.add(new_rating)
    db.session.commit()
    
    flash('Your rating has been submitted!', 'success')
    return redirect(url_for('main.recipe', recipe_id=recipe.id))  

@main.route('/remove_rating/<int:recipe_id>', methods=['POST'])
@login_required
def remove_rating(recipe_id):
    rating = Rating.query.filter_by(recipe_id=recipe_id, user_id=current_user.id).first()
    
    if rating:
        db.session.delete(rating)
        db.session.commit()
        flash('Your rating has been removed!', 'success')
    else:
        flash('You have not rated this recipe.', 'info')

    return redirect(url_for('main.recipe', recipe_id=recipe_id))

@main.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    """Display a user's profile with their uploaded recipes."""
    user = User.query.get_or_404(user_id)
    user_recipes = Recipe.query.filter_by(user_id=user.id).all()
    saved_recipes = current_user.favorite_recipes
    return render_template('profile.html', user=user, recipes=user_recipes, saved_recipes=saved_recipes)

@main.route('/remove_comment/<int:comment_id>', methods=['POST'])
@login_required
def remove_comment(comment_id):
    """Remove a specific comment."""
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.user_id == current_user.id:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment removed successfully!', 'success')
    else:
        flash('You are not authorized to remove this comment.', 'danger')
    
    return redirect(url_for('main.recipe', recipe_id=comment.recipe_id))