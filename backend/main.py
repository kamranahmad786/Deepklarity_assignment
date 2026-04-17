from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import uvicorn
import os
from datetime import datetime

import models, scraper, llm_manager
from database import engine, get_db, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recipe Extractor API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExtractRequest(BaseModel):
    url: str | None = None
    raw_text: str | None = None

class MealPlanRequest(BaseModel):
    recipe_ids: List[int]

@app.post("/api/extract")
async def extract_recipe(request: ExtractRequest, db: Session = Depends(get_db)):
    """Scrapes a URL or processes raw text with LLM, and stores in database."""
    
    scraped_data = None
    source_url = request.url

    if request.raw_text:
        # Manual paste mode
        scraped_data = {
            "url": "Manual Entry",
            "raw_text": request.raw_text,
            "json_ld": {}
        }
        source_url = f"manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    elif request.url:
        # Check if already exists
        existing = db.query(models.Recipe).filter(models.Recipe.url == request.url).first()
        if existing:
            return existing

        # Scrape
        result = scraper.scrape_recipe_page(request.url)
        if not result:
            raise HTTPException(status_code=400, detail="Could not scrape the provided URL.")
        
        if isinstance(result, dict) and "status" in result and result["status"] != 200:
            # Special handling for blocked sites to trigger UI fallback
            raise HTTPException(
                status_code=result["status"], 
                detail=f"Access denied (Blocked by site). {result.get('error', '')}"
            )
            
        scraped_data = result
    else:
        raise HTTPException(status_code=400, detail="Either URL or Raw Text must be provided.")

    # LLM Extract
    extracted_data = llm_manager.extract_recipe_details(scraped_data)
    if not extracted_data:
        raise HTTPException(status_code=500, detail="LLM failed to process the recipe.")
    
    # Save to DB
    new_recipe = models.Recipe(
        url=source_url,
        title=extracted_data.get("title"),
        cuisine=extracted_data.get("cuisine"),
        prep_time=extracted_data.get("prep_time"),
        cook_time=extracted_data.get("cook_time"),
        total_time=extracted_data.get("total_time"),
        servings=extracted_data.get("servings"),
        difficulty=extracted_data.get("difficulty"),
        ingredients=extracted_data.get("ingredients"),
        instructions=extracted_data.get("instructions"),
        nutrition_estimate=extracted_data.get("nutrition_estimate"),
        substitutions=extracted_data.get("substitutions"),
        shopping_list=extracted_data.get("shopping_list"),
        related_recipes=extracted_data.get("related_recipes")
    )
    
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    
    return new_recipe

@app.get("/api/recipes")
async def get_recipes(db: Session = Depends(get_db)):
    """Returns list of all saved recipes (limited history)."""
    return db.query(models.Recipe).order_by(models.Recipe.created_at.desc()).all()

@app.get("/api/recipes/{recipe_id}")
async def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Returns details for a specific recipe."""
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found.")
    return recipe

@app.post("/api/meal-plan")
async def create_meal_plan(request: MealPlanRequest, db: Session = Depends(get_db)):
    """Generates a combined shopping list for multiple recipes."""
    recipes = db.query(models.Recipe).filter(models.Recipe.id.in_(request.recipe_ids)).all()
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found for the provided IDs.")
    
    merged_list = llm_manager.generate_combined_shopping_list(recipes)
    if not merged_list:
        raise HTTPException(status_code=500, detail="Failed to generate combined shopping list.")
        
    return merged_list

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
