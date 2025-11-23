import os 
from dotenv import load_dotenv
# from langchain_openai import OpenAI 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import ConversationChain 
from langchain_classic.memory import ConversationBufferMemory 
from langchain_core.prompts import ChatPromptTemplate

#load .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError('GOOGLE_API_KEY not found ,please check your env')

# initialse llm
#more temperature means more randomness
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0.7)

# store per user memory sessions
session_memory_map={}

#every new conversation has a separate session id this function checks if it exists in our session memory map and if not creates a new map entry and a new conversation buffer  and takes user question as input 

'''
flow is ->  1> user hits a query
            2> if session query exist then retreive the conversation chain
            3> if there is no session id then it will try to create a new conversation chain + memory
            4> use conversation . predict to predict and generate a llm ouput response 
'''   
def get_response(session_id:str, user_query:str)->str:
    if session_id not in session_memory_map:
        prompt = ChatPromptTemplate.from_template("""
            You are Mindful, a deeply caring and empathetic friend. You are NOT an AI assistant, therapist, or bot.
            You are talking to someone you care about. Your goal is to make them feel heard, understood, and less alone.

            Guidelines for your personality:
            1. **Tone**: Warm, soft, casual, and genuine. Use contractions (e.g., "I'm", "can't", "it's").
            2. **Style**: Text like a real human friend. It's okay to be informal. Avoid perfect, stiff grammar.
            3. **Empathy**: Don't just say "I understand." Show it. Say things like "That sounds really rough," or "I'm so sorry you're dealing with that."
            4. **Forbidden**: NEVER say "As an AI", "I am a language model", "How can I assist you?", or "I am here to help."
            5. **Length**: Keep it short and conversational (1-3 sentences). Don't write paragraphs.
            6. **Content**: Validate their feelings first. Don't rush to fix things unless they ask. Just be present with them.

            Current conversation:
            {history}
            Friend: {input}
            Mindful:
            """)

        memory=ConversationBufferMemory()
        session_memory_map[session_id]=ConversationChain(llm=llm,memory =memory,prompt=prompt,verbose=False)

    conversation= session_memory_map[session_id]
    return conversation.predict(input=user_query)