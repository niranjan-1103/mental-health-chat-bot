from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil
import uuid
import json
import re
from datetime import datetime

from voice_engine import speech_to_text, text_to_speech
from chat_logic import get_chat_response, check_for_crisis

app = FastAPI(title="MindGuard API")

# Simple Database using JSON
DB_FILE = "data.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"goals": [], "moods": []}

def save_db(db_data):
    with open(DB_FILE, "w") as f:
        json.dump(db_data, f, indent=4)

# Setup directories for static files and uploads
os.makedirs("static/audio", exist_ok=True)
os.makedirs("static/uploads", exist_ok=True)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return html

class ChatRequest(BaseModel):
    text: str

class GoalRequest(BaseModel):
    title: str

class MoodRequest(BaseModel):
    mood: str

def process_interaction(text: str) -> dict:
    if not text:
        text = "I couldn't understand that clearly, could you repeat?"
        audio_file = text_to_speech(text)
        return {"text": text, "input_text": "", "audio": f"/static/audio/{audio_file}", "crisis": False, "mood": None}
        
    is_crisis = check_for_crisis(text)
    
    if is_crisis:
        response_text = "[CRISIS_OVERRIDE] I am an AI and cannot help in life-threatening situations. Please call your local emergency number (like 100 or 911) or go to the nearest hospital immediately."
    else:
        response_text = get_chat_response(text)
        if "[CRISIS_OVERRIDE]" in response_text:
            is_crisis = True
            
    # Extract Mood
    detected_mood = None
    mood_match = re.search(r"\[MOOD:(.*?)\]", response_text)
    if mood_match:
        detected_mood = mood_match.group(1).strip()
        response_text = re.sub(r"\[MOOD:.*?\]", "", response_text).strip()
        
        # Save mood quietly
        db = load_db()
        db["moods"].append({"timestamp": datetime.now().isoformat(), "mood": detected_mood, "source": "ai"})
        save_db(db)

    # Clean the token from the speech text
    speech_text = response_text.replace("[CRISIS_OVERRIDE]", "").strip()
    
    # Text to speech
    audio_file = text_to_speech(speech_text)
    
    return {
        "text": speech_text,
        "input_text": text,
        "audio": f"/static/audio/{audio_file}",
        "crisis": is_crisis,
        "mood": detected_mood
    }

@app.get("/api/dashboard")
async def get_dashboard():
    db = load_db()
    
    # Auto-populate 5 curated daily goals if empty
    if not db.get("goals"):
        default_goals = [
            "Drink 3 glasses of water",
            "Take 5 deep breaths in the Resources tab",
            "Take a 15-minute walk outside to relieve stress",
            "Acknowledge 1 thing you are grateful for",
            "Stretch your neck and shoulders"
        ]
        db["goals"] = [{"id": str(uuid.uuid4()), "title": g, "completed": False} for g in default_goals]
        save_db(db)

    tips = [
        "Take a 5-minute walk outside.",
        "Practice 4-7-8 breathing when stressed.",
        "Write down 3 things you are grateful for today."
    ]
    quotes = [
        "You are stronger than you think.",
        "Every day is a second chance.",
        "Small steps are still progress."
    ]
    import random
    return JSONResponse({
        "goals": db["goals"],
        "moods": db["moods"],
        "tip": random.choice(tips),
        "quote": random.choice(quotes)
    })

@app.post("/api/goals")
async def add_goal(req: GoalRequest):
    db = load_db()
    new_goal = {"id": str(uuid.uuid4()), "title": req.title, "completed": False}
    db["goals"].append(new_goal)
    save_db(db)
    return JSONResponse({"status": "success", "goal": new_goal})

@app.put("/api/goals/{goal_id}")
async def toggle_goal(goal_id: str):
    db = load_db()
    for g in db["goals"]:
        if g["id"] == goal_id:
            g["completed"] = not g["completed"]
            save_db(db)
            return JSONResponse({"status": "success", "goal": g})
    return JSONResponse({"status": "error", "message": "Goal not found"}, status_code=404)

@app.post("/api/mood")
async def log_mood(req: MoodRequest):
    db = load_db()
    new_mood = {"timestamp": datetime.now().isoformat(), "mood": req.mood, "source": "manual"}
    db["moods"].append(new_mood)
    save_db(db)
    return JSONResponse({"status": "success", "mood": new_mood})

@app.post("/api/chat")
async def chat_endpoint(audio: UploadFile = File(...)):
    # Save the incoming audio
    extension = audio.filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{extension}"
    upload_path = os.path.join("static/uploads", filename)
    
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
        
    # Convert audio to text
    text = speech_to_text(upload_path)
    
    # Process
    result = process_interaction(text)
    return JSONResponse(result)

@app.post("/api/chat/text")
async def chat_text_endpoint(req: ChatRequest):
    # Process
    result = process_interaction(req.text)
    return JSONResponse(result)
