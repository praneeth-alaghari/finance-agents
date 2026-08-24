from abc import ABC, abstractmethod


class PortfolioRepository(ABC):
    """Abstract interface defining the portfolio data persistence contract."""

    @abstractmethod
    def get_portfolio(self, user_id):
        """Retrieve a Portfolio domain entity by user_id."""
        pass

    @abstractmethod
    def upsert_portfolio(self, portfolio):
        """Upsert a Portfolio domain entity for a user."""
        pass
