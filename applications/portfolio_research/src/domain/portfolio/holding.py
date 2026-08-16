from dataclasses import dataclass


@dataclass
class Holding:
    """Domain model representing a single stock position."""
    symbol: str
    quantity: float
    average_price: float
