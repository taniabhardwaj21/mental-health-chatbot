#used to structure and parse ,validation incoming request data for fast api endpoint
from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    query: str