from portfolio_research.domain.portfolio.holding import Holding
from portfolio_research.domain.portfolio.portfolio import Portfolio


class PortfolioService:
    """Application service for managing portfolio logic, decoupled from persistence engines."""

    def __init__(self, portfolio_repository):
        self._portfolio_repository = portfolio_repository

    def get_portfolio(self, portfolio_id="default"):
        """Retrieves a portfolio domain entity by ID via injected repository."""
        return self._portfolio_repository.get_portfolio(portfolio_id)

    def upload_portfolio_csv(self, portfolio_id, csv_rows):
        """Parses CSV rows, validates data, constructs domain objects, and persists via upsert."""
        holdings = []
        for index, row in enumerate(csv_rows, start=1):
            ticker = row.get("ticker") or row.get("symbol") or row.get("Ticker") or row.get("Symbol")
            if not ticker or not str(ticker).strip():
                raise ValueError(f"Row {index}: Missing ticker/symbol.")

            raw_qty = row.get("quantity") or row.get("Quantity") or row.get("shares") or row.get("Shares")
            if raw_qty is None or str(raw_qty).strip() == "":
                raise ValueError(f"Row {index} ({ticker}): Missing quantity.")
            try:
                quantity = float(raw_qty)
            except ValueError:
                raise ValueError(f"Row {index} ({ticker}): Invalid quantity '{raw_qty}'. Must be a number.")

            if quantity <= 0:
                raise ValueError(f"Row {index} ({ticker}): Quantity must be greater than 0.")

            raw_price = row.get("average_price") or row.get("Average_Price") or row.get("price") or row.get("Price") or row.get("avg_price")
            if raw_price is None or str(raw_price).strip() == "":
                raise ValueError(f"Row {index} ({ticker}): Missing average price.")
            try:
                average_price = float(raw_price)
            except ValueError:
                raise ValueError(f"Row {index} ({ticker}): Invalid average price '{raw_price}'. Must be a number.")

            if average_price < 0:
                raise ValueError(f"Row {index} ({ticker}): Average price cannot be negative.")

            holdings.append(
                Holding(
                    symbol=str(ticker).strip().upper(),
                    quantity=quantity,
                    average_price=average_price,
                )
            )

        portfolio = Portfolio(portfolio_id=portfolio_id, holdings=holdings)
        self._portfolio_repository.upsert_portfolio(portfolio)
        return portfolio
