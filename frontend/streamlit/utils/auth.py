import streamlit as st
from utils.api import fetch_api

COOKIE_KEY = "fa_session_user_id"


def restore_session():
    if st.session_state.get("logged_out"):
        return None

    if st.session_state.get("user"):
        return st.session_state["user"]

    user_id = None
    if hasattr(st, "context") and hasattr(st.context, "cookies"):
        user_id = st.context.cookies.get(COOKIE_KEY)

    if not user_id:
        try:
            user_id = st.query_params.get("session")
        except Exception:
            user_id = None

    if not user_id:
        try:
            from streamlit_cookies_controller import CookieController
            user_id = CookieController().get(COOKIE_KEY)
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
                clear_session()
        except Exception:
            pass
    return None


def save_session(user_data):
    st.session_state["user"] = user_data
    st.session_state["logged_out"] = False
    if user_data and user_data.get("user_id"):
        uid = str(user_data["user_id"])
        st.query_params["session"] = uid
        try:
            from streamlit_cookies_controller import CookieController
            CookieController().set(COOKIE_KEY, uid)
        except Exception:
            pass


def clear_session():
    st.session_state["user"] = None
    st.session_state["logged_out"] = True
    try:
        st.query_params.clear()
    except Exception:
        pass
    try:
        from streamlit_cookies_controller import CookieController
        CookieController().remove(COOKIE_KEY)
    except Exception:
        pass


def require_auth():
    user = restore_session()
    if not user:
        st.warning("🔒 Please log in to access this page.")
        if st.button("🔑 Go to Login", type="primary"):
            st.switch_page("app.py")
        st.stop()
    return user


def get_user_headers():
    user = require_auth()
    return {"X-User-Id": user.get("user_id", "default")}
