# Architecture Notes: Portfolio Research Platform

This document describes the architectural layout, layer responsibilities, and request execution flows of the **Portfolio Research** application.

---

## 1. Overview & Architectural Principles

The application is structured following **Domain-Driven Design (DDD)** and **Clean Architecture (Hexagonal Architecture)** principles.

```
+-------------------------------------------------------------------+
|                         INTERFACE LAYER                           |
|       FastAPI Routers | REST Endpoints | Request/Response Schemas |
+---------------------------------+---------------------------------+
                                  |
                                  v
+---------------------------------+---------------------------------+
|                        APPLICATION LAYER                          |
|             PortfolioService | Use Cases | Business Rules        |
+---------------------------------+---------------------------------+
                                  |
                                  v
+---------------------------------+---------------------------------+
|                          DOMAIN LAYER                             |
|          Entities (Portfolio, Holding) | Business Invariants      |
+---------------------------------+---------------------------------+
                                  ^
                                  | (Implements Interfaces)
+---------------------------------+---------------------------------+
|                       INFRASTRUCTURE LAYER                        |
|   MongoPortfolioRepository | InMemoryRepository | External APIs   |
+-------------------------------------------------------------------+
```

### Core Design Rules
1. **Inner Independence**: The Domain layer has zero dependencies on external libraries, frameworks, or database drivers.
2. **Inverted Infrastructure**: The Application layer defines repository contracts, and the Infrastructure layer implements them.
3. **Explicit Data Contracts**: DTOs and Pydantic models insulate outer clients from internal domain structures.

---

## 2. Layer Responsibilities

### Domain Layer
- **Location**: `finance_agents/domain/`
- **Responsibilities**:
  - Encapsulates core financial business concepts and entities (`Portfolio`, `Holding`).
  - Holds business invariants and calculation rules (e.g., total valuation, asset allocation percentages).
  - Written in pure Python (`@dataclass`) without database annotations or web dependencies.

### Application Layer
- **Location**: `finance_agents/application/`
- **Responsibilities**:
  - Implements application use cases via services like `PortfolioService`.
  - Coordinates domain entities and orchestrates operations.
  - Accepts injected repository interfaces to perform persistence actions without binding to specific database technologies.

### Infrastructure Layer
- **Location**: `finance_agents/infrastructure/`
- **Responsibilities**:
  - Implements technical capabilities such as data storage and retrieval.
  - Contains concrete repositories: `MongoPortfolioRepository` (MongoDB BSON engine) and `InMemoryPortfolioRepository` (in-memory dict).
  - Handles external integrations (market data feeds, LLM APIs, vector stores).

### Interface Layer
- **Location**: `finance_agents/interfaces/`
- **Responsibilities**:
  - Exposes HTTP REST API endpoints via FastAPI routers (`/portfolio`).
  - Converts external HTTP JSON payloads into internal method invocations.
  - Serializes domain entities into client-facing Pydantic schemas (`PortfolioResponse`).

---

## 3. End-to-End Request Flow

The following diagram illustrates how an incoming HTTP request traverses through each layer of the application:

```
+---------+         +----------------+         +------------------+         +-----------------------+         +------------------+
| Browser |         | FastAPI Router |         | PortfolioService |         | MongoPortfolioRepo    |         | MongoDB Database |
| (Client)|         | (Interface)    |         | (Application)    |         | (Infrastructure)      |         | (Storage)        |
+----+----+         +-------+--------+         +--------+---------+         +-----------+-----------+         +--------+---------+
     |                      |                           |                               |                              |
     |--- 1. GET /portfolio ->|                           |                               |                              |
     |                      |--- 2. get_portfolio() --->|                               |                              |
     |                      |                           |--- 3. get_portfolio(id) ----->|                              |
     |                      |                           |                               |--- 4. db.find_one(id) ------>|
     |                      |                           |                               |                              |
     |                      |                           |                               |<-- 5. BSON document ---------|
     |                      |                           |<-- 6. Domain Entity ----------|                              |
     |                      |<-- 7. Domain Entity ------|                               |                              |
     |                      |                           |                               |                              |
     |                      |-- 8. Pydantic Validate -->|                               |                              |
     |<-- 9. HTTP 200 JSON -|                           |                               |                              |
```

### Detailed Sequence
1. **Client Request**: The browser or API client sends an HTTP GET request to `/portfolio`.
2. **Interface Processing**: The FastAPI endpoint router handles the request and invokes `PortfolioService`.
3. **Application Orchestration**: `PortfolioService` delegates data fetching to the injected repository instance.
4. **Infrastructure Retrieval**: `MongoPortfolioRepository` executes a BSON query against MongoDB.
5. **Database Execution**: MongoDB returns raw document data.
6. **Domain Rehydration**: The repository maps the database record into a pure `Portfolio` domain entity.
7. **Service Return**: The service returns the domain entity back to the interface router.
8. **Schema Validation**: The FastAPI router converts the domain model into a client-facing `PortfolioResponse` model using Pydantic validation.
9. Client Response: FastAPI serializes the model into a JSON payload and returns an HTTP 200 OK response.

---

## 4. Complete Repository Directory Architecture

```
finance-agents/
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── applications/
│   └── portfolio_research/
│       ├── README.md
│       ├── agents/
│       ├── docs/
│       │   ├── architecture_notes.md
│       │   ├── deployment_notes.md
│       │   ├── learning_journey.md
│       │   └── roadmap.md
│       ├── prompts/
│       ├── tools/
│       └── workflows/
├── deployment/
│   └── docker/
│       └── Dockerfile
├── docs/
├── frontend/
│   └── streamlit/
├── scripts/
├── src/
│   └── finance_agents/
│       ├── __init__.py
│       ├── application/
│       │   ├── __init__.py
│       │   └── portfolio_service.py
│       ├── core/
│       │   └── __init__.py
│       ├── domain/
│       │   ├── __init__.py
│       │   └── portfolio/
│       │       ├── __init__.py
│       │       ├── holding.py
│       │       └── portfolio.py
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   └── databases/
│       │       ├── __init__.py
│       │       ├── memory/
│       │       │   ├── __init__.py
│       │       │   └── portfolio_repository.py
│       │       └── mongo/
│       │           ├── __init__.py
│       │           └── portfolio_repository.py
│       ├── interfaces/
│       │   ├── __init__.py
│       │   └── api/
│       │       ├── __init__.py
│       │       ├── main.py
│       │       ├── routers/
│       │       │   ├── __init__.py
│       │       │   └── portfolio.py
│       │       └── schemas/
│       │           ├── __init__.py
│       │           └── portfolio.py
│       └── repositories/
│           ├── __init__.py
│           └── portfolio_repository.py
└── tests/
    ├── api/
    ├── integration/
    └── unit/
```
