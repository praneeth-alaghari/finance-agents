from pydantic import BaseModel, ConfigDict


class HoldingResponse(BaseModel):
    """API response model for an individual holding position."""
    symbol: str
    quantity: float
    average_price: float

    model_config = ConfigDict(from_attributes=True)


class PortfolioResponse(BaseModel):
    """API response model for a portfolio."""
    user_id: str
    portfolio_id: str
    holdings: list[HoldingResponse]

    model_config = ConfigDict(from_attributes=True)
