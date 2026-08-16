from dataclasses import dataclass, field
from finance_agents.domain.portfolio.holding import Holding


@dataclass
class Portfolio:
    """Domain model representing a portfolio of holding positions."""
    portfolio_id: str
    holdings: list[Holding] = field(default_factory=list)
