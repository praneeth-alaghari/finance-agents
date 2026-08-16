from fastapi import APIRouter, HTTPException
from finance_agents.application.portfolio_service import PortfolioService
from finance_agents.infrastructure.databases.memory.portfolio_repository import InMemoryPortfolioRepository
from finance_agents.infrastructure.databases.mongo.portfolio_repository import MongoPortfolioRepository
from finance_agents.interfaces.api.schemas.portfolio import PortfolioResponse

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("", response_model=PortfolioResponse)
def get_portfolio():
    repository = MongoPortfolioRepository()
    service = PortfolioService(portfolio_repository=repository)
    domain_portfolio = service.get_portfolio(portfolio_id="default")
    if not domain_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return PortfolioResponse.model_validate(domain_portfolio)
