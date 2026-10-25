from dataclasses import dataclass, field


@dataclass
class Holding:
    symbol: str
    quantity: float
    average_price: float


@dataclass
class Portfolio:
    user_id: str
    holdings: list[Holding] = field(default_factory=list)
    portfolio_id: str | None = None

    def __post_init__(self):
        if not self.portfolio_id:
            self.portfolio_id = self.user_id
