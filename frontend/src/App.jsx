import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Search,
  History as HistoryIcon,
  ChefHat,
  Clock,
  Users,
  Flame,
  ShoppingBasket,
  UtensilsCrossed,
  Replace,
  TrendingUp,
  X,
  Printer,
  Copy
} from 'lucide-react';

const API_BASE = "http://localhost:8000/api";

function App() {
  const [activeTab, setActiveTab] = useState('extract');
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [recipe, setRecipe] = useState(null);
  const [history, setHistory] = useState([]);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [mealPlanIds, setMealPlanIds] = useState([]);
  const [mergedShoppingList, setMergedShoppingList] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`${API_BASE}/recipes`);
      setHistory(res.data);
    } catch (err) {
      console.error("Failed to fetch history", err);
    }
  };

  const handleExtract = async () => {
    if (!url) return;
    setLoading(true);
    setRecipe(null);
    try {
      const res = await axios.post(`${API_BASE}/extract`, { url });
      setRecipe(res.data);
      fetchHistory();
    } catch (err) {
      alert("Error extracting recipe. Please check the URL and try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleMealPlan = async () => {
    if (mealPlanIds.length < 2) {
      alert("Please select at least 2 recipes.");
      return;
    }
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/meal-plan`, { recipe_ids: mealPlanIds });
      setMergedShoppingList(res.data);
    } catch (err) {
      alert("Failed to generate meal plan.");
    } finally {
      setLoading(false);
    }
  };

  const toggleMealPlanId = (id) => {
    setMealPlanIds(prev =>
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  const handlePrint = () => {
    window.print();
  };

  const handleCopyList = () => {
    if (!mergedShoppingList) return;
    const text = Object.entries(mergedShoppingList)
      .map(([cat, items]) => `${cat.toUpperCase()}\n${items.map(i => `- ${i}`).join('\n')}`)
      .join('\n\n');
    navigator.clipboard.writeText(text);
    alert("Shopping list copied to clipboard!");
  };

  const loadingPhrases = [
    "Analyzing culinary data...",
    "Bypassing site firewalls...",
    "Rotating identity profiles...",
    "Searching for recipe metadata...",
    "Organizing ingredients...",
    "Almost there..."
  ];
  const [phraseIndex, setPhraseIndex] = useState(0);

  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(() => {
        setPhraseIndex((prev) => (prev + 1) % loadingPhrases.length);
      }, 2500);
    } else {
      setPhraseIndex(0);
    }
    return () => clearInterval(interval);
  }, [loading]);

  return (
    <div className="container">
      <header className="animate-slideDown">
        <h1 style={{ color: 'var(--text)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
          <ChefHat size={44} color="var(--primary)" />
          <span style={{ background: 'linear-gradient(to right, var(--primary), var(--accent))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            DailyBite
          </span>
        </h1>
      </header>

      <div className="nav-wrapper glass">
        <button
          className={`tab-btn ${activeTab === 'extract' ? 'active' : ''}`}
          onClick={() => setActiveTab('extract')}
        >
          <Search size={18} /> Extract
        </button>
        <button
          className={`tab-btn ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          <HistoryIcon size={18} /> History
        </button>
        <button
          className={`tab-btn ${activeTab === 'mealplan' ? 'active' : ''}`}
          onClick={() => setActiveTab('mealplan')}
        >
          <UtensilsCrossed size={18} /> Planner
        </button>
      </div>

      <main>
        {activeTab === 'extract' && (
          <section className="animate-slideUp">
            <div className="input-hero">
              <input
                type="text"
                placeholder="Paste a recipe blog URL here..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
              <button className="btn-primary" onClick={handleExtract} disabled={loading}>
                {loading ? (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div className="spinner"></div> Processing
                  </div>
                ) : (
                  <>Extract Recipe <ChefHat size={20} /></>
                )}
              </button>
            </div>

            {loading && !recipe && (
              <div style={{ textAlign: 'center', marginTop: '3rem' }}>
                <div className="scan-line"></div>
                <p className="subtitle animate-pulse">{loadingPhrases[phraseIndex]}</p>
              </div>
            )}

            {recipe && <RecipeDetails recipe={recipe} />}
          </section>
        )}

        {activeTab === 'history' && (
          <section className="animate-slideUp">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '1.5rem' }}>
              <h2 className="section-title"><HistoryIcon /> Recently Saved</h2>
              <span className="subtitle">{history.length} recipes found</span>
            </div>

            <div className="history-grid">
              {history.map(r => (
                <div key={r.id} className="recipe-card glass" onClick={() => setSelectedRecipe(r)}>
                  <div className="recipe-card-content">
                    <div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                        <span className={`badge badge-${{ easy: 'success', medium: 'warning', hard: 'info' }[r.difficulty?.toLowerCase()] || 'info'}`}>
                          {r.difficulty}
                        </span>
                        <span className="subtitle" style={{ fontSize: '0.75rem' }}>
                          {new Date(r.created_at).toLocaleDateString()}
                        </span>
                      </div>
                      <h3 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>{r.title}</h3>
                      <p className="subtitle" style={{ fontSize: '0.85rem' }}>{r.cuisine} • {r.total_time}</p>
                    </div>
                    <div style={{ marginTop: '1rem', borderTop: '1px solid var(--border)', paddingTop: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: '0.8rem', color: 'var(--primary-dark)', fontWeight: 600 }}>View Details →</span>
                      <UtensilsCrossed size={16} color="var(--text-muted)" />
                    </div>
                  </div>
                </div>
              ))}
            </div>
            {history.length === 0 && (
              <div style={{ textAlign: 'center', padding: '5rem 0' }}>
                <Search size={48} color="var(--text-muted)" style={{ marginBottom: '1rem' }} />
                <p className="subtitle">No recipes saved yet. Start by extracting your first recipe!</p>
              </div>
            )}
          </section>
        )}

        {activeTab === 'mealplan' && (
          <section className="animate-slideUp">
            <div className="card glass">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <div>
                  <h2 className="section-title" style={{ marginBottom: '0.25rem' }}><UtensilsCrossed /> Meal Planner</h2>
                  <p className="subtitle">Select recipes to create a combined shopping list</p>
                </div>
                {mealPlanIds.length > 0 && (
                  <button className="tab-btn" onClick={() => setMealPlanIds([])} style={{ padding: '0.5rem 1rem', fontSize: '0.8rem' }}>Clear All</button>
                )}
              </div>

              <div className="history-grid" style={{ marginBottom: '2rem' }}>
                {history.length === 0 ? (
                  <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '3rem 0' }}>
                    <p className="subtitle">No recipes found. Extract some recipes first!</p>
                  </div>
                ) : (
                  history.map(r => (
                    <div
                      key={r.id}
                      className={`recipe-card glass ${mealPlanIds.includes(r.id) ? 'active-selection' : ''}`}
                      style={{
                        padding: '0',
                        border: mealPlanIds.includes(r.id) ? '2px solid var(--primary)' : '1px solid var(--border)',
                        background: mealPlanIds.includes(r.id) ? 'var(--primary-light)' : 'var(--surface)'
                      }}
                      onClick={() => toggleMealPlanId(r.id)}
                    >
                      <div className="recipe-card-content" style={{ padding: '1.25rem' }}>
                        <h4 style={{ fontSize: '0.95rem', marginBottom: '0.25rem' }}>{r.title}</h4>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <span className="subtitle" style={{ fontSize: '0.75rem' }}>{r.cuisine}</span>
                          {mealPlanIds.includes(r.id) && <div style={{ background: 'var(--primary)', borderRadius: '50%', width: '20px', height: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><X size={12} color="white" /></div>}
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>

              <div style={{ textAlign: 'center' }}>
                <button
                  className="btn-primary"
                  style={{ margin: '0 auto', padding: '1rem 3rem', height: 'auto' }}
                  onClick={handleMealPlan}
                  disabled={loading || mealPlanIds.length < 2}
                >
                  {loading ? 'Analyzing Substitutions...' : `Generate List for ${mealPlanIds.length} Recipes`}
                </button>
                <p className="subtitle" style={{ marginTop: '0.75rem', fontSize: '0.8rem' }}>Select at least 2 recipes to begin</p>
              </div>
            </div>

            {mergedShoppingList && (
              <div className="card glass animate-slideUp" style={{ marginTop: '2rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
                  <h2 className="section-title" style={{ margin: 0 }}><ShoppingBasket /> Smart Shopping List</h2>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button className="tab-btn glass" style={{ fontSize: '0.8rem' }} onClick={handlePrint}><Printer size={14} /> Print</button>
                    <button className="tab-btn glass" style={{ fontSize: '0.8rem' }} onClick={handleCopyList}><Copy size={14} /> Copy List</button>
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '2.5rem' }}>
                  {Object.entries(mergedShoppingList).map(([cat, items]) => (
                    <div key={cat}>
                      <h4 style={{ textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '1px', color: 'var(--primary-dark)', marginBottom: '1rem', borderBottom: '2px solid var(--primary-light)', pb: '0.5rem' }}>
                        {cat}
                      </h4>
                      <ul className="items-list">
                        {items.map((item, idx) => (
                          <li key={idx} style={{ display: 'flex', gap: '10px', alignItems: 'start', padding: '0.75rem 0' }}>
                            <input type="checkbox" style={{ marginTop: '5px', width: '18px', height: '18px', cursor: 'pointer', accentColor: 'var(--primary)' }} />
                            <span>{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}
      </main>

      {selectedRecipe && (
        <div className="modal-overlay" onClick={() => setSelectedRecipe(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setSelectedRecipe(null)}><X /></button>
            <RecipeDetails recipe={selectedRecipe} />
          </div>
        </div>
      )}
    </div>
  );
}

function RecipeDetails({ recipe }) {
  return (
    <div className="recipe-details animate-slideUp">
      <div className="recipe-header" style={{ marginBottom: '3rem', textAlign: 'center' }}>
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1rem' }}>
          <span className={`badge badge-${{ easy: 'success', medium: 'warning', hard: 'info' }[recipe.difficulty?.toLowerCase()] || 'info'}`} style={{ fontSize: '0.9rem' }}>
            {recipe.difficulty}
          </span>
        </div>
        <h2 style={{ fontSize: '2.5rem', fontWeight: 800, marginBottom: '1rem', color: 'var(--text)' }}>{recipe.title}</h2>

        <div className="glass" style={{ display: 'inline-flex', padding: '1rem 2rem', borderRadius: '50px', gap: '2rem', flexWrap: 'wrap', justifyContent: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Clock size={18} color="var(--primary)" /> <span>{recipe.total_time}</span></div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Users size={18} color="var(--accent)" /> <span>{recipe.servings} Servings</span></div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><UtensilsCrossed size={18} color="var(--secondary)" /> <span>{recipe.cuisine}</span></div>
        </div>
      </div>

      <div className="recipe-grid">
        <div className="main-content">
          <div className="card glass" style={{ padding: '2rem', borderLeft: '4px solid var(--primary)' }}>
            <h3 className="section-title"><ShoppingBasket size={22} /> Ingredients</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem', marginTop: '1.5rem' }}>
              {recipe.ingredients?.map((ing, idx) => (
                <div key={idx} style={{ padding: '1rem', background: 'rgba(0,0,0,0.02)', borderRadius: '12px' }}>
                  <span style={{ color: 'var(--primary-dark)', fontWeight: 800 }}>{ing.quantity} {ing.unit}</span>
                  <p style={{ fontSize: '0.9rem', color: 'var(--text)' }}>{ing.item}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="card glass" style={{ padding: '2rem', marginTop: '2rem' }}>
            <h3 className="section-title"><ChefHat size={22} /> Method</h3>
            <div style={{ marginTop: '1.5rem' }}>
              {recipe.instructions?.map((step, idx) => (
                <div key={idx} style={{ display: 'flex', gap: '1.5rem', marginBottom: '2rem', alignItems: 'start' }}>
                  <span style={{
                    background: 'var(--primary)',
                    color: 'white',
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                    fontWeight: 800,
                    fontSize: '0.9rem',
                    boxShadow: '0 4px 10px rgba(var(--primary-rgb), 0.3)'
                  }}>
                    {idx + 1}
                  </span>
                  <p style={{ fontSize: '1.05rem', lineHeight: '1.7', color: 'var(--text)' }}>{step}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <aside>
          <div className="card glass" style={{ padding: '1.5rem', marginBottom: '2rem' }}>
            <h3 className="section-title" style={{ fontSize: '1.1rem' }}><TrendingUp size={18} /> Nutrition <span>(per serving)</span></h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
              {[
                { label: 'Calories', val: recipe.nutrition_estimate?.calories, color: 'var(--primary)' },
                { label: 'Protein', val: recipe.nutrition_estimate?.protein, color: 'var(--accent)' },
                { label: 'Carbs', val: recipe.nutrition_estimate?.carbs, color: 'var(--secondary)' },
                { label: 'Fat', val: recipe.nutrition_estimate?.fat, color: '#e91e63' }
              ].map(stat => (
                <div key={stat.label} style={{ padding: '0.75rem', border: '1px solid var(--border)', borderRadius: '12px', textAlign: 'center' }}>
                  <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>{stat.label}</p>
                  <p style={{ fontSize: '1.1rem', fontWeight: 800, color: stat.color }}>{stat.val || '--'}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="card glass" style={{ padding: '1.5rem', marginBottom: '2rem' }}>
            <h3 className="section-title" style={{ fontSize: '1.1rem' }}><Replace size={18} /> Substitutions</h3>
            <ul className="items-list" style={{ marginTop: '1rem' }}>
              {recipe.substitutions?.map((sub, idx) => (
                <li key={idx} style={{ fontSize: '0.85rem', color: 'var(--text-muted)', display: 'flex', gap: '10px', alignItems: 'start' }}>
                  <div style={{ width: '6px', height: '6px', background: 'var(--secondary)', borderRadius: '50%', marginTop: '8px', flexShrink: 0 }}></div>
                  {sub}
                </li>
              ))}
            </ul>
          </div>

          <div className="card glass" style={{ padding: '1.5rem' }}>
            <h3 className="section-title" style={{ fontSize: '1.1rem' }}><UtensilsCrossed size={18} /> Pairings</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '1rem' }}>
              {recipe.related_recipes?.map((rel, idx) => (
                <span key={idx} className="badge badge-info" style={{ fontSize: '0.7rem', textTransform: 'none' }}>{rel}</span>
              ))}
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}

export default App;
