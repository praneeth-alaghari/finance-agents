import pandas as pd
import requests
import streamlit as st
from utils.api import fetch_api
from utils.auth import require_auth, get_user_headers

st.set_page_config(page_title="Portfolio Researcher", page_icon="📈", layout="wide")

# 1. Enforce Authentication
current_user = require_auth()
username = current_user.get("username", "User")
user_headers = get_user_headers()

# 2. Header & Navigation
header_left, header_right = st.columns([4, 1])
with header_left:
    st.title("📈 Portfolio Researcher")
    st.caption(f"Dedicated Portfolio for **{username}**")
with header_right:
    nav_home, nav_logout = st.columns(2)
    with nav_home:
        st.write("")
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    with nav_logout:
        st.write("")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["user"] = None
            st.switch_page("app.py")

st.divider()

# 3. Fetch Portfolio Automatically
portfolio_data = None
try:
    response = fetch_api("/portfolio", headers=user_headers)
    if response.ok:
        portfolio_data = response.json()
except requests.exceptions.ConnectionError:
    st.error("❌ Backend API service is unreachable. Please ensure the backend container is running.")

# 4. Display Portfolio Data (Tabulated) or Empty State
if portfolio_data and portfolio_data.get("holdings"):
    holdings = portfolio_data["holdings"]
    df = pd.DataFrame(holdings)
    df["total_cost"] = df["quantity"] * df["average_price"]

    # Summary Metrics
    total_invested = df["total_cost"].sum()
    m1, m2 = st.columns(2)
    m1.metric("Total Positions", len(df))
    m2.metric("Total Invested Capital", f"${total_invested:,.2f}")

    # Tabulated Holdings
    st.subheader("Your Holdings")
    table_df = df.rename(
        columns={
            "symbol": "Ticker",
            "quantity": "Quantity",
            "average_price": "Avg Price ($)",
            "total_cost": "Total Cost ($)",
        }
    )
    st.dataframe(
        table_df[["Ticker", "Quantity", "Avg Price ($)", "Total Cost ($)"]].style.format(
            {"Quantity": "{:,.2f}", "Avg Price ($)": "${:,.2f}", "Total Cost ($)": "${:,.2f}"}
        ),
        use_container_width=True,
        hide_index=True,
    )

    # Action: Get AI Insight
    st.write("")
    if st.button("🤖 Get AI Insight", type="primary"):
        try:
            with st.spinner("Analyzing portfolio with AI agent (reasoning models may take 15–30s)..."):
                insight_res = fetch_api("/portfolio/insights", method="POST", timeout=120, headers=user_headers)
                if insight_res.ok:
                    data = insight_res.json()
                    model_used = data.get("model", "AI Model")
                    st.success("✅ Portfolio Analysis Complete!")
                    st.caption(f"🧠 **Model Engine:** `{model_used}` • Powered by LangChain")
                    with st.expander(f"📊 AI Research & Risk Report ({model_used})", expanded=True):
                        st.markdown(data.get("insight", "No insight returned."))
                elif insight_res.status_code == 422:
                    st.warning(f"⚠️ {insight_res.json().get('detail', 'Validation error.')}")
                else:
                    st.error(f"Error {insight_res.status_code}: {insight_res.text}")
        except requests.exceptions.ReadTimeout:
            st.error("⏳ AI model took longer than 2 minutes to respond. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not reach backend service.")
else:
    st.info("ℹ️ You don't have any holdings uploaded yet. Upload a CSV file below to get started!")

# 5. Collapsible CSV Upload
st.divider()
with st.expander("📤 Upload / Replace Portfolio CSV", expanded=not bool(portfolio_data and portfolio_data.get("holdings"))):
    st.markdown("Upload a CSV file containing your stock tickers, quantities, and average prices.")
    uploaded_file = st.file_uploader("Select CSV file", type=["csv"])
    if uploaded_file and st.button("Save to Portfolio"):
        try:
            with st.spinner("Uploading and persisting portfolio..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                upload_res = fetch_api("/portfolio/upload", method="POST", files=files, headers=user_headers)
                if upload_res.ok:
                    st.success("🎉 Portfolio saved successfully!")
                    st.rerun()
                else:
                    st.error(f"Error {upload_res.status_code}: {upload_res.text}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to backend service.")
