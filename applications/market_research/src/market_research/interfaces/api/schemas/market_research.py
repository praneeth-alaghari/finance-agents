from pydantic import BaseModel, Field, field_validator


def _format_summary(v):
    if isinstance(v, list):
        return "\n".join(f"• {str(item).lstrip('•- ')}" for item in v if item)
    return str(v or "").strip()


class MacroSnapshotSchema(BaseModel):
    name: str
    value: float | str | None = None
    summary: str = ""


class SectorTrendSchema(BaseModel):
    name: str
    strength: float = 0.0
    summary: str = ""


class CompanyEarningsSnapshotSchema(BaseModel):
    ticker: str
    quarter: str = ""
    eps: float | None = None
    revenue_growth: float | None = None
    guidance: str = ""
    summary: str = ""


class MarketContextResponse(BaseModel):
    market_summary: str = ""
    macro_factors: list[MacroSnapshotSchema] = Field(default_factory=list)
    sector_trends: list[SectorTrendSchema] = Field(default_factory=list)
    company_earnings: list[CompanyEarningsSnapshotSchema] = Field(default_factory=list)
    generated_at: str = ""

    @field_validator("market_summary", mode="before")
    @classmethod
    def validate_market_summary(cls, v):
        return _format_summary(v)


class MacroAnalysisResponse(BaseModel):
    summary: str = ""
    macro_factors: list[MacroSnapshotSchema] = Field(default_factory=list)

    @field_validator("summary", mode="before")
    @classmethod
    def validate_summary(cls, v):
        return _format_summary(v)


class SectorAnalysisResponse(BaseModel):
    summary: str = ""
    sector_trends: list[SectorTrendSchema] = Field(default_factory=list)

    @field_validator("summary", mode="before")
    @classmethod
    def validate_summary(cls, v):
        return _format_summary(v)


class MarketResearchRequest(BaseModel):
    market_summary: str = ""
    region: str = "US"
    sector_focus: str | None = None
