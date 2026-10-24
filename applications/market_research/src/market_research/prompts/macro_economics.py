"""Prompt templates for MacroEconomicsAgent."""

SYSTEM_INSTRUCTION = (
    "You are an expert macro strategist with access to web search. "
    "Always search for the latest data before forming conclusions. "
    "Return structured, practical, data-grounded market commentary."
)

# Used as the 'input' task string sent to the AgentExecutor.
# The agent will decide how many searches to run before composing the final answer.
MACRO_ANALYSIS_TASK_TEMPLATE = """Research the current macroeconomic conditions for {region}.

Search for the latest data on:
- Inflation rate and CPI trend
- Central bank interest rate decision and policy stance
- GDP growth rate (recent quarter or year)
- Currency performance and foreign exchange reserves
- Government fiscal policy and deficit/surplus
- Global risk factors affecting {region} (e.g. commodity prices, global rates)

After gathering real data from your searches, compose a final answer as a valid JSON object:
{{
  "summary": "2-3 crisp bullet points summarising the macro picture (single string)",
  "macro_factors": [
    {{"name": "Inflation", "value": "actual figure or status", "summary": "1-line context"}},
    {{"name": "Interest Rates", "value": "actual figure or status", "summary": "1-line context"}},
    {{"name": "GDP Growth", "value": "actual figure or status", "summary": "1-line context"}},
    {{"name": "Currency", "value": "actual figure or status", "summary": "1-line context"}},
    {{"name": "Fiscal Policy", "value": "actual figure or status", "summary": "1-line context"}}
  ]
}}

Return ONLY the JSON object as your Final Answer. No markdown fences.
"""

# Alias for backward compatibility
MACRO_ANALYSIS_PROMPT_TEMPLATE = MACRO_ANALYSIS_TASK_TEMPLATE
