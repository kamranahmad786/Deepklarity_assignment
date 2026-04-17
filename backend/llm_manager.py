import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Initialize the Gemini LLM
# Use gemini-1.5-flash for speed and cost-efficiency
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    temperature=0.1,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def extract_recipe_details(scraped_data):
    """Uses LLM to extract structured data from scraped content."""
    
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "recipe_extraction_prompt.txt")
    with open(prompt_path, "r") as f:
        prompt_template = f.read()
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm | StrOutputParser()
    
    try:
        response = chain.invoke({
            "url": scraped_data["url"],
            "json_ld": json.dumps(scraped_data["json_ld"], indent=2),
            "raw_text": scraped_data["raw_text"]
        })
        
        # Parse JSON from response
        # Sometimes LLMs wrap response in ```json ```
        cleaned_response = response.strip()
        if "```json" in cleaned_response:
            cleaned_response = cleaned_response.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned_response:
            cleaned_response = cleaned_response.split("```")[1].split("```")[0].strip()
            
        return json.loads(cleaned_response)
    except Exception as e:
        # Re-raise so main.py can capture the details
        raise Exception(f"Gemini API Error: {str(e)}")

def generate_combined_shopping_list(recipes):
    """Uses LLM to merge shopping lists from multiple recipes."""
    
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "meal_planner_prompt.txt")
    with open(prompt_path, "r") as f:
        prompt_template = f.read()
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm | StrOutputParser()
    
    recipes_json = json.dumps([
        {
            "title": r.title,
            "ingredients": r.ingredients,
            "shopping_list": r.shopping_list
        } for r in recipes
    ], indent=2)
    
    try:
        response = chain.invoke({
            "recipes_json": recipes_json
        })
        
        cleaned_response = response.strip()
        if "```json" in cleaned_response:
            cleaned_response = cleaned_response.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned_response:
            cleaned_response = cleaned_response.split("```")[1].split("```")[0].strip()
            
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Error in Meal Plan generation: {e}")
        return None
