import uuid
import bcrypt
from portfolio_research.domain.user.user import User


class UserService:
    def __init__(self, user_repository):
        self._user_repository = user_repository

    def signup(self, username, email, password):
        cleaned_username = (username or "").strip()
        cleaned_email = (email or "").strip().lower()
        cleaned_password = password or ""

        if not cleaned_username:
            raise ValueError("Username is required.")
        if not cleaned_email:
            raise ValueError("Email is required.")
        if len(cleaned_password) < 6:
            raise ValueError("Password must be at least 6 characters long.")

        if self._user_repository.get_by_username(cleaned_username):
            raise ValueError(f"Username '{cleaned_username}' is already taken.")

        if self._user_repository.get_by_email(cleaned_email):
            raise ValueError(f"Email '{cleaned_email}' is already registered.")

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(cleaned_password.encode("utf-8"), salt).decode("utf-8")

        user_id = f"usr_{uuid.uuid4().hex[:10]}"
        new_user = User(
            user_id=user_id,
            username=cleaned_username,
            email=cleaned_email,
            password_hash=password_hash,
        )

        return self._user_repository.create_user(new_user)

    def login(self, username_or_email, password):
        identifier = (username_or_email or "").strip()
        cleaned_password = password or ""

        if not identifier or not cleaned_password:
            raise ValueError("Please provide both username/email and password.")

        user = self._user_repository.get_by_email(identifier.lower()) or self._user_repository.get_by_username(identifier)
        if not user or not bcrypt.checkpw(cleaned_password.encode("utf-8"), user.password_hash.encode("utf-8")):
            raise ValueError("Invalid username/email or password.")

        return user

    def get_user_by_id(self, user_id):
        return self._user_repository.get_by_id(user_id)
