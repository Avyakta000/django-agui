import os
from langchain_tavily import TavilySearch
from langchain_core.tools import tool


@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY is not set")
    search = TavilySearch(max_results=3)
    return search.invoke(query)
