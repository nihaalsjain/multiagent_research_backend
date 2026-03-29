from langgraph.graph import START, END, StateGraph
from agents import (research_planner,
                    web_searcher,
                    wiki_searcher,
                    analyst,
                    report_generator)
from state import ResearchState

#graph construction

def build_graph():
    builder = StateGraph(ResearchState)

#nodes

    builder.add_node("research_planner", research_planner)
    builder.add_node("web_searcher",web_searcher)
    builder.add_node("wiki_searcher", wiki_searcher)
    builder.add_node("analyst",analyst)
    builder.add_node("report_generator", report_generator)

#edges

    builder.add_edge(START,"research_planner")
    builder.add_edge("research_planner","web_searcher")
    builder.add_edge("research_planner","wiki_searcher")
    builder.add_edge("web_searcher","analyst")
    builder.add_edge("wiki_searcher","analyst")
    builder.add_edge("analyst","report_generator")
    builder.add_edge("report_generator",END)

    graph = builder.compile()
    return graph