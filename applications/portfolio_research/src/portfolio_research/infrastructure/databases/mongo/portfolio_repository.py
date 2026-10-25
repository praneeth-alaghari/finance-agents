import os
from datetime import datetime, timezone
from pymongo import MongoClient, ASCENDING
from portfolio_research.domain.portfolio.holding import Holding
from portfolio_research.domain.portfolio.portfolio import Portfolio
from portfolio_research.repositories.portfolio_repository import PortfolioRepository


class MongoPortfolioRepository(PortfolioRepository):
    def __init__(self, mongo_uri=None, db_name="finance_agents"):
        uri = mongo_uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self._client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        self._collection = self._client[db_name]["portfolios"]
        self._ensure_indexes()

    def _ensure_indexes(self):
        try:
            self._collection.create_index([("user_id", ASCENDING)], unique=True)
        except Exception:
            pass

    def upsert_portfolio(self, portfolio):
        user_id = getattr(portfolio, "user_id", None) or (portfolio.get("user_id") if isinstance(portfolio, dict) else None)
        raw_holdings = getattr(portfolio, "holdings", None) or (portfolio.get("holdings", []) if isinstance(portfolio, dict) else [])

        holdings_doc = []
        for h in raw_holdings:
            if isinstance(h, dict):
                ticker = h.get("ticker") or h.get("symbol")
                quantity = h.get("quantity")
                avg_price = h.get("average_price")
            else:
                ticker = getattr(h, "symbol", None) or getattr(h, "ticker", None)
                quantity = getattr(h, "quantity", None)
                avg_price = getattr(h, "average_price", None)

            holdings_doc.append({
                "ticker": ticker,
                "quantity": quantity,
                "average_price": avg_price,
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
        doc = self._collection.find_one({"$or": [{"user_id": user_id}, {"portfolio_id": user_id}]})
        if not doc:
            return None

        holdings = [
            Holding(
                symbol=h.get("ticker") or h.get("symbol", ""),
                quantity=float(h.get("quantity", 0.0)),
                average_price=float(h.get("average_price", 0.0)),
            )
            for h in doc.get("holdings", [])
        ]
        resolved_user_id = doc.get("user_id") or doc.get("portfolio_id")
        return Portfolio(user_id=resolved_user_id, holdings=holdings, portfolio_id=resolved_user_id)
