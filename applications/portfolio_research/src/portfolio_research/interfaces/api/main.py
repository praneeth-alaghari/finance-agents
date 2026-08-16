from fastapi import FastAPI
from finance_agents.interfaces.api.routers.portfolio import router as portfolio_router

app = FastAPI(title="Finance Agents API")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(portfolio_router, prefix="/api/v1")
