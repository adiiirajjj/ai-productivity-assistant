from fastapi import FastAPI
import joblib
import pandas as pd
from utils.ai_insights import get_ai_insight

app = FastAPI(title="AI Productivity Assistant", version="1.0")

# Load the trained model
model = joblib.load("model/model.pkl")

@app.get("/")
def root():
    return {"message": "Welcome to AI Productivity Assistant API"}

@app.post("/predict/")
def predict(hours_worked: float, sleep_hours: float, tasks_completed: int, breaks_taken: int, focus_level: float):
    data = pd.DataFrame([{
        "hours_worked": hours_worked,
        "sleep_hours": sleep_hours,
        "tasks_completed": tasks_completed,
        "breaks_taken": breaks_taken,
        "focus_level": focus_level
    }])
    prediction = model.predict(data)[0]
    return {"Predicted Productivity": prediction}

@app.get("/ai_insight/")
def ai_insight(summary_prompt: str):
    """
    Example:
    /ai_insight/?summary_prompt=Suggest ways to improve focus and reduce breaks.
    """
    insight = get_ai_insight(summary_prompt)
    return {"AI Insight": insight}
