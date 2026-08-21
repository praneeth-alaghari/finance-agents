# Coding Style Rules

## Type Annotations
- Do NOT include Python type hints or annotations in function signatures, method parameters, or return types across any newly written or refactored code.
- Write standard, dynamic Python functions and methods: e.g., `def my_method(self, param1, param2):`.
- Only use type declarations inside Pydantic BaseModel definitions where required by FastAPI.
