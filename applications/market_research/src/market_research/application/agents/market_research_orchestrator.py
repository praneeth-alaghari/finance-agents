from common.models import MarketContext
from market_research.application.agents.macro_economics_agent import MacroEconomicsAgent
from market_research.application.agents.sector_rotation_agent import SectorRotationAgent


class MarketResearchOrchestrator:
    """Coordinates market intelligence agents into a single reusable market context."""

    def __init__(self, llm_client=None):
        self._macro_agent = MacroEconomicsAgent(llm_client=llm_client)
        self._sector_agent = SectorRotationAgent(llm_client=llm_client)

    def run(self, market_summary="", region="US", sector_focus=None):
        macro_result = self._macro_agent.run(market_summary=market_summary, region=region)
        sector_result = self._sector_agent.run(market_summary=market_summary, sector_focus=sector_focus)

        return MarketContext(
            market_summary=f"{macro_result.get('summary', '')} {sector_result.get('summary', '')}".strip(),
            macro_factors=macro_result.get("macro_factors", []),
            sector_trends=sector_result.get("sector_trends", []),
            company_earnings=[],
        )
