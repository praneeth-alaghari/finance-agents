from abc import ABC, abstractmethod


class PortfolioRepository(ABC):
    """Abstract interface defining the portfolio data persistence contract."""

    @abstractmethod
    def get_portfolio(self, portfolio_id):
        """Retrieve a Portfolio domain entity by its ID."""
        pass
