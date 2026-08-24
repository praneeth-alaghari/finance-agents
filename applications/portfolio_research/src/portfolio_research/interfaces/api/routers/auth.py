from fastapi import APIRouter, HTTPException, Header
from portfolio_research.application.user_service import UserService
from portfolio_research.infrastructure.databases.mongo.user_repository import MongoUserRepository
from portfolio_research.interfaces.api.schemas.auth import (
    SignupRequest,
    LoginRequest,
    UserResponse,
    LoginResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(request: SignupRequest):
    """Register a new user account with unique username and email."""
    repository = MongoUserRepository()
    service = UserService(user_repository=repository)
    try:
        user = service.signup(request.username, request.email, request.password)
        return UserResponse.model_validate(user)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Registration failed: {err}")


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    """Authenticate user credentials and return user profile with session token."""
    repository = MongoUserRepository()
    service = UserService(user_repository=repository)
    try:
        user = service.login(request.username, request.password)
        return LoginResponse(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            token=f"tok_{user.user_id}",
        )
    except ValueError as err:
        raise HTTPException(status_code=401, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Login failed: {err}")


@router.get("/me", response_model=UserResponse)
def get_current_user(x_user_id: str = Header(None, alias="X-User-Id")):
    """Fetch profile of currently authenticated user via X-User-Id header."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required (missing X-User-Id header).")

    repository = MongoUserRepository()
    service = UserService(user_repository=repository)
    user = service.get_user_by_id(x_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return UserResponse.model_validate(user)
