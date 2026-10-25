import os
from ddgs import DDGS
from langchain_core.tools import Tool


def _search(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(str(query), max_results=3))
        if not results:
            return f"No results found for query '{query}'."
        return "\n".join(f"{r.get('title', '')}: {r.get('body', '')}" for r in results)
    except Exception as e:
        return f"Search note: could not fetch live results for query '{query}': {e}. Use established baseline knowledge."


def get_web_search_tool(provider=None):
    return Tool(
        name="web_search",
        func=_search,
        description="Search the web for financial news, macroeconomic data, and sector performance.",
    )
