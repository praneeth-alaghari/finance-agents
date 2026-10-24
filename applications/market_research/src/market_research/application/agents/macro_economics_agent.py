from ai_core import get_llm_client
from common.models import MacroSnapshot, MarketContext, SectorTrend


class MacroEconomicsAgent:
    """Summarizes macroeconomic risks and opportunities for a market context."""

    def __init__(self, llm_client=None):
        self._llm_client = llm_client or get_llm_client()

    def run(self, market_summary="", region="US"):
        prompt = f"""You are a macroeconomic research analyst.

Provide a concise market-facing summary for the {region} economy.
Focus on inflation, rates, growth, liquidity, and policy conditions.

Reference context:
{market_summary}

Return a JSON object with:
- summary: one paragraph
- macro_factors: a list of objects with name, value, summary
"""

        raw_response = self._llm_client.generate(
            prompt=prompt,
            system_instruction="You are an expert macro strategist. Return structured, practical market commentary.",
        )

        try:
            import json
            payload = json.loads(raw_response)
        except Exception:
            payload = {
                "summary": raw_response,
                "macro_factors": [],
            }

        macro_factors = []
        for item in payload.get("macro_factors", []):
            macro_factors.append(
                MacroSnapshot(
                    name=item.get("name", "macro_factor"),
                    value=item.get("value"),
                    summary=item.get("summary", ""),
                )
            )

        return {
            "summary": payload.get("summary", raw_response),
            "macro_factors": macro_factors,
        }
