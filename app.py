from fastapi import FastAPI
from pydantic import BaseModel
from graph import build_graph
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Multi-Agent API")

#for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"], # Allowed methods (GET, POST, etc.)
    allow_headers=["*"], # Allowed headers
)

graph = build_graph()

class ResearchRequest(BaseModel):
   topic:str
 

class ResearchResponse(BaseModel):
    topic:str
    research_plan : str 
    web_search : str 
    wiki_search : str 
    analysis : str 
    final_report: str

@app.post("/research", response_model=ResearchResponse)
def run_research(request:ResearchRequest):
   result=graph.invoke({"topic":request.topic})
   return ResearchResponse(topic = request.topic,
                           research_plan = result["research_plan"],
                           web_search = result["web_search"],
                           wiki_search = result["wiki_search"],
                           analysis = result["analysis"],
                           final_report = result["final_report"])

 
 