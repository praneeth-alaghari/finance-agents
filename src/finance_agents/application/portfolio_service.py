class PortfolioService:
    """Application service for managing portfolio logic, decoupled from persistence engines."""

    def __init__(self, portfolio_repository):
        self._portfolio_repository = portfolio_repository

    def get_portfolio(self, portfolio_id="default"):
        """Retrieves a portfolio domain entity by ID via injected repository."""
        return self._portfolio_repository.get_portfolio(portfolio_id)
