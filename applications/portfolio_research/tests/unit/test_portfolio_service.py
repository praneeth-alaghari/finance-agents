import pytest
from portfolio_research.application.portfolio_service import PortfolioService
from portfolio_research.repositories.portfolio_repository import PortfolioRepository


class InMemoryPortfolioRepository(PortfolioRepository):
    """In-memory fake repository for testing PortfolioService."""

    def __init__(self):
        self.portfolios = {}

    def get_portfolio(self, user_id):
        return self.portfolios.get(user_id)

    def upsert_portfolio(self, portfolio):
        self.portfolios[portfolio.user_id] = portfolio
        return portfolio


class FakeLLMClient:
    """Mock LLM client for deterministic unit testing."""

    def __init__(self, response_text="Mock AI Analysis", model="mock-gpt-4o"):
        self.response_text = response_text
        self.model = model
        self.last_prompt = None

    def generate(self, prompt, system_instruction=None, temperature=None):
        self.last_prompt = prompt
        return self.response_text


def test_upload_and_get_portfolio():
    repo = InMemoryPortfolioRepository()
    service = PortfolioService(portfolio_repository=repo)

    rows = [
        {"ticker": "TCS", "quantity": "10", "average_price": "3500.0"},
        {"ticker": "INFY", "quantity": "20", "average_price": "1500.0"},
    ]

    portfolio = service.upload_portfolio_csv("usr_test123", rows)
    assert portfolio.user_id == "usr_test123"
    assert len(portfolio.holdings) == 2
    assert portfolio.holdings[0].symbol == "TCS"
    assert portfolio.holdings[0].quantity == 10.0

    retrieved = service.get_portfolio("usr_test123")
    assert retrieved is not None
    assert len(retrieved.holdings) == 2


def test_user_portfolios_are_isolated():
    repo = InMemoryPortfolioRepository()
    service = PortfolioService(portfolio_repository=repo)

    rows_a = [{"ticker": "TCS", "quantity": "10", "average_price": "3500.0"}]
    rows_b = [{"ticker": "AAPL", "quantity": "50", "average_price": "180.0"}]

    service.upload_portfolio_csv("user_A", rows_a)
    service.upload_portfolio_csv("user_B", rows_b)

    portfolio_a = service.get_portfolio("user_A")
    portfolio_b = service.get_portfolio("user_B")

    assert len(portfolio_a.holdings) == 1
    assert portfolio_a.holdings[0].symbol == "TCS"

    assert len(portfolio_b.holdings) == 1
    assert portfolio_b.holdings[0].symbol == "AAPL"


def test_generate_ai_insight_success():
    repo = InMemoryPortfolioRepository()
    service = PortfolioService(portfolio_repository=repo)

    rows = [{"ticker": "NVDA", "quantity": "15", "average_price": "120.0"}]
    service.upload_portfolio_csv("usr_ai_test", rows)

    mock_llm = FakeLLMClient(response_text="Strong tech allocation with high growth potential.", model="gpt-4o-mini")
    result = service.generate_ai_insight("usr_ai_test", llm_client=mock_llm)

    assert "Strong tech allocation" in result["insight"]
    assert result["model"] == "gpt-4o-mini"
    assert "NVDA" in mock_llm.last_prompt


def test_generate_ai_insight_empty_portfolio():
    repo = InMemoryPortfolioRepository()
    service = PortfolioService(portfolio_repository=repo)

    with pytest.raises(ValueError, match="No portfolio found"):
        service.generate_ai_insight("empty_user")
