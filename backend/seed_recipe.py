from sqlalchemy.orm import Session
from database import SessionLocal
import models
from datetime import datetime

# Data extracted by browser subagent
recipe_data = {
  "title": "Macaroni and Cheese",
  "cuisine": "American",
  "prep_time": "10 min",
  "cook_time": "55 min",
  "total_time": "1 hr 5 min",
  "servings": "6 to 8 servings",
  "ingredients": [
    {"item": "elbow macaroni", "quantity": "4", "unit": "cups (1 pound)"},
    {"item": "unsalted butter (split)", "quantity": "5", "unit": "tablespoons"},
    {"item": "milk", "quantity": "4", "unit": "cups"},
    {"item": "medium onion, stuck with 1 clove", "quantity": "1/2", "unit": ""},
    {"item": "cloves garlic", "quantity": "4", "unit": ""},
    {"item": "bay leaf", "quantity": "1", "unit": ""},
    {"item": "sprigs fresh thyme", "quantity": "3", "unit": ""},
    {"item": "dry mustard", "quantity": "1", "unit": "teaspoon"},
    {"item": "all-purpose flour", "quantity": "2", "unit": "tablespoons"},
    {"item": "grated Cheddar", "quantity": "2", "unit": "cups"},
    {"item": "grated Parmesan", "quantity": "1/2", "unit": "cup"},
    {"item": "Cheddar in big chunks", "quantity": "1", "unit": "cup"}
  ],
  "instructions": [
    "Cook the macaroni in a large pot of boiling salted water until done, about 5 to 7 minutes. Drain and toss it with 2 tablespoons butter; set aside.",
    "Heat the oven to 350 degrees F.",
    "Coat a large baking dish with 1 tablespoon butter and set it aside.",
    "Put the milk into a saucepan and add the clove studded onion, garlic, bay leaf, thyme, and mustard.",
    "Warm over medium low heat until the milk starts to steam, about 10 minutes.",
    "Remove from the heat and let the flavors infuse while you make the roux.",
    "In a large pot over medium heat add 2 tablespoons butter and the flour.",
    "Cook, stirring, for about 2 to 3 minutes; don't let the roux color.",
    "Strain the infused milk onto the roux, whisking constantly to avoid lumps.",
    "Cook, stirring often, for about 5 minutes until the sauce is thick.",
    "Remove from the heat and add 1/2 the grated Cheddar and 1/2 the Parmesan; stir until it is melted and smooth.",
    "Taste and adjust seasoning with salt and pepper.",
    "Pour this over the macaroni, add the chunks of Cheddar, and mix until well blended; put this into the prepared baking dish.",
    "Sprinkle the remaining Cheddar and Parmesan cheeses evenly over the top.",
    "Bake until the top is golden and crusty, about 25 to 30 minutes."
  ],
  "nutrition_estimate": {
    "calories": "High",
    "protein": "25g",
    "carbs": "60g",
    "fat": "35g"
  },
  "substitutions": ["Use gluten-free macaroni if needed", "Gruyere works well instead of Cheddar"],
  "related_recipes": ["Garlic Bread", "Green Salad", "Roasted Broccoli"],
  "url": "https://www.foodnetwork.com/recipes/tyler-florence/macaroni-and-cheese-recipe-1915846"
}

def seed_recipe():
    db = SessionLocal()
    try:
        # Check if already exists
        existing = db.query(models.Recipe).filter(models.Recipe.url == recipe_data["url"]).first()
        if existing:
            print("Recipe already in database.")
            return

        new_recipe = models.Recipe(
            url=recipe_data["url"],
            title=recipe_data["title"],
            cuisine=recipe_data["cuisine"],
            prep_time=recipe_data["prep_time"],
            cook_time=recipe_data["cook_time"],
            total_time=recipe_data["total_time"],
            servings=recipe_data["servings"],
            difficulty="Medium",
            ingredients=recipe_data["ingredients"],
            instructions=recipe_data["instructions"],
            nutrition_estimate=recipe_data["nutrition_estimate"],
            substitutions=recipe_data["substitutions"],
            related_recipes=recipe_data["related_recipes"],
            shopping_list=recipe_data["ingredients"] # Use simplified list
        )
        db.add(new_recipe)
        db.commit()
        print(f"Successfully seeded: {recipe_data['title']}")
    except Exception as e:
        print(f"Error seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_recipe()
