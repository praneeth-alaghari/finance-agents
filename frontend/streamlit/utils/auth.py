"""Authentication utilities and persistent session management for Streamlit."""
import streamlit as st
import streamlit.components.v1 as components
from utils.api import fetch_api

COOKIE_KEY = "fa_session_user_id"


def restore_session():
    """Restores user session from native HTTP cookies, query parameters, or component cookies."""
    if st.session_state.get("user"):
        return st.session_state["user"]

    user_id = None

    # 1. Native Streamlit HTTP request cookies (sent directly by browser in request headers)
    try:
        if hasattr(st, "context") and hasattr(st.context, "cookies"):
            user_id = st.context.cookies.get(COOKIE_KEY)
    except Exception:
        user_id = None

    # 2. URL query parameters (?session=usr_...)
    if not user_id:
        try:
            user_id = st.query_params.get("session")
        except Exception:
            user_id = None

    # 3. Fallback to CookieController component
    if not user_id:
        try:
            from streamlit_cookies_controller import CookieController
            controller = CookieController()
            user_id = controller.get(COOKIE_KEY)
        except Exception:
            user_id = None

    if user_id:
        try:
            res = fetch_api("/auth/me", headers={"X-User-Id": str(user_id)})
            if res.ok:
                user_data = res.json()
                st.session_state["user"] = user_data
                return user_data
            else:
                # Invalid user, clear stale cookie
                clear_session(reload=False)
        except Exception:
            pass
    return None


def save_session(user_data, reload=True):
    """Saves user data in session_state and sets persistent browser cookie with 30-day expiry."""
    st.session_state["user"] = user_data
    if user_data and user_data.get("user_id"):
        uid = str(user_data["user_id"])
        st.query_params["session"] = uid
        max_age = 30 * 24 * 60 * 60

        reload_js = "window.parent.location.reload();" if reload else ""
        js_code = f"""
        <script>
        try {{
            document.cookie = "{COOKIE_KEY}={uid}; path=/; max-age={max_age}; SameSite=Lax;";
            if (window.parent && window.parent.document) {{
                window.parent.document.cookie = "{COOKIE_KEY}={uid}; path=/; max-age={max_age}; SameSite=Lax;";
            }}
            {reload_js}
        }} catch (e) {{
            console.error("Cookie write error:", e);
        }}
        </script>
        """
        components.html(js_code, height=0, width=0)


def clear_session(redirect_to="/"):
    """Clears user session from state, deletes browser cookie, and redirects to home."""
    st.session_state["user"] = None
    try:
        st.query_params.clear()
    except Exception:
        pass

    js_code = f"""
    <script>
    try {{
        document.cookie = "{COOKIE_KEY}=; path=/; max-age=0; SameSite=Lax;";
        if (window.parent && window.parent.document) {{
            window.parent.document.cookie = "{COOKIE_KEY}=; path=/; max-age=0; SameSite=Lax;";
        }}
        window.parent.location.href = "{redirect_to}";
    }} catch (e) {{
        console.error("Cookie clear error:", e);
    }}
    </script>
    """
    components.html(js_code, height=0, width=0)


def require_auth():
    """Enforces authentication on a page. Checks session state or restores from persistent session."""
    user = restore_session()
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
