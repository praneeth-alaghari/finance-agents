# Coding Style Rules

## 1. Type Annotations
- Do NOT include Python type hints or annotations in function signatures, method parameters, or return types across any newly written or refactored code.
- Write standard, dynamic Python functions and methods: e.g., `def my_method(self, param1, param2):`.
- Only use type declarations inside Pydantic BaseModel definitions where fundamentally required by FastAPI / Pydantic schema validation.

## 2. PEP 8 & Imports Standard
- **Top-Level Imports**: Always place all imports at the top of the file, never inside functions or methods (unless strictly necessary to resolve an unavoidable circular import).
- **PEP 8 Compliance**: Follow standard PEP 8 formatting (4 spaces indentation, snake_case for functions and variables, PascalCase for classes, UPPER_CASE for constants).
- Keep code clean, readable, dynamic, and standard across all packages and services.
