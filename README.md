# 🍳 DailyBite: AI-Powered Recipe Intelligence & Meal Planner

DailyBite is a high-performance, full-stack application designed to transform messy food blog URLs into structured, actionable culinary data. Leveraging **Gemini 1.5 Flash**, the system provides deep recipe analysis, nutritional estimations, and an intelligent meal planning engine.

---

## 🌟 Key Features

### 1. Resilient Recipe Extraction Engine
- **Stealth Scraping**: Uses `curl_cffi` with impersonated browser identities (Chrome, Safari) to bypass aggressive bot protections.
- **Invisible Fallback**: Automatically falls back to **Google Web Cache** if a site blocks direct access.
- **Dual-Mode Processing**: Supports both URL-based extraction and manual text paste for recipes behind complex paywalls.
- **JSON-LD Aware**: Prioritizes structured Schema.org metadata while using LLM vision for unstructured content.

### 2. AI-Driven Culinary Insights
- **Smart Parsing**: Segregates ingredients into quantity, unit, and item for precise calculations.
- **Nutritional Estimation**: Generates automatic per-serving estimates for Calories, Protein, Carbs, and Fat.
- **Substitution Engine**: Provides 3 intelligent ingredient substitutions for every recipe.
- **Pairing Recommendations**: Suggests complementary dishes to complete the meal.

### 3. Intelligent Meal Planner
- **Multi-Recipe Selection**: Select multiple recipes from history to generate a unified meal plan.
- **Categorized Shopping List**: Automatically merges duplicate ingredients and groups them by category (Produce, Dairy, Pantry, etc.) using AI.
- **One-Click Export**: Copy the entire shopping list to your clipboard or print for physical use.

---

## 🛠️ Technical Stack

- **Frontend**: 
  - React 18 (Vite)
  - Lucide-React for Premium Iconography
  - Vanilla CSS3 with Glassmorphic Design System
  - Axios for API Communication
- **Backend**: 
  - FastAPI (Python 3.10+)
  - SQLAlchemy ORM
  - BeautifulSoup4 & Cloudscraper for initial parsing
  - `curl_cffi` for advanced stealth requests
- **Database**: 
  - PostgreSQL (Persistent storage of recipe history)
- **AI Integration**: 
  - Google Gemini 1.5 Flash (via LangChain/Google Generative AI)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js & NPM
- PostgreSQL (Active Instance)
- Google Gemini API Key

### 1. Database Configuration
Ensure PostgreSQL is running and create the project database:
```bash
createdb recipe_db
```

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Environment Variables (`backend/.env`):
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   DATABASE_URL=postgresql://localhost/recipe_db
   ```
4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

---

## 📂 Project Structure

```text
├── backend/
│   ├── main.py            # FastAPI Entry Point
│   ├── scraper.py         # Resilient Stealth Scraper
│   ├── llm_manager.py     # Gemini AI Integration Logic
│   ├── models.py          # SQLAlchemy Database Models
│   └── .gitignore         # Backend-specific exclusions [NEW]
├── frontend/
│   ├── src/App.jsx        # Premium React UI
│   └── index.css          # Design System & Animations
├── prompts/
│   ├── recipe_extraction_prompt.txt
│   └── meal_planner_prompt.txt
└── sample_data/           # Test URLs and Example Payloads
```




