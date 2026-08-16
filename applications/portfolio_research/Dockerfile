FROM python:3.12-slim

WORKDIR /app

ENV MONGO_URI="mongodb://host.docker.internal:27017"

COPY pyproject.toml .

COPY src ./src

RUN pip install --no-cache-dir .

CMD ["uvicorn", "portfolio_research.interfaces.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
