from common.models import CompanyEarningsSnapshot, MacroSnapshot, MarketContext, SectorTrend


class MarketResearchService:
    """Service for building shared market context used by finance apps."""

    def build_market_context(self, market_summary="", macro_factors=None, sector_trends=None, company_earnings=None):
        return MarketContext(
            market_summary=market_summary,
            macro_factors=macro_factors or [],
            sector_trends=sector_trends or [],
            company_earnings=company_earnings or [],
        )

    def build_macro_snapshot(self, name, value=None, summary=""):
        return MacroSnapshot(name=name, value=value, summary=summary)

    def build_sector_trend(self, name, strength=0.0, summary=""):
        return SectorTrend(name=name, strength=strength, summary=summary)

    def build_earnings_snapshot(self, ticker, quarter="", eps=None, revenue_growth=None, guidance="", summary=""):
        return CompanyEarningsSnapshot(
            ticker=ticker,
            quarter=quarter,
            eps=eps,
            revenue_growth=revenue_growth,
            guidance=guidance,
            summary=summary,
        )
