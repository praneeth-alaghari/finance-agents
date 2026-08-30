from portfolio_research.domain.portfolio.holding import Holding
from portfolio_research.domain.portfolio.portfolio import Portfolio


class PortfolioService:
    """Application service for managing portfolio logic, decoupled from persistence engines."""

    def __init__(self, portfolio_repository):
        self._portfolio_repository = portfolio_repository

    def get_portfolio(self, user_id="default"):
        """Retrieves a portfolio domain entity by user_id via injected repository."""
        return self._portfolio_repository.get_portfolio(user_id)

    def upload_portfolio_csv(self, user_id, csv_rows):
        """Parses CSV rows, validates data, constructs domain objects, and persists via upsert."""
        if not user_id:
            raise ValueError("User identification is required to upload a portfolio.")

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

        portfolio = Portfolio(user_id=user_id, holdings=holdings, portfolio_id=user_id)
        self._portfolio_repository.upsert_portfolio(portfolio)
        return portfolio

    def generate_ai_insight(self, user_id, llm_client=None):
        """Generates AI analysis and insights for a user's portfolio."""
        portfolio = self.get_portfolio(user_id)
        if not portfolio or not portfolio.holdings:
            raise ValueError("No portfolio found for this user. Please upload a portfolio CSV first.")

        holdings_summary = []
        total_invested = 0.0
        for h in portfolio.holdings:
            invested = h.quantity * h.average_price
            total_invested += invested
            holdings_summary.append(
                f"- Ticker: {h.symbol}, Quantity: {h.quantity}, Avg Price: ${h.average_price:,.2f}, Total Cost: ${invested:,.2f}"
            )

        prompt = (
            f"User Portfolio Summary (Total Invested: ${total_invested:,.2f}):\n"
            + "\n".join(holdings_summary)
            + "\n\nPlease provide a clear and professional financial analysis of this portfolio covering:\n"
            + "1. Diversification & Concentration Risk\n"
            + "2. Key Strengths & Potential Exposures\n"
            + "3. Strategic Recommendations for Rebalancing or Risk Management"
        )

        system_instruction = (
            "You are an elite institutional portfolio manager and quantitative risk analyst. "
            "Provide insightful, concise, and structured financial portfolio assessments."
        )

        if llm_client is None:
            from ai_core import get_llm_client
            llm_client = get_llm_client()

        insight = llm_client.generate(prompt=prompt, system_instruction=system_instruction)
        model_name = getattr(llm_client, "model", "Unknown Model")
        return {"insight": insight, "model": model_name}
