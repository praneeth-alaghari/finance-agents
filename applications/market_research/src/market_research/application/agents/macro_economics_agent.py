import json
import re
from ai_core import get_llm_client
from ai_core.tools import get_web_search_tool
from common.models import MacroSnapshot
from market_research.prompts.macro_economics import (
    MACRO_ANALYSIS_TASK_TEMPLATE,
    SYSTEM_INSTRUCTION,
)


class MacroEconomicsAgent:
    """
    A real AI agent that researches macroeconomic conditions using web search.

    Uses a ReAct-style AgentExecutor loop:
      Thought → web_search → Observation → Thought → ... → Final Answer (JSON)

    Unlike a simple LLM chain (generate → parse), this agent autonomously
    decides what to search for, reads live results, and synthesises a
    data-grounded macro analysis.
    """

    def __init__(self, llm_client=None):
        self._llm_client = llm_client or get_llm_client()
        self._tools = [get_web_search_tool()]

    def run(self, region="INDIA", *args, **kwargs):
        task = MACRO_ANALYSIS_TASK_TEMPLATE.format(region=region)

        executor = self._llm_client.get_agent_executor(
            tools=self._tools,
            system_instruction=SYSTEM_INSTRUCTION,
            verbose=True,
        )

        result = executor.invoke({"input": task})
        raw_output = result.get("output", "")

        return self._parse_output(raw_output)

    def _parse_output(self, raw_output):
        """Extracts and validates the JSON payload from the agent's Final Answer."""
        try:
            # Strip markdown fences if the LLM wrapped the JSON anyway
            cleaned = re.sub(r"```(?:json)?", "", raw_output).strip().rstrip("```").strip()
            payload = json.loads(cleaned)
        except Exception:
            # Fallback: treat entire output as the summary, no structured factors
            payload = {
                "summary": raw_output,
                "macro_factors": [],
            }

        macro_factors = [
            MacroSnapshot(
                name=item.get("name", "macro_factor"),
                value=item.get("value"),
                summary=item.get("summary", ""),
            )
            for item in payload.get("macro_factors", [])
        ]

        raw_summary = payload.get("summary", raw_output)
        if isinstance(raw_summary, list):
            summary = "\n".join(f"• {str(s).lstrip('•- ')}" for s in raw_summary if s)
        else:
            summary = str(raw_summary or "").strip()

        return {
            "summary": summary,
            "macro_factors": macro_factors,
        }
