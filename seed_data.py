from app import create_app, db
from app.models import Recipe

app = create_app()

# Use the application context to access the database
with app.app_context():
    # Add six additional new predefined recipes
    new_recipes = [
        {
            "title": "Classic Pancakes",
            "description": "Fluffy pancakes perfect for breakfast.",
            "ingredients": "Flour, Eggs, Milk, Sugar, Butter, Baking Powder",
            "instructions": "Mix the ingredients and cook on a skillet until golden brown.",
            "category": "Breakfast",
            "dietary": "None",
            "difficulty": "Easy",
            "image_path": "static/uploads/suggested1.jpg",
            "is_predefined": True,
        },
        {
            "title": "Spaghetti Bolognese",
            "description": "Rich and hearty spaghetti with a classic Bolognese sauce.",
            "ingredients": "Spaghetti, Ground Beef, Tomatoes, Onion, Garlic, Herbs",
            "instructions": "Cook spaghetti and simmer the sauce with ground beef and tomatoes.",
            "category": "Dinner",
            "dietary": "Halal",
            "difficulty": "Medium",
            "image_path": "static/uploads/suggested2.jpg",
            "is_predefined": True,
        },
        {
            "title": "Vegan Buddha Bowl",
            "description": "Healthy and colorful bowl filled with vegetables, grains, and plant-based protein.",
            "ingredients": "Quinoa, Chickpeas, Spinach, Avocado, Sweet Potato",
            "instructions": "Cook quinoa and roast sweet potatoes. Assemble with fresh veggies.",
            "category": "Lunch",
            "dietary": "Vegan",
            "difficulty": "Easy",
            "image_path": "static/uploads/suggested3.jpg",
            "is_predefined": True,
        },
        {
            "title": "Chocolate Chip Cookies",
            "description": "Delicious homemade cookies with chocolate chips.",
            "ingredients": "Flour, Sugar, Butter, Eggs, Chocolate Chips, Baking Soda",
            "instructions": "Mix ingredients and bake at 350°F (175°C) for 10-12 minutes.",
            "category": "Dessert",
            "dietary": "Vegetarian",
            "difficulty": "Easy",
            "image_path": "static/uploads/suggested4.jpg",
              "is_predefined": True,  # Ensure this image exists
        },
        {
            "title": "Caprese Salad",
            "description": "A simple Italian salad made of fresh mozzarella, tomatoes, and basil.",
            "ingredients": "Fresh mozzarella, Tomatoes, Basil leaves, Olive oil, Balsamic glaze",
            "instructions": "Slice mozzarella and tomatoes. Arrange with basil leaves. Drizzle with olive oil and balsamic glaze.",
            "category": "Lunch",
            "dietary": "Vegetarian",
            "difficulty": "Easy",
            "image_path": "static/uploads/lunch2.jpg",
            "is_predefined": True,
        },
        {
            "title": "Thai Green Curry",
            "description": "Spicy and aromatic Thai green curry with coconut milk and vegetables.",
            "ingredients": "Coconut milk, Green curry paste, Chicken or tofu, Bamboo shoots, Vegetables",
            "instructions": "Sauté curry paste. Add coconut milk and vegetables. Simmer until cooked.",
            "category": "Dinner",
            "dietary": "Halal",
            "difficulty": "Medium",
            "image_path": "static/uploads/breakfast1.jpg",
            "is_predefined": True,
        },
        {
            "title": "Avocado Toast",
            "description": "A quick and healthy breakfast option with mashed avocado on toast.",
            "ingredients": "Avocado, Bread, Lemon juice, Salt, Pepper",
            "instructions": "Mash avocado with lemon juice, salt, and pepper. Spread on toasted bread.",
            "category": "Breakfast",
            "dietary": "Vegan",
            "difficulty": "Easy",
            "image_path": "static/uploads/breakfast2.jpg",
            "is_predefined": True,
        },
        {
            "title": "Miso Soup",
            "description": "A traditional Japanese soup made with miso paste and tofu.",
            "ingredients": "Miso paste, Tofu, Seaweed, Green onions, Dashi stock",
            "instructions": "Heat dashi stock. Stir in miso paste. Add tofu, seaweed, and green onions.",
            "category": "Lunch",
            "dietary": "Vegan",
            "difficulty": "Easy",
            "image_path": "static/uploads/lunch1.jpg",
            "is_predefined": True,
        },
        {
            "title": "Beef Tacos",
            "description": "Mexican-style tacos with seasoned beef, fresh toppings, and tortillas.",
            "ingredients": "Ground beef, Taco seasoning, Tortillas, Lettuce, Cheese, Salsa",
            "instructions": "Cook beef with taco seasoning. Assemble tacos with toppings.",
            "category": "Dinner",
            "dietary": "Halal",
            "difficulty": "Medium",
            "image_path": "static/uploads/dinner1.jpg",
            "is_predefined": True,
        },
        {
            "title": "Strawberry Smoothie",
            "description": "Refreshing smoothie made with fresh strawberries and yogurt.",
            "ingredients": "Strawberries, Yogurt, Honey, Ice cubes",
            "instructions": "Blend all ingredients until smooth. Serve chilled.",
            "category": "Breakfast",
            "dietary": "Vegetarian",
            "difficulty": "Easy",
            "image_path": "static/uploads/dinner2.jpg",
            "is_predefined": True,
        },
    ]

    for recipe_data in new_recipes:
        existing_recipe = Recipe.query.filter_by(title=recipe_data["title"]).first()
        if not existing_recipe:
            recipe = Recipe(**recipe_data, user_id=1)  
            db.session.add(recipe)

    db.session.commit()
    print("New sample recipes added to the database.")
