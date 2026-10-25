from abc import ABC, abstractmethod


class PortfolioRepository(ABC):
    @abstractmethod
    def get_portfolio(self, user_id):
        pass

    @abstractmethod
    def upsert_portfolio(self, portfolio):
        pass
