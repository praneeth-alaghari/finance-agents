import os
import requests
import streamlit as st

# Configure Landing Page
st.set_page_config(
    page_title="Finance Agents Hub",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.api import fetch_api

# Initialize session state for user authentication
if "user" not in st.session_state:
    st.session_state["user"] = None

# ==========================================
# 1. UNAUTHENTICATED STATE: AUTHENTICATION GATE
# ==========================================
if not st.session_state["user"]:
    st.title("💼 Finance Agents")
    st.markdown("### Secure Financial Intelligence & Multi-Agent Platform")
    st.caption("Please log in to your account or create a new account to continue.")

    st.divider()

    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        auth_tab_login, auth_tab_signup = st.tabs(["🔐 Log In", "📝 Sign Up"])

        # TAB 1: LOGIN
        with auth_tab_login:
            st.subheader("Welcome Back")
            with st.form("login_form", clear_on_submit=False):
                login_identifier = st.text_input("Username or Email", placeholder="e.g. praneeth or user@example.com")
                login_password = st.text_input("Password", type="password", placeholder="Enter your password")
                login_submitted = st.form_submit_button("Log In", type="primary", use_container_width=True)

            if login_submitted:
                if not login_identifier or not login_password:
                    st.warning("Please fill in both username/email and password.")
                else:
                    try:
                        with st.spinner("Authenticating..."):
                            payload = {"username": login_identifier, "password": login_password}
                            response = fetch_api("/auth/login", method="POST", json=payload)
                            if response.ok:
                                user_data = response.json()
                                st.session_state["user"] = user_data
                                st.success(f"Welcome back, {user_data.get('username')}!")
                                st.rerun()
                            else:
                                err_detail = response.json().get("detail", "Invalid username or password.")
                                st.error(f"❌ {err_detail}")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend API service is unreachable. Please ensure the API container is running.")

        # TAB 2: SIGN UP
        with auth_tab_signup:
            st.subheader("Create an Account")
            with st.form("signup_form", clear_on_submit=False):
                signup_username = st.text_input("Username", placeholder="e.g. praneeth")
                signup_email = st.text_input("Email", placeholder="e.g. praneeth@example.com")
                signup_password = st.text_input("Password", type="password", placeholder="Minimum 6 characters")
                signup_confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
                signup_submitted = st.form_submit_button("Sign Up", type="primary", use_container_width=True)

            if signup_submitted:
                if not signup_username or not signup_email or not signup_password:
                    st.warning("Please complete all required fields.")
                elif signup_password != signup_confirm:
                    st.error("Passwords do not match. Please check and try again.")
                elif len(signup_password) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    try:
                        with st.spinner("Creating account..."):
                            payload = {
                                "username": signup_username.strip(),
                                "email": signup_email.strip(),
                                "password": signup_password,
                            }
                            response = fetch_api("/auth/signup", method="POST", json=payload)
                            if response.ok:
                                created_user = response.json()
                                # Auto-login newly registered user
                                st.session_state["user"] = created_user
                                st.success("🎉 Account created successfully! Logging you in...")
                                st.rerun()
                            else:
                                err_detail = response.json().get("detail", "Signup failed.")
                                st.error(f"❌ {err_detail}")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend API service is unreachable. Please ensure the API container is running.")

# ==========================================
# 2. AUTHENTICATED STATE: FINANCE AGENTS HUB
# ==========================================
else:
    current_user = st.session_state["user"]
    username = current_user.get("username", "User")
    email = current_user.get("email", "")

    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.title(f"Welcome, {username}! 👋")
        st.caption(f"Signed in as `{email}` • Session active")
    with header_col2:
        st.write("")
        st.write("")
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state["user"] = None
            st.rerun()

    st.divider()

    st.markdown("### Applications & Intelligence Suites")
    st.markdown("Select an application below or use the sidebar navigation:")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("📈 Portfolio Researcher")
            st.markdown(
                """
                - **Personalized Portfolio**: Manage your dedicated holdings.
                - **Holdings Analysis**: Track allocations, quantities, and weights.
                - **AI Research Agents**: Autonomous financial agents researching market insights.
                """
            )
            if st.button("🚀 Launch Portfolio Researcher", type="primary", use_container_width=True):
                st.switch_page("pages/1_Portfolio_Researcher.py")

    with col2:
        with st.container(border=True):
            st.subheader("🤖 Algorithmic Trading Bot")
            st.markdown(
                """
                - **Strategy Execution**: Real-time signal generation and automated execution.
                - **Backtesting Suite**: Evaluate risk, Sharpe ratios, and drawdowns.
                - **Market Monitoring**: Live order books and algorithmic safety checks.
                """
            )
            st.button("⚙️ Coming Soon", disabled=True, use_container_width=True)

    st.divider()
    st.caption("Finance Agents Monorepo • Clean Architecture Micro-Frontend")
