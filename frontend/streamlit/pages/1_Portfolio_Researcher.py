import os
import requests
import streamlit as st

# Configure Page
st.set_page_config(page_title="Portfolio Researcher", page_icon="📈", layout="wide")

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://portfolio_research:8000/api/v1")
LOCAL_FALLBACK_URL = "http://localhost:8000/api/v1"


def fetch_api(path, method="GET", **kwargs):
    """Helper function to perform requests with automatic fallback (Docker service -> localhost)."""
    url = f"{API_BASE_URL}{path}"
    try:
        if method == "GET":
            return requests.get(url, timeout=5, **kwargs)
        elif method == "POST":
            return requests.post(url, timeout=10, **kwargs)
    except requests.exceptions.ConnectionError:
        if API_BASE_URL != LOCAL_FALLBACK_URL:
            fallback_url = f"{LOCAL_FALLBACK_URL}{path}"
            if method == "GET":
                return requests.get(fallback_url, timeout=5, **kwargs)
            elif method == "POST":
                return requests.post(fallback_url, timeout=10, **kwargs)
        raise


# ==========================================
# AUTHENTICATION GATE
# ==========================================
current_user = st.session_state.get("user")

if not current_user:
    st.warning("🔒 You must be logged in to access the Portfolio Researcher.")
    st.info("Please log in or create an account on the main page.")
    if st.button("🔑 Go to Login", type="primary"):
        st.switch_page("app.py")
    st.stop()

# ==========================================
# AUTHENTICATED USER VIEW
# ==========================================
user_id = current_user.get("user_id")
username = current_user.get("username", "User")
user_headers = {"X-User-Id": user_id}

top_col1, top_col2, top_col3 = st.columns([3, 1, 1])
with top_col1:
    st.title("📈 Portfolio Researcher")
    st.caption(f"Authenticated as **{username}** (`{user_id}`) • Dedicated 1:1 Portfolio")
with top_col2:
    st.write("")
    if st.button("🏠 Home Hub", use_container_width=True):
        st.switch_page("app.py")
with top_col3:
    st.write("")
    if st.button("🚪 Log Out", use_container_width=True):
        st.session_state["user"] = None
        st.switch_page("app.py")

st.divider()

# Section 1: Fetch Portfolio
st.subheader("1. View Your Portfolio")
st.markdown("Retrieve your saved portfolio from MongoDB.")

if st.button("Get My Portfolio", type="primary"):
    try:
        with st.spinner("Fetching portfolio data..."):
            response = fetch_api("/portfolio", headers=user_headers)
            st.write("Status Code:", response.status_code)
            if response.ok:
                st.success("Portfolio retrieved successfully!")
                st.json(response.json())
            elif response.status_code == 404:
                st.info("ℹ️ You don't have a portfolio uploaded yet. Upload a CSV below to get started!")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Could not connect to FastAPI backend (tried `portfolio_research:8000` and `localhost:8000`). Please ensure the service is running."
        )

st.divider()

# Section 2: Upload Portfolio CSV
st.subheader("2. Upload & Save Portfolio CSV")
st.markdown("Upload a CSV file containing your stock tickers, quantities, and average prices.")

uploaded_file = st.file_uploader("Select Portfolio CSV", type=["csv"])

if uploaded_file and st.button("Upload CSV"):
    try:
        with st.spinner("Uploading and persisting portfolio CSV..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            response = fetch_api("/portfolio/upload", method="POST", files=files, headers=user_headers)
            st.write("Status Code:", response.status_code)
            if response.ok:
                st.success(f"🎉 Portfolio for user '{username}' saved successfully to MongoDB!")
                st.json(response.json())
            else:
                st.error(f"Error {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Could not connect to FastAPI backend (tried `portfolio_research:8000` and `localhost:8000`). Please ensure the service is running."
        )
