import os
from pymongo import MongoClient
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

    def upsert_portfolio(self, portfolio):
        """Upsert a portfolio into MongoDB.

        Converts the domain Portfolio entity to a Mongo document, matching by
        portfolio_id and replacing the entire holdings list using $set with upsert=True.
        """
        portfolio_id = getattr(portfolio, "portfolio_id", None) if hasattr(portfolio, "portfolio_id") else portfolio.get("portfolio_id")
        raw_holdings = getattr(portfolio, "holdings", []) if hasattr(portfolio, "holdings") else portfolio.get("holdings", [])

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
            "portfolio_id": portfolio_id,
            "holdings": holdings_doc,
        }

        return self._collection.update_one(
            {"portfolio_id": portfolio_id},
            {"$set": portfolio_doc},
            upsert=True,
        )

    def get_portfolio(self, portfolio_id):
        """Retrieve a Portfolio domain entity by its ID from MongoDB."""
        doc = self._collection.find_one({"portfolio_id": portfolio_id})
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
        return Portfolio(portfolio_id=doc["portfolio_id"], holdings=holdings)

    def get_all_portfolios(self):
        # TODO:
        # - Mongo operation to be used: self._collection.find({})
        # - Expected input: None
        # - Expected return value: List[Portfolio] - A list of all Portfolio domain entities found in the collection
        # - Note: If query fails, raise an exception
        pass

    def save_portfolio(self, portfolio):
        # TODO:
        # - Mongo operation to be used: self._collection.insert_one(portfolio_doc)
        # - Expected input: portfolio (Portfolio) - The Portfolio domain entity to insert
        # - Expected return value: None (or the inserted ID / persisted entity)
        # - Note: If insertion fails or duplicate key error occurs, raise an exception
        pass

    def update_portfolio(self, portfolio):
        # TODO:
        # - Mongo operation to be used: self._collection.update_one({"portfolio_id": portfolio.portfolio_id}, {"$set": portfolio_doc})
        # - Expected input: portfolio (Portfolio) - The Portfolio domain entity containing updated data
        # - Expected return value: None (or boolean/update result indicating success)
        # - Note: If update fails or target portfolio is not found, raise an exception
        pass

    def delete_portfolio(self, portfolio_id):
        # TODO:
        # - Mongo operation to be used: self._collection.delete_one({"portfolio_id": portfolio_id})
        # - Expected input: portfolio_id (str) - The unique identifier of the portfolio to delete
        # - Expected return value: None (or boolean/delete result indicating success)
        # - Note: If deletion fails or document does not exist, raise an exception
        pass
