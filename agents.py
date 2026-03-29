
from state import ResearchState
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities import WikipediaAPIWrapper
from config import llm
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')


#node 1 planner

def research_planner(state:ResearchState):
    """This is to plan the research for the given query"""
    topic = state["topic"]

    prompt = f"""You are a research planner, given the topic below, generate:

    1. Web search - extract concise summary from credible web sources, factual data,latest trends.
    2. Wiki search - extract the info from wiki sources.

    Return only 2 queries clearly labelled.

    Topic:{topic}
"""
    response = llm.invoke(prompt)
    return {"research_plan":response.content}

#node 2 web_serch

def web_searcher(state:ResearchState):
    """This is to search the web and extract the info from web"""
    topic = state["topic"]
    plan = state["research_plan"]

    try:
        tavily_search = TavilySearchResults(max_results=3)
    except Exception as e:
        print("Tavily API didn't respond:{e}")
        tavily_search = "No results from Tavily"

    web_results = tavily_search.invoke(topic)

    prompt=f"""Summarize the below web results, for the given {topic}, keep 3 to 4
    bullet points, based on the given Research plan. 
    Research plan:{plan}
    Web Results:{web_results}
    """
    response = llm.invoke(prompt)
    return {"web_search":response.content}

#node 3 wiki search
def wiki_searcher(state:ResearchState):
    """This is to search the topic from wiki"""
    topic = state["topic"]
    plan = state["research_plan"]

    try:
        wiki_search = WikipediaAPIWrapper(top_k_results=3,doc_content_chars_max=2000)
    except Exception as e:
        print("Wiki search API failed: {e}")
        wiki_search = "No results from wikipedia"

    wiki_results = wiki_search.run(topic)

    prompt = f"""Summarize the below contents from wiki results for the given {topic},
    based on the given Research plan
    Research plan:{plan}
    Wiki Results: {wiki_results}
    """
    response = llm.invoke(prompt)
    return {"wiki_search":response.content}

#node 4 analyst

def analyst(state:ResearchState):
    """This is an analyst node to analyze the results from different sources"""
    topic = state["topic"]
    web_ser = state["web_search"]
    wiki_ser = state["wiki_search"]

    prompt = f"""You are a Senior Analyst.
              Summarize the key findings from all the sources for the {topic} and provide the following points:
              Sources:
              1. Web results:{web_ser}
              2. Wiki resukts:{wiki_ser}

              Tasks:
              1. From the above sources, Identify the key trends or patterns,compare the key findings between sources.
              2. Present the sales performance data to highlight the crucial insights effectively.
              3. Identify the key competitors and the market share and the revenue model.
              4. Identify bottlenecks and inefficiencies and provide the data. 
             """
    response = llm.invoke(prompt)
    return {"analysis":response.content}

def report_generator(state:ResearchState):
    """This is a report generation node"""
    topic  = state["topic"]
    analysis = state["analysis"]

    prompt= f"""Generate a detailed report for the analysis given below for the {topic}:
          
            Analysis:{analysis}

            Based on the given analysis, generate a detailed report in below format:

            **Title :** Research on {topic}
            **Executive Summary :** A brief summary of analysis provided.
            **Key Findings:** Mention the findings from the analysis.
            **Comparisons:** If this is necessary then provide a comparison.
            **Conclusion** Final conclusion
           """
    response = llm.invoke(prompt)
    return {"final_report":response.content}