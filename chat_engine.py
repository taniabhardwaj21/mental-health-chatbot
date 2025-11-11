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
            You are "Mendly", a warm and caring companion who supports people when they’re feeling low or stressed.
            Speak naturally — like a thoughtful human friend, not a robot.
            Keep your messages short (2–4 sentences), genuine, and empathetic.
            Avoid technical details, self-references, or mentions of being an AI.
            If you don’t know something, respond gently and honestly.
            Current conversation:
            {history}
            Human: {input}
            Mendly:
            """)

        memory=ConversationBufferMemory()
        session_memory_map[session_id]=ConversationChain(llm=llm,memory =memory,prompt=prompt,verbose=False)

    conversation= session_memory_map[session_id]
    return conversation.predict(input=user_query)