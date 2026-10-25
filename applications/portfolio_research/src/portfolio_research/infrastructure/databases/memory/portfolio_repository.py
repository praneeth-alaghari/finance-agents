from portfolio_research.domain.portfolio.holding import Holding
from portfolio_research.domain.portfolio.portfolio import Portfolio
from portfolio_research.repositories.portfolio_repository import PortfolioRepository


class InMemoryPortfolioRepository(PortfolioRepository):
    def __init__(self):
        self._portfolios = {
            "default": Portfolio(
                user_id="default",
                portfolio_id="default",
                holdings=[
                    Holding(symbol="AAPL", quantity=10.0, average_price=150.0),
                    Holding(symbol="MSFT", quantity=5.0, average_price=280.0),
                    Holding(symbol="GOOGL", quantity=8.0, average_price=120.0),
                ],
            )
        }

    def get_portfolio(self, user_id):
        return self._portfolios.get(user_id)

    def upsert_portfolio(self, portfolio):
        self._portfolios[portfolio.user_id] = portfolio
        return portfolio
