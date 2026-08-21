# Agent Instructions & Guidelines

## Python Code Style & Standards

### 1. No Type Hinting
- **Do NOT use Python type hints / type annotations** in function signatures, method parameters, or return types (e.g., avoid `def func(a: str, b: list[dict]) -> dict:`, instead use `def func(a, b):`).
- Exception: Pydantic response/request models where type definitions are fundamentally required by FastAPI / Pydantic schema validation.
- Keep Python code dynamic, readable, standard, and clean.

### 2. Architecture & Layering
- **Domain Layer (`domain/`)**: Pure business entities.
- **Application Layer (`application/`)**: Orchestrates business workflows and coordinates domain entities with repository interfaces.
- **Infrastructure Layer (`infrastructure/`)**: Concrete implementations (e.g. MongoDB repositories).
- **Interface / API Layer (`interfaces/`)**: FastAPI routers, request/response models.
- **Frontend (`frontend/`)**: Communicates with backend strictly via REST API network calls.
