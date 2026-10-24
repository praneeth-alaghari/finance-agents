"""
Shared web search tools for Finance Agents.

Provides a factory function `get_web_search_tool()` that returns a LangChain-compatible
tool which agents can use for live internet research.

Currently active: DuckDuckGo (no API key required)
Future providers (stubbed): Tavily, SerpAPI
"""

import os
from dotenv import load_dotenv
from ddgs import DDGS
from langchain_core.tools import Tool

load_dotenv()

# ---------------------------------------------------------------------------
# Provider: DuckDuckGo (active — no API key needed)
# ---------------------------------------------------------------------------

def _safe_duckduckgo_search(query):
    """Executes DuckDuckGo search using ddgs directly for fast, reliable snippets."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(str(query), max_results=3))
        if not results:
            return f"No results found for query '{query}'."
        snippets = []
        for r in results:
            title = r.get("title", "")
            body = r.get("body", "")
            snippets.append(f"{title}: {body}")
        return "\n".join(snippets)
    except Exception as e:
        return f"Search note: could not fetch live results for query '{query}': {e}. Use your established baseline knowledge."


def _get_duckduckgo_tool():
    """Returns a LangChain DuckDuckGo search tool with error resilience."""
    return Tool(
        name="web_search",
        func=_safe_duckduckgo_search,
        description=(
            "Search the web for current financial news, macroeconomic data, "
            "central bank policy updates, inflation figures, GDP reports, "
            "and sector performance. Input should be a focused search query string."
        ),
    )


# ---------------------------------------------------------------------------
# Provider: Tavily (stub — enable when TAVILY_API_KEY is set)
# ---------------------------------------------------------------------------

def _get_tavily_tool():
    """Returns a LangChain Tavily search tool (requires TAVILY_API_KEY)."""
    # from langchain_community.tools.tavily_search import TavilySearchResults
    # api_key = os.getenv("TAVILY_API_KEY")
    # if not api_key:
    #     raise ValueError("TAVILY_API_KEY is not set in environment variables.")
    # return TavilySearchResults(
    #     name="web_search",
    #     max_results=5,
    #     description="Search for financial news and macroeconomic data using Tavily.",
    # )
    raise NotImplementedError("Tavily provider is not yet enabled. Set TAVILY_API_KEY and uncomment the implementation.")


# ---------------------------------------------------------------------------
# Provider: SerpAPI (stub — enable when SERPAPI_API_KEY is set)
# ---------------------------------------------------------------------------

def _get_serpapi_tool():
    """Returns a LangChain SerpAPI Google search tool (requires SERPAPI_API_KEY)."""
    # from langchain_community.utilities import SerpAPIWrapper
    # from langchain.tools import Tool
    # api_key = os.getenv("SERPAPI_API_KEY")
    # if not api_key:
    #     raise ValueError("SERPAPI_API_KEY is not set in environment variables.")
    # search = SerpAPIWrapper(serpapi_api_key=api_key)
    # return Tool(
    #     name="web_search",
    #     func=search.run,
    #     description="Search Google for financial data, market news, and economic indicators.",
    # )
    raise NotImplementedError("SerpAPI provider is not yet enabled. Set SERPAPI_API_KEY and uncomment the implementation.")


# ---------------------------------------------------------------------------
# Registry & Factory
# ---------------------------------------------------------------------------

_TOOL_REGISTRY = {
    "duckduckgo": _get_duckduckgo_tool,
    "tavily": _get_tavily_tool,
    "serpapi": _get_serpapi_tool,
}


def get_web_search_tool(provider=None):
    """Factory function that returns a configured LangChain web search tool.

    Reads WEB_SEARCH_PROVIDER from environment (default: 'duckduckgo').
    Agents import this and pass the returned tool into their AgentExecutor.

    Usage:
        from ai_core.tools import get_web_search_tool
        tool = get_web_search_tool()                   # uses env default
        tool = get_web_search_tool(provider="tavily")  # explicit override
    """
    provider_name = (provider or os.getenv("WEB_SEARCH_PROVIDER", "duckduckgo")).lower()

    factory_fn = _TOOL_REGISTRY.get(provider_name)
    if not factory_fn:
        available = ", ".join(_TOOL_REGISTRY.keys())
        raise ValueError(
            f"Unsupported web search provider: '{provider_name}'. "
            f"Available providers: {available}"
        )

    return factory_fn()
