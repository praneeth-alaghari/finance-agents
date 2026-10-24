from datetime import datetime, timezone
import pandas as pd
import requests
import streamlit as st
from utils.api import fetch_api
from utils.auth import clear_session, get_user_headers, require_auth


def get_factor_icon(name):
    lower = (name or "").lower()
    if any(k in lower for k in ["rate", "repo", "interest", "yield", "bond"]):
        return "🏦"
    if any(k in lower for k in ["inflation", "cpi", "price", "wpi"]):
        return "🏷️"
    if any(k in lower for k in ["growth", "gdp", "output", "capex", "production"]):
        return "📈"
    if any(k in lower for k in ["liquidity", "money", "credit", "cash", "flow"]):
        return "💧"
    if any(k in lower for k in ["policy", "fiscal", "tax", "budget", "gov", "regulatory"]):
        return "🏛️"
    if any(k in lower for k in ["currency", "fx", "forex", "rupee", "dollar", "exchange"]):
        return "💱"
    if any(k in lower for k in ["trade", "export", "import", "deficit"]):
        return "🚢"
    if any(k in lower for k in ["employment", "job", "wage", "labor"]):
        return "👥"
    return "📌"


st.set_page_config(page_title="Market Researcher", page_icon="🌐", layout="wide")

# Inverted White/Grey button for primary action
st.markdown(
    """
    <style>
    div.stButton > button[kind="primary"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D4D4D8 !important;
        color: #18181B !important;
        font-weight: 600;
        padding: 0.5rem 1.25rem;
        border-radius: 8px;
        transition: background-color 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #F4F4F5 !important;
        border-color: #A1A1AA !important;
        color: #09090B !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    }
    div.stButton > button[kind="primary"]:active {
        background-color: #E4E4E7 !important;
        border-color: #71717A !important;
        box-shadow: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 1. Enforce Authentication
current_user = require_auth()
username = current_user.get("username", "User")
user_headers = get_user_headers()

# 2. Header & Navigation
header_left, header_right = st.columns([4, 1])
with header_left:
    st.title("🌐 Market Researcher")
    st.caption(f"Autonomous Market & Sector Intelligence • Active User: **{username}**")
with header_right:
    nav_home, nav_logout = st.columns(2)
    with nav_home:
        st.write("")
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    with nav_logout:
        st.write("")
        if st.button("🚪 Logout", use_container_width=True):
            clear_session()

st.divider()

# 3. Sidebar (Informational Guide)
with st.sidebar:
    st.subheader("💡 Multi-Agent Pipeline")
    st.markdown(
        """
        - **MacroEconomicsAgent**: Synthesizes inflation, policy rates, GDP growth, and liquidity conditions.
        - **SectorRotationAgent**: Tracks sector momentum, relative strength, and rotational signals.
        - **MarketResearchOrchestrator**: Combines macro and sector signals into an end-to-end `MarketContext`.
        """
    )
    st.caption("Shared domain intelligence for portfolios and trading strategies.")

# 4. In-Page Configuration & Research Parameters
st.markdown("### ⚙️ Research Configuration")
region = st.selectbox(
    "🌍 Target Economy / Region",
    options=["INDIA", "US", "EUROPE", "GLOBAL", "EMERGING MARKETS"],
    index=0,
    help="Select the macroeconomic region to analyze.",
)

st.write("")
run_orchestrator = st.button("🚀 Run Full Market Research", type="primary", use_container_width=False)

# 5. Execute Multi-Agent Pipeline with Real-Time Status Logging
if run_orchestrator:
    payload = {"region": region}
    with st.status(f"🚀 Running Full Market Research for {region}...", expanded=True) as status:
        try:
            # Step 1: Macroeconomics Agent
            status.write("🌐 **MacroEconomicsAgent** is fetching Macro economics data (inflation, policy rates, growth, liquidity)...")
            res_macro = fetch_api("/market/macro", method="POST", json=payload, headers=user_headers, timeout=90)
            if not res_macro.ok:
                raise RuntimeError(f"MacroEconomicsAgent failed ({res_macro.status_code}): {res_macro.text}")
            macro_data = res_macro.json()
            status.write("✅ **MacroEconomicsAgent**: Macro factors successfully analyzed.")

            # Step 2: Sector Economics / Rotation Agent
            status.write("🔄 **SectorEconomicsAgent** is fetching Sectors and evaluating rotation signals & relative strength...")
            res_sector = fetch_api("/market/sector", method="POST", json=payload, headers=user_headers, timeout=90)
            if not res_sector.ok:
                raise RuntimeError(f"SectorRotationAgent failed ({res_sector.status_code}): {res_sector.text}")
            sector_data = res_sector.json()
            status.write("✅ **SectorEconomicsAgent**: Sector trends and relative strength computed.")

            # Step 3: Orchestrator Synthesis
            status.write("⚡ **MarketResearchOrchestrator** is collating data and assembling unified MarketContext...")
            macro_summary = macro_data.get("summary", "").strip()
            sector_summary = sector_data.get("summary", "").strip()
            combined_summary = f"{macro_summary}\n\n{sector_summary}".strip()

            orchestrated_data = {
                "market_summary": combined_summary,
                "macro_factors": macro_data.get("macro_factors", []),
                "sector_trends": sector_data.get("sector_trends", []),
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }

            st.session_state["market_research_result"] = {
                "type": "orchestrator",
                "data": orchestrated_data,
            }
            status.update(label=f"✅ Market Research for {region} completed successfully!", state="complete", expanded=False)
            st.success(f"✅ Market research for {region} completed successfully!")

        except requests.exceptions.ReadTimeout:
            status.update(label="⏳ Execution timed out", state="error", expanded=True)
            st.error("⏳ AI agent took longer than expected to respond. Please try again.")
        except requests.exceptions.ConnectionError:
            status.update(label="❌ Connection failed", state="error", expanded=True)
            st.error("❌ Could not connect to the Backend API service.")
        except Exception as exc:
            status.update(label="❌ Execution failed", state="error", expanded=True)
            st.error(f"❌ Execution failed: {exc}")

# 6. Render Results
results = st.session_state.get("market_research_result")

if results:
    st.divider()
    res_type = results["type"]
    data = results["data"]

    # Executive Market Summary Card
    summary_text = data.get("market_summary") or data.get("summary") or "No narrative summary provided."
    with st.container(border=True):
        st.subheader("📋 Executive Market Summary")
        st.markdown(summary_text)
        if data.get("generated_at"):
            st.caption(f"Generated at: `{data['generated_at']}` UTC")

    # Tabs for detailed intelligence
    tab_macro, tab_sector, tab_raw = st.tabs([
        "🌐 Macroeconomic Factors",
        "🔄 Sector Rotation & Momentum",
        "🔍 Raw Context / JSON",
    ])

    with tab_macro:
        macro_factors = data.get("macro_factors", [])
        if macro_factors:
            st.subheader("Key Macro Factors")
            
            # Responsive 2-column card grid
            grid_cols = st.columns(2)
            for idx, factor in enumerate(macro_factors):
                name = factor.get("name", f"Factor {idx + 1}")
                val = factor.get("value")
                desc = factor.get("summary", "")
                icon = get_factor_icon(name)
                
                with grid_cols[idx % 2]:
                    with st.container(border=True):
                        st.markdown(f"**{icon} {name}**")
                        if val is not None and str(val).strip():
                            st.markdown(
                                f"<div style='font-size: 0.85rem; font-style: italic; color: #888888; margin-top: -6px; margin-bottom: 8px;'>"
                                f"Indicator Value: <b>{val}</b></div>",
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                "<div style='font-size: 0.82rem; font-style: italic; color: #999999; margin-top: -6px; margin-bottom: 8px;'>"
                                "Indicator Value: <i>Qualitative indicator</i></div>",
                                unsafe_allow_html=True,
                            )
                        st.markdown(desc or "*No detailed summary provided.*")
        else:
            st.warning("No macro factors parsed from the agent response.")

    with tab_sector:
        sector_trends = data.get("sector_trends", [])
        if sector_trends:
            st.subheader("Sector Trends & Momentum")
            df_sectors = pd.DataFrame(sector_trends)
            if not df_sectors.empty:
                display_df = df_sectors.rename(
                    columns={"name": "Sector", "summary": "Analysis & Outlook"}
                )
                cols_to_display = [c for c in ["Sector", "Analysis & Outlook"] if c in display_df.columns]
                st.dataframe(
                    display_df[cols_to_display],
                    use_container_width=True,
                    hide_index=True,
                )
        else:
            st.warning("No sector trends parsed from the agent response.")

    with tab_raw:
        st.subheader("Raw Output Payload")
        st.json(data)
