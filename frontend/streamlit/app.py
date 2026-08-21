import os
import streamlit as st
import requests

# Docker service name URL by default, configurable via API_BASE_URL env var
API_BASE_URL = os.getenv("API_BASE_URL", "http://portfolio_research:8000/api/v1")
LOCAL_FALLBACK_URL = "http://localhost:8000/api/v1"

st.title("Finance Agents")

# Helper function to perform requests with automatic fallback (Docker service name -> localhost)
def fetch_api(path, method="GET", **kwargs):
    url = f"{API_BASE_URL}{path}"
    try:
        if method == "GET":
            return requests.get(url, timeout=3, **kwargs)
        elif method == "POST":
            return requests.post(url, timeout=5, **kwargs)
    except requests.exceptions.ConnectionError:
        # Fallback to localhost if Docker service name is unreachable (e.g. running locally outside container)
        if API_BASE_URL != LOCAL_FALLBACK_URL:
            fallback_url = f"{LOCAL_FALLBACK_URL}{path}"
            if method == "GET":
                return requests.get(fallback_url, timeout=3, **kwargs)
            elif method == "POST":
                return requests.post(fallback_url, timeout=5, **kwargs)
        raise

# 1. Simple button to fetch portfolio from FastAPI (port 8000)
if st.button("Get Portfolio"):
    try:
        response = fetch_api("/portfolio")
        st.write("Status Code:", response.status_code)
        st.json(response.json() if response.ok else {"error": response.text})
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to FastAPI (tried Docker service `portfolio_research:8000` and local `localhost:8000`). Please ensure the server is running.")

# 2. Simple file uploader to upload CSV to FastAPI (port 8000)
uploaded_file = st.file_uploader("Select Portfolio CSV", type=["csv"])

if uploaded_file and st.button("Upload"):
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
        response = fetch_api("/portfolio/upload", method="POST", files=files)
        st.write("Status Code:", response.status_code)
        st.json(response.json())
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to FastAPI (tried Docker service `portfolio_research:8000` and local `localhost:8000`). Please ensure the server is running.")
