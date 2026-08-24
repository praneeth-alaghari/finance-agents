import os
from datetime import datetime, timezone
from pymongo import MongoClient, ASCENDING
from portfolio_research.domain.portfolio.holding import Holding
from portfolio_research.domain.portfolio.portfolio import Portfolio
from portfolio_research.repositories.portfolio_repository import PortfolioRepository


class MongoPortfolioRepository(PortfolioRepository):
    """MongoDB concrete implementation of PortfolioRepository contract."""

    def __init__(self, mongo_uri=None, db_name="finance_agents"):
        if not mongo_uri:
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        self._db = self._client[db_name]
        self._collection = self._db["portfolios"]
        self._ensure_indexes()

    def _ensure_indexes(self):
        """Ensure unique index exists on user_id."""
        try:
            self._collection.create_index([("user_id", ASCENDING)], unique=True)
        except Exception:
            pass

    def upsert_portfolio(self, portfolio):
        """Upsert a portfolio into MongoDB by user_id.

        Converts the domain Portfolio entity to a Mongo document, matching by
        user_id and replacing the entire holdings list using $set with upsert=True.
        """
        user_id = (
            getattr(portfolio, "user_id", None)
            or getattr(portfolio, "portfolio_id", None)
            or (portfolio.get("user_id") if isinstance(portfolio, dict) else None)
            or (portfolio.get("portfolio_id") if isinstance(portfolio, dict) else None)
        )
        raw_holdings = (
            getattr(portfolio, "holdings", [])
            if hasattr(portfolio, "holdings")
            else (portfolio.get("holdings", []) if isinstance(portfolio, dict) else [])
        )

        holdings_doc = []
        for holding in raw_holdings:
            if isinstance(holding, dict):
                ticker = holding.get("ticker") or holding.get("symbol")
                quantity = holding.get("quantity")
                average_price = holding.get("average_price")
            else:
                ticker = getattr(holding, "ticker", None) or getattr(holding, "symbol", None)
                quantity = getattr(holding, "quantity", None)
                average_price = getattr(holding, "average_price", None)

            holdings_doc.append({
                "ticker": ticker,
                "quantity": quantity,
                "average_price": average_price,
            })

        portfolio_doc = {
            "user_id": user_id,
            "portfolio_id": user_id,
            "holdings": holdings_doc,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        return self._collection.update_one(
            {"$or": [{"user_id": user_id}, {"portfolio_id": user_id}]},
            {"$set": portfolio_doc},
            upsert=True,
        )

    def get_portfolio(self, user_id):
        """Retrieve a Portfolio domain entity by user_id from MongoDB."""
        doc = self._collection.find_one({"$or": [{"user_id": user_id}, {"portfolio_id": user_id}]})
        if not doc:
            return None

        holdings = []
        for h in doc.get("holdings", []):
            holdings.append(
                Holding(
                    symbol=h.get("ticker") or h.get("symbol", ""),
                    quantity=float(h.get("quantity", 0.0)),
                    average_price=float(h.get("average_price", 0.0)),
                )
            )
        resolved_user_id = doc.get("user_id") or doc.get("portfolio_id")
        return Portfolio(user_id=resolved_user_id, holdings=holdings, portfolio_id=resolved_user_id)
