from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib
import pandas as pd
from utils.ai_insights import get_ai_insight

app = FastAPI(title="AI Productivity Assistant", version="2.0")

# Template setup
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load ML model
model = joblib.load("model/model.pkl")

def generate_recommendation(category: str) -> str:
    if category == "High":
        return "Great job! Keep your current routine consistent."
    elif category == "Medium":
        return "You’re doing okay, but try improving focus or sleep hours."
    else:
        return "You may need more rest or better focus management today."

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "result": None})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    hours_worked: float = Form(...),
    sleep_hours: float = Form(...),
    tasks_completed: int = Form(...),
    breaks_taken: int = Form(...),
    focus_level: float = Form(...)
):
    # Create dataframe for model
    data = pd.DataFrame([{
        "hours_worked": hours_worked,
        "sleep_hours": sleep_hours,
        "tasks_completed": tasks_completed,
        "breaks_taken": breaks_taken,
        "focus_level": focus_level
    }])
    prediction = model.predict(data)[0]
    recommendation = generate_recommendation(prediction)
    ai_prompt = f"Give personalized productivity advice for a {prediction} productivity day."
    ai_text = get_ai_insight(ai_prompt)

    result = {
        "prediction": prediction,
        "recommendation": recommendation,
        "ai_text": ai_text
    }

    return templates.TemplateResponse("dashboard.html", {"request": request, "result": result})
from database import SessionLocal, ProductivityRecord

...

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    hours_worked: float = Form(...),
    sleep_hours: float = Form(...),
    tasks_completed: int = Form(...),
    breaks_taken: int = Form(...),
    focus_level: float = Form(...)
):
    data = pd.DataFrame([{
        "hours_worked": hours_worked,
        "sleep_hours": sleep_hours,
        "tasks_completed": tasks_completed,
        "breaks_taken": breaks_taken,
        "focus_level": focus_level
    }])
    prediction = model.predict(data)[0]
    recommendation = generate_recommendation(prediction)
    ai_prompt = f"Give personalized productivity advice for a {prediction} productivity day."
    ai_text = get_ai_insight(ai_prompt)

    # Save to DB
    db = SessionLocal()
    record = ProductivityRecord(
        hours_worked=hours_worked,
        sleep_hours=sleep_hours,
        tasks_completed=tasks_completed,
        breaks_taken=breaks_taken,
        focus_level=focus_level,
        prediction=prediction
    )
    db.add(record)
    db.commit()
    db.close()

    result = {
        "prediction": prediction,
        "recommendation": recommendation,
        "ai_text": ai_text
    }

    return templates.TemplateResponse("dashboard.html", {"request": request, "result": result})
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

@app.get("/weekly_summary")
def weekly_summary():
    db = SessionLocal()
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    records = db.query(ProductivityRecord).filter(ProductivityRecord.timestamp >= one_week_ago).all()
    db.close()

    if not records:
        return JSONResponse({"summary": "No data yet for this week."})

    # Basic analytics
    total = len(records)
    high = sum(1 for r in records if r.prediction == "High")
    medium = sum(1 for r in records if r.prediction == "Medium")
    low = sum(1 for r in records if r.prediction == "Low")

    prompt = (
        f"This week, the user had {high} high, {medium} medium, and {low} low productivity days "
        f"out of {total} total. Provide a concise AI summary with suggestions for improvement."
    )
    ai_summary = get_ai_insight(prompt)

    return JSONResponse({"summary": ai_summary})
