from finance_agents.domain.portfolio.holding import Holding
from finance_agents.domain.portfolio.portfolio import Portfolio
from finance_agents.repositories.portfolio_repository import PortfolioRepository


class InMemoryPortfolioRepository(PortfolioRepository):
    """In-memory concrete implementation of PortfolioRepository contract."""

    def __init__(self):
        self._portfolios = {
            "default": Portfolio(
                portfolio_id="default_memory",
                holdings=[
                    Holding(symbol="AAPL", quantity=10.0, average_price=150.0),
                    Holding(symbol="MSFT", quantity=5.0, average_price=280.0),
                    Holding(symbol="GOOGL", quantity=8.0, average_price=120.0),
                ],
            )
        }

    def get_portfolio(self, portfolio_id):
        """Retrieves a portfolio by ID from in-memory dictionary storage."""
        return self._portfolios.get(portfolio_id)
