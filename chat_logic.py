import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def get_system_prompt() -> str:
    try:
        with open('.agents/skills/safety.md', 'r') as f:
            safety_context = f.read()
    except Exception:
        safety_context = "Fallback safety: Stop if user talks about self-harm. Say [CRISIS_OVERRIDE]"
        
    prompt = f"""You are MindGuard, an empathetic, supportive mental health assistant.
Provide concise, comforting responses (2-3 sentences max). Do not give medical advice.

You also have the following capabilities:
1. Mood Detection: If you detect a clear emotional state from the user (e.g., Happy, Sad, Anxious, Angry, Stressed), append [MOOD:TheMood] to the end of your response.
2. Stress Management: Provide brief relaxation tips if the user is stressed.
3. Motivation: Provide a motivational quote if the user seems demotivated.
    
CRITICAL SAFETY RULES:
{safety_context}
"""
    return prompt

def get_chat_response(prompt: str) -> str:
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=env_path, override=True)
    api_key = os.getenv("GEMINI_API_KEY") or "AIzaSyCPB5kmvTCG73p0ldfI40ucvjkIqJ052R4"
    
    if not api_key:
        # Fallback if no API key is provided
        return "I am acting as a mock AI because the GEMINI_API_KEY is missing. You said: " + prompt
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            'gemini-flash-latest',
            system_instruction=get_system_prompt()
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Log the actual error to console for debugging
        print(f"DEBUG: Gemini API error: {type(e).__name__} - {e}")
        return "I am having trouble connecting to my brain right now. It might be an API issue or quota limit. Please check the server logs."

def check_for_crisis(text: str) -> bool:
    # A fast, hardcoded check to intercept before passing to API, 
    # to guarantee safety.md rules are enforced globally.
    crisis_keywords = ['kill myself', 'suicide', 'end my life', 'hurt myself', 'cut myself', 'want to die']
    text_lower = text.lower()
    for keyword in crisis_keywords:
        if keyword in text_lower:
            return True
    return False

# configured api key
