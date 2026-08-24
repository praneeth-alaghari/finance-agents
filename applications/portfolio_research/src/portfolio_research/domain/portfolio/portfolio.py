from dataclasses import dataclass, field
from portfolio_research.domain.portfolio.holding import Holding


@dataclass
class Portfolio:
    """Domain model representing a portfolio of holding positions owned by a user."""
    user_id: str
    holdings: list[Holding] = field(default_factory=list)
    portfolio_id: str = None

    def __post_init__(self):
        if not self.portfolio_id:
            self.portfolio_id = self.user_id
