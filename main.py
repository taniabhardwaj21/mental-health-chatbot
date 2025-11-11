import os
from fastapi import FastAPI,Request
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import base64, cv2, numpy as np, torch
from models import ChatRequest
from chat_engine import get_response
from crisis import contains_crisis_keywords, get_crisis_message, SAFETY_MESSAGE
from logger import log_chat
# from doc_engine import query_documents

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

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
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
    current_emotion = result[0]['dominant_emotion']
    return {"emotion": current_emotion}

# @app.post("/doc-chat")
# def chat_with_documents(request: ChatRequest):
#     response = query_documents(request.query)
#     return {"response": response}
