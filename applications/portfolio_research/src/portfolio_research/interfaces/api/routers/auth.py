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
    service = UserService(MongoUserRepository())
    try:
        user = service.signup(request.username, request.email, request.password)
        return UserResponse.model_validate(user)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Registration failed: {err}")


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    service = UserService(MongoUserRepository())
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
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required (missing X-User-Id header).")

    service = UserService(MongoUserRepository())
    user = service.get_user_by_id(x_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return UserResponse.model_validate(user)
