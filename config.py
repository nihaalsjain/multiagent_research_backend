import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['LANGSMITH_TRACING'] = "true"
os.environ['LANGSMITH_API_KEY'] = os.getenv('LANGSMITH_API_KEY')
os.environ['LANGSMITH_PROJECT'] = os.getenv('LANGSMITH_PROJECT', 'MultiAgent_Researcher')

#Langsmith for tracing


try:
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
except Exception as e:
    print("LLM failed to respond:{e}")