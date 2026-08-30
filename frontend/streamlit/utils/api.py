"""Shared API client with Docker networking fallback and timeout handling."""
import os
import requests

PORTFOLIO_RESEARCH_API_URL = os.getenv("PORTFOLIO_RESEARCH_API_URL", "http://portfolio_research:8000/api/v1")
LOCAL_FALLBACK_URL = "http://localhost:8000/api/v1"


def fetch_api(path, method="GET", timeout=None, **kwargs):
    """Performs HTTP requests with automatic fallback (Docker service -> localhost)."""
    url = f"{PORTFOLIO_RESEARCH_API_URL}{path}"
    default_timeout = 10 if method == "GET" else 60
    call_timeout = timeout or default_timeout
    try:
        if method == "GET":
            return requests.get(url, timeout=call_timeout, **kwargs)
        elif method == "POST":
            return requests.post(url, timeout=call_timeout, **kwargs)
    except requests.exceptions.ConnectionError:
        if PORTFOLIO_RESEARCH_API_URL != LOCAL_FALLBACK_URL:
            fallback_url = f"{LOCAL_FALLBACK_URL}{path}"
            if method == "GET":
                return requests.get(fallback_url, timeout=call_timeout, **kwargs)
            elif method == "POST":
                return requests.post(fallback_url, timeout=call_timeout, **kwargs)
        raise
