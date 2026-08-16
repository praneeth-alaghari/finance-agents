# Learning Journey: Portfolio Research & Finance Platform

This document tracks key architectural, engineering, and devops concepts mastered during the development of the **Portfolio Research** application. It serves as a continuous record of technical growth, core concepts, and interviews reference.

---

## 1. Layered Architecture

### Key Takeaways
- **Separation of Concerns**: Decouples presentation/interface code, business logic, and infrastructure data access into distinct layers.
- **Dependency Rule**: Dependencies only point inwards. Inner layers (Domain & Application) have zero knowledge of outer layers (Infrastructure & Interface).
- **Maintainability & Testability**: Business logic can be unit-tested in isolation without mocking databases or starting HTTP servers.

### Application Context
In `portfolio_research`, code is divided into four distinct layers: `domain`, `application`, `infrastructure`, and `interfaces`.

---

## 2. Domain Models

### Key Takeaways
- **Pure Business Logic**: Domain models represent core business entities (`Portfolio`, `Holding`) using pure Python data constructs (e.g., `@dataclass`).
- **Framework Independence**: Domain entities do not inherit from ORM basemodels (like SQLAlchemy or MongoEngine) or API frameworks (like Pydantic).
- **Ubiquitous Language**: Terminology matches domain vocabulary (shares, tickers, holdings, asset allocation).

---

## 3. Repository Pattern

### Key Takeaways
- **Persistence Abstraction**: Mediates between the domain and data mapping layers using a collection-like interface for accessing domain objects.
- **Pluggable Backends**: Allows seamless switching between persistence mechanisms—such as `InMemoryPortfolioRepository` for testing and `MongoPortfolioRepository` for production—without altering service logic.
- **Contract-Driven**: Enforces consistent interface contracts across all repository implementations.

---

## 4. Dependency Injection

### Key Takeaways
- **Inversion of Control (IoC)**: High-level modules (services) do not instantiate their dependencies directly; dependencies are passed into constructors.
- **Flexibility**: Enables passing concrete repository implementations into `PortfolioService(portfolio_repository=repository)` dynamically based on configuration or environment.
- **Simplified Testing**: Mock repositories can be injected easily during automated unit and integration tests.

---

## 5. FastAPI

### Key Takeaways
- **Asynchronous Web Framework**: High-performance HTTP server leveraging Python type hints and `asyncio`.
- **Automatic OpenAPI Documentation**: Automatically generates interactive Swagger (`/docs`) and ReDoc (`/redoc`) documentation.
- **Schema Validation**: Integrates Pydantic schemas (`PortfolioResponse`) for automatic request validation, parsing, and serialization.

---

## 6. Docker

### Key Takeaways
- **Containerization**: Packages the application, python dependencies, and runtime environment into an immutable, isolated image.
- **Reproducibility**: Eliminates "works on my machine" issues by standardizing the runtime environment across development, testing, and production.
- **Dockerfile Best Practices**: Use of lightweight base images (e.g., `python:3.12-slim`), explicit working directory management, and optimized build caching.

---

## 7. Docker Hub

### Key Takeaways
- **Centralized Container Registry**: Cloud registry for hosting, versioning, and sharing Docker images.
- **Image Tagging**: Tagging images with semantic versioning (`v1.0.0`) and `latest` flags for pipeline deployment.
- **Distribution Pipeline**: Building images locally or via CI/CD, pushing to Docker Hub, and pulling down to deployment targets.

---

## 8. MongoDB

### Key Takeaways
- **NoSQL Document Database**: Stores financial data as flexible, JSON-like BSON documents.
- **Schema Flexibility**: Accommodates evolving portfolio data structures, complex nested holdings, and historical snapshot data without requiring rigid schema migrations.
- **Python Integration**: Utilizing PyMongo / Motor drivers to execute queries efficiently.

---

## 9. Docker Volumes

### Key Takeaways
- **Stateful Persistence**: Docker containers are ephemeral by default. Volumes persist MongoDB data independently of container lifecycles.
- **Named Volumes vs. Bind Mounts**: Named volumes are managed by Docker for database storage, while bind mounts mount host directories into containers during development.
- **Data Safety**: Prevent data loss when stopping, destroying, or upgrading database containers.

---

## 10. Future Learnings & Notes

> This section is reserved for upcoming concepts and tools to be explored as the portfolio research platform expands.

- [ ] **LangGraph & Multi-Agent Orchestration**: Stateful graph execution for financial analysis agents.
- [ ] **Vector Databases (Chroma / Qdrant)**: Embeddings storage for unstructured financial earnings reports and news.
- [ ] **Event-Driven Architecture**: Asynchronous event streams for real-time market data ticks.
- [ ] **Authentication & Security**: OAuth2 with JWT tokens and role-based access control (RBAC).
