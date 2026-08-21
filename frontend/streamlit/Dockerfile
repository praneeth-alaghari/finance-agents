FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir streamlit requests

COPY app.py .

ENV API_BASE_URL="http://portfolio_research:8000/api/v1"

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
