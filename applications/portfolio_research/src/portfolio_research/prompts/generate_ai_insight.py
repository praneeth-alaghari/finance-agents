"""Prompt templates for generate_ai_insight."""

SYSTEM_INSTRUCTION = """You are an elite institutional portfolio manager and quantitative risk analyst. Provide insightful, concise, and structured financial portfolio assessments."""

USER_PROMPT_TEMPLATE = """User Portfolio Summary (Total Invested: ${total_invested:,.2f}):
{holdings_summary}

Please provide a clear and professional financial analysis of this portfolio covering:
1. Diversification & Concentration Risk
2. Key Strengths & Potential Exposures
3. Strategic Recommendations for Rebalancing or Risk Management"""
