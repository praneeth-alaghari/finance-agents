from fastapi import FastAPI
from portfolio_research.interfaces.api.routers.auth import router as auth_router
from portfolio_research.interfaces.api.routers.portfolio import router as portfolio_router

app = FastAPI(title="Finance Agents API")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(auth_router, prefix="/api/v1")
app.include_router(portfolio_router, prefix="/api/v1")
