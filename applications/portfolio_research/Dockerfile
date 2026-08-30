FROM python:3.12-slim

WORKDIR /app

ENV MONGO_URI="mongodb://host.docker.internal:27017"
ENV PYTHONPATH="/app/src:/app/packages/common/src"

# 1. Install shared common package and dependencies (langchain, openai, etc.)
COPY packages/common ./packages/common
RUN pip install --no-cache-dir -e ./packages/common

# 2. Install application package
COPY applications/portfolio_research/pyproject.toml .
COPY applications/portfolio_research/src ./src
RUN pip install --no-cache-dir -e .

CMD ["uvicorn", "portfolio_research.interfaces.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
