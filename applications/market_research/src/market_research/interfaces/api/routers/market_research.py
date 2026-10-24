from dataclasses import asdict
from fastapi import APIRouter, HTTPException
from market_research.application.agents.macro_economics_agent import MacroEconomicsAgent
from market_research.application.agents.sector_rotation_agent import SectorRotationAgent
from market_research.application.agents.market_research_orchestrator import MarketResearchOrchestrator
from market_research.interfaces.api.schemas.market_research import (
    MarketResearchRequest,
    MarketContextResponse,
    MacroAnalysisResponse,
    SectorAnalysisResponse,
)

router = APIRouter(prefix="/market", tags=["market_research"])


@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "market_research"}


@router.post("/orchestrate", response_model=MarketContextResponse)
def orchestrate_market_research(request: MarketResearchRequest):
    """Executes full market research workflow: macro + sector rotation -> MarketContext."""
    try:
        orchestrator = MarketResearchOrchestrator()
        context = orchestrator.run(region=request.region)
        return MarketContextResponse.model_validate(asdict(context))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Market research orchestration failed: {exc}")


@router.post("/macro", response_model=MacroAnalysisResponse)
def run_macro_analysis(request: MarketResearchRequest):
    """Executes MacroEconomicsAgent individually."""
    try:
        agent = MacroEconomicsAgent()
        result = agent.run(region=request.region)
        return MacroAnalysisResponse(
            summary=result.get("summary", ""),
            macro_factors=[asdict(item) for item in result.get("macro_factors", [])],
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Macro economic analysis failed: {exc}")


@router.post("/sector", response_model=SectorAnalysisResponse)
def run_sector_analysis(request: MarketResearchRequest):
    """Executes SectorRotationAgent individually."""
    try:
        agent = SectorRotationAgent()
        result = agent.run()
        return SectorAnalysisResponse(
            summary=result.get("summary", ""),
            sector_trends=[asdict(item) for item in result.get("sector_trends", [])],
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Sector rotation analysis failed: {exc}")
