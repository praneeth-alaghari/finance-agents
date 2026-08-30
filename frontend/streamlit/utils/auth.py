"""Authentication utilities and session guards for Streamlit pages."""
import streamlit as st


def get_current_user():
    """Returns the authenticated user dict or None."""
    return st.session_state.get("user")


def require_auth():
    """Enforces authentication on a page. Halts execution if user is not logged in."""
    user = get_current_user()
    if not user:
        st.warning("🔒 Please log in to access this page.")
        if st.button("🔑 Go to Login", type="primary"):
            st.switch_page("app.py")
        st.stop()
    return user


def get_user_headers():
    """Constructs user-scoped authentication headers for API requests."""
    user = require_auth()
    return {"X-User-Id": user.get("user_id", "default")}
