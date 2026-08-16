import os
from pymongo import MongoClient
from portfolio_research.domain.portfolio.holding import Holding
from portfolio_research.domain.portfolio.portfolio import Portfolio
from portfolio_research.repositories.portfolio_repository import PortfolioRepository


class MongoPortfolioRepository(PortfolioRepository):
    """MongoDB concrete implementation of PortfolioRepository contract."""

    def __init__(self, mongo_uri: str = None, db_name: str = "finance_agents"):
        if not mongo_uri:
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        self._db = self._client[db_name]
        self._collection = self._db["portfolios"]
        self._seed_default_portfolio_if_empty()

    def _seed_default_portfolio_if_empty(self):
        """Seeds initial sample portfolio data into MongoDB if the collection is empty."""
        try:
            if self._collection.count_documents({}) == 0:
                sample_doc = {
                    "portfolio_id": "default",
                    "holdings": [
                        {"symbol": "AAPL", "quantity": 10.0, "average_price": 150.0},
                        {"symbol": "MSFT", "quantity": 5.0, "average_price": 280.0},
                        {"symbol": "GOOGL", "quantity": 8.0, "average_price": 120.0},
                        {"symbol": "NVDA", "quantity": 15.0, "average_price": 110.0},
                    ],
                }
                self._collection.insert_one(sample_doc)
        except Exception:
            # If database is offline during startup, skip seeding
            pass

    def get_portfolio(self, portfolio_id: str = "default"):
        """Retrieves portfolio domain entity from MongoDB collection by portfolio_id."""
        try:
            doc = self._collection.find_one({"portfolio_id": portfolio_id})
            if doc:
                holdings = [
                    Holding(
                        symbol=h.get("ticker", "UNKNOWN"),
                        quantity=float(h.get("quantity", 0)),
                        average_price=float(h.get("average_price", 0)),
                    )
                    for h in doc.get("holdings", [])
                ]
                return Portfolio(portfolio_id=doc["portfolio_id"], holdings=holdings)
        except Exception as e:
            print(f"[MongoPortfolioRepository ERROR] Failed to fetch portfolio '{portfolio_id}': {e}")

        # Fallback if doc not found or connection issue occurs
        return Portfolio(
            portfolio_id=portfolio_id,
            holdings=[
                Holding(symbol="AAPL", quantity=10.0, average_price=150.0),
                Holding(symbol="MSFT", quantity=5.0, average_price=280.0),
            ],
        )
