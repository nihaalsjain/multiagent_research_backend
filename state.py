import os
from dotenv import load_dotenv
from typing_extensions import TypedDict

class ResearchState(TypedDict):
    topic:str  #receive input queries
    research_plan : str #output of planner
    web_search : str #output of web search
    wiki_search : str #output of wiki search
    analysis : str #output of analyst node
    final_report: str #output of report generation node