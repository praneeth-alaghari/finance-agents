from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class MacroSnapshot:
    name: str
    value: float | None = None
    summary: str = ""


@dataclass
class SectorTrend:
    name: str
    strength: float = 0.0
    summary: str = ""


@dataclass
class CompanyEarningsSnapshot:
    ticker: str
    quarter: str = ""
    eps: float | None = None
    revenue_growth: float | None = None
    guidance: str = ""
    summary: str = ""


@dataclass
class MarketContext:
    market_summary: str = ""
    macro_factors: list[MacroSnapshot] = field(default_factory=list)
    sector_trends: list[SectorTrend] = field(default_factory=list)
    company_earnings: list[CompanyEarningsSnapshot] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
