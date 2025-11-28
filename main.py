import os
from fastapi import FastAPI,Request
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from emotion_model.inference import load_model, predict_from_bytes
import base64
from models import ChatRequest
from chat_engine import get_response
from crisis import contains_crisis_keywords, get_crisis_message, SAFETY_MESSAGE
from logger import log_chat

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Load emotion model
model, device = load_model()

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# global vars
current_emotion = "neutral" 


@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Mental Health Bot"}

@app.post("/chat")
def chat_with_memory(request: ChatRequest):
    session_id = request.session_id
    user_query = request.query

    # Crisis keyword check
    if contains_crisis_keywords(user_query):
        crisis_message = SAFETY_MESSAGE if 'SAFETY_MESSAGE' in globals() else get_crisis_message()
        log_chat(session_id, user_query, crisis_message, is_crisis=True)
        return {"response": crisis_message}

    # Normal LLM response
    response = get_response(session_id, user_query)
    log_chat(session_id, user_query, response, is_crisis=False)
    return {"response": response}

    
@app.post("/emotion")
async def emotion(request: Request):
    global current_emotion
    data = await request.json()
    frame_data = data['frame'].split(',')[1]
    img_bytes = base64.b64decode(frame_data)

    emotions = predict_from_bytes(model, device, img_bytes)

    if 'sad' in emotions:
        emotions['sad'] *= 0.5
    
    if 'happy' in emotions:
        emotions['happy'] *= 1.2

    for emo, val in emotions.items():
        print(f"{emo:10} : {val:.4f}")

    current_emotion = max(emotions, key=emotions.get)
    return {"emotion": current_emotion}
