import csv
import io
from fastapi import APIRouter, HTTPException, UploadFile, File, Header
from portfolio_research.application.portfolio_service import PortfolioService
from portfolio_research.infrastructure.databases.mongo.portfolio_repository import MongoPortfolioRepository
from portfolio_research.interfaces.api.schemas.portfolio import PortfolioResponse, PortfolioInsightResponse

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("", response_model=PortfolioResponse)
def get_portfolio(x_user_id: str = Header("default", alias="X-User-Id")):
    """Retrieve portfolio for the authenticated user."""
    repository = MongoPortfolioRepository()
    service = PortfolioService(portfolio_repository=repository)
    domain_portfolio = service.get_portfolio(user_id=x_user_id)
    if not domain_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found for this user.")
    return PortfolioResponse.model_validate(domain_portfolio)


@router.post("/upload", response_model=PortfolioResponse)
async def upload_portfolio(
    file: UploadFile = File(...),
    x_user_id: str = Header("default", alias="X-User-Id"),
):
    """Receives uploaded portfolio CSV file, validates, and persists to MongoDB for the authenticated user."""
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    contents = await file.read()
    try:
        decoded = contents.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Could not decode CSV file as UTF-8.")

    reader = csv.DictReader(io.StringIO(decoded))
    csv_rows = list(reader)

    if not csv_rows:
        raise HTTPException(status_code=400, detail="CSV file is empty or contains only headers.")

    repository = MongoPortfolioRepository()
    service = PortfolioService(portfolio_repository=repository)

    try:
        domain_portfolio = service.upload_portfolio_csv(user_id=x_user_id, csv_rows=csv_rows)
    except ValueError as val_err:
        raise HTTPException(status_code=422, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Failed to persist portfolio: {err}")

    return PortfolioResponse.model_validate(domain_portfolio)


@router.post("/insights", response_model=PortfolioInsightResponse)
def get_portfolio_insights(x_user_id: str = Header("default", alias="X-User-Id")):
    """Generates LLM-powered financial research and insights for the user's portfolio."""
    repository = MongoPortfolioRepository()
    service = PortfolioService(portfolio_repository=repository)
    try:
        result = service.generate_ai_insight(user_id=x_user_id)
        return PortfolioInsightResponse(
            user_id=x_user_id,
            insight=result["insight"],
            model=result["model"],
        )
    except ValueError as val_err:
        raise HTTPException(status_code=422, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"AI insight generation failed: {err}")
