import json
from ai_core import get_llm_client
from common.models import SectorTrend
from market_research.prompts.sector_rotation import (
    SECTOR_ROTATION_PROMPT_TEMPLATE,
    SYSTEM_INSTRUCTION,
)


class SectorRotationAgent:
    """Identifies which sectors are leading or lagging relative to the broader market."""

    def __init__(self, llm_client=None):
        self._llm_client = llm_client or get_llm_client()

    def run(self, *args, **kwargs):
        raw_response = self._llm_client.generate(
            prompt=SECTOR_ROTATION_PROMPT_TEMPLATE,
            system_instruction=SYSTEM_INSTRUCTION,
        )

        try:
            payload = json.loads(raw_response)
        except Exception:
            payload = {
                "summary": raw_response,
                "sector_trends": [],
            }

        sector_trends = [
            SectorTrend(
                name=item.get("name", "sector"),
                summary=item.get("summary", ""),
            )
            for item in payload.get("sector_trends", [])
        ]

        raw_summary = payload.get("summary", raw_response)
        if isinstance(raw_summary, list):
            summary = "\n".join(f"• {str(item).lstrip('•- ')}" for item in raw_summary if item)
        else:
            summary = str(raw_summary or "").strip()

        return {
            "summary": summary,
            "sector_trends": sector_trends,
        }
