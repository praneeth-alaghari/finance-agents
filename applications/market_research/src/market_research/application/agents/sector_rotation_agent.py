from ai_core import get_llm_client
from common.models import SectorTrend


class SectorRotationAgent:
    """Identifies which sectors are leading or lagging relative to the broader market."""

    def __init__(self, llm_client=None):
        self._llm_client = llm_client or get_llm_client()

    def run(self, market_summary="", sector_focus=None):
        focus = sector_focus or "broad equity market"
        prompt = f"""You are a sector rotation analyst.

Review the market narrative and identify which sectors are leading, lagging, and rotating.
Focus: {focus}

Reference context:
{market_summary}

Return a JSON object with:
- summary: one paragraph
- sector_trends: a list of objects with name, strength, summary
"""

        raw_response = self._llm_client.generate(
            prompt=prompt,
            system_instruction="You are an expert sector strategist. Translate market conditions into sector-level insights.",
        )

        try:
            import json
            payload = json.loads(raw_response)
        except Exception:
            payload = {
                "summary": raw_response,
                "sector_trends": [],
            }

        sector_trends = []
        for item in payload.get("sector_trends", []):
            sector_trends.append(
                SectorTrend(
                    name=item.get("name", "sector"),
                    strength=float(item.get("strength", 0.0) or 0.0),
                    summary=item.get("summary", ""),
                )
            )

        return {
            "summary": payload.get("summary", raw_response),
            "sector_trends": sector_trends,
        }
