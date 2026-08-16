# Portfolio Research Application

A domain-driven financial portfolio research and analysis application built with Python, FastAPI, MongoDB, and Agentic AI workflows.

---

## 📌 Overview

**Portfolio Research** is an enterprise-ready financial application designed to model, analyze, and manage investment portfolios. Built on **Clean/Hexagonal Architecture** principles, the platform decouples business entities from persistence technologies, providing a scalable foundation for automated portfolio optimization, market data ingestion, and AI agent research flows.

---

## 🛠 Tech Stack

- **Language**: Python 3.12+
- **API Framework**: FastAPI, Uvicorn, Pydantic v2
- **Persistence**: MongoDB, PyMongo (with In-Memory Fallback Repository)
- **Containerization**: Docker, Docker Hub, Docker Volumes
- **AI & Agent Orchestration**: LangGraph, Multi-Agent Frameworks
- **Architecture**: Domain-Driven Design (DDD), Clean Architecture

---

## ✨ Features

- **Layered Architecture**: Clear separation across Domain, Application, Infrastructure, and Interface layers.
- **Pluggable Persistence**: Repository pattern enabling seamless switching between In-Memory and MongoDB data backends.
- **RESTful API**: Fast, asynchronous endpoints with automated OpenAPI (Swagger) documentation.
- **Container Ready**: Fully containerized deployment with Docker and isolated volume persistence.
- **Autonomous Research Workflows**: Foundation for AI agent workflows performing automated portfolio risk and market research.

---

## 📐 Architecture Diagram

```
+--------------------------------------------------------------------+
|                         CLIENT / BROWSER                           |
+----------------------------------+---------------------------------+
                                   |
                                   v HTTP GET /portfolio
+----------------------------------+---------------------------------+
|                         INTERFACE LAYER                            |
|             FastAPI Router & Pydantic Serialization                |
+----------------------------------+---------------------------------+
                                   |
                                   v
+----------------------------------+---------------------------------+
|                        APPLICATION LAYER                           |
|                    PortfolioService Orchestration                  |
+----------------------------------+---------------------------------+
                                   |
                                   v
+----------------------------------+---------------------------------+
|                          DOMAIN LAYER                              |
|             Pure Domain Entities (Portfolio, Holding)              |
+----------------------------------+---------------------------------+
                                   ^
                                   | (Implements Contract)
+----------------------------------+---------------------------------+
|                       INFRASTRUCTURE LAYER                         |
|           MongoPortfolioRepository / InMemoryRepository            |
+----------------------------------+---------------------------------+
                                   |
                                   v BSON Queries
+----------------------------------+---------------------------------+
|                         MONGODB DATABASE                           |
+--------------------------------------------------------------------+
```

---

## 🚀 Quick Start Instructions

### Prerequisites
- Python 3.12+
- Docker & Docker Compose (optional, for container deployment)

### 1. Local Python Setup

```bash
# Clone the repository
git clone https://github.com/praneeth-alaghari/finance-agents.git
cd finance-agents

# Create virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### 2. Run API Server

```bash
# Start FastAPI application with Uvicorn
uvicorn finance_agents.interfaces.api.main:app --reload --host 0.0.0.0 --port 8000
```

Access the interactive API documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 3. Docker Quick Start

```bash
# Build Docker image
docker build -t portfolio-research -f deployment/docker/Dockerfile .

# Run application container
docker run -p 8000:8000 portfolio-research
```

---

## 📚 Documentation Reference

For detailed guides, architecture decision records, roadmap checklists, and deployment command cheat sheets, explore the documentation suite inside [`docs/`](file:///c:/code_repo/finance-agents/applications/portfolio_research/docs/):

- 🧠 [Learning Journey](file:///c:/code_repo/finance-agents/applications/portfolio_research/docs/learning_journey.md): Key concepts learned (Layered Architecture, Repository Pattern, DI, FastAPI, Docker, MongoDB).
- 🏗️ [Architecture Notes](file:///c:/code_repo/finance-agents/applications/portfolio_research/docs/architecture_notes.md): Layer breakdown, responsibilities, and request sequence flows.
- 🗺️ [Project Roadmap](file:///c:/code_repo/finance-agents/applications/portfolio_research/docs/roadmap.md): Milestone progress and upcoming feature checklist.
- 🐳 [Deployment Notes](file:///c:/code_repo/finance-agents/applications/portfolio_research/docs/deployment_notes.md): Practical Docker, MongoDB, and volume management reference.
