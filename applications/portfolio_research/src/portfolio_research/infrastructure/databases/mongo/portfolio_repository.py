from portfolio_research.domain.portfolio.holding import Holding
from portfolio_research.domain.portfolio.portfolio import Portfolio
from portfolio_research.repositories.portfolio_repository import PortfolioRepository


class MongoPortfolioRepository(PortfolioRepository):
    """MongoDB concrete implementation of PortfolioRepository contract."""

    def get_portfolio(self, portfolio_id):
        """Retrieves portfolio from database (stubbed with sample data until connection established)."""
        return Portfolio(
            portfolio_id=portfolio_id + "_mongo",
            holdings=[
                Holding(symbol="AAPL", quantity=10.0, average_price=150.0),
                Holding(symbol="MSFT", quantity=5.0, average_price=280.0),
                Holding(symbol="GOOGL", quantity=8.0, average_price=120.0),
            ],
        )
