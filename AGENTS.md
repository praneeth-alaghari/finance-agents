# Agent Instructions & Guidelines

## Python Code Style & Standards

### 1. No Type Hinting
- **Do NOT use Python type hints / type annotations** in function signatures, method parameters, or return types (e.g., avoid `def func(a: str, b: list[dict]) -> dict:`, instead use `def func(a, b):`).
- Exception: Pydantic response/request models where type definitions are fundamentally required by FastAPI / Pydantic schema validation.
- Keep Python code dynamic, readable, standard, and clean.

### 2. PEP 8 & Import Standards
- **Top-Level Imports**: Place all module imports strictly at the top of the file. Do NOT place imports inside functions or methods unless strictly required to break an unavoidable circular dependency.
- **PEP 8 Compliance**: Follow standard PEP 8 naming conventions and structure (4-space indentation, snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants).

### 3. Architecture & Layering
- **Domain Layer (`domain/`)**: Pure business entities.
- **Application Layer (`application/`)**: Orchestrates business workflows and coordinates domain entities with repository interfaces.
- **Infrastructure Layer (`infrastructure/`)**: Concrete implementations (e.g. MongoDB repositories).
- **Interface / API Layer (`interfaces/`)**: FastAPI routers, request/response models.
- **Frontend (`frontend/`)**: Communicates with backend strictly via REST API network calls.
