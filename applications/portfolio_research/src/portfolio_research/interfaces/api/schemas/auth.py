from pydantic import BaseModel, ConfigDict


class SignupRequest(BaseModel):
    """Schema for user registration request."""
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    """Schema for user login request."""
    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for user representation response."""
    user_id: str
    username: str
    email: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    """Schema for successful authentication response."""
    user_id: str
    username: str
    email: str
    token: str

    model_config = ConfigDict(from_attributes=True)
