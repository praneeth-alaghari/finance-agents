import pytest
from portfolio_research.application.user_service import UserService
from portfolio_research.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    """In-memory fake repository for testing UserService."""

    def __init__(self):
        self.users = {}

    def create_user(self, user):
        self.users[user.user_id] = user
        return user

    def get_by_id(self, user_id):
        return self.users.get(user_id)

    def get_by_username(self, username):
        for u in self.users.values():
            if u.username.lower() == username.lower():
                return u
        return None

    def get_by_email(self, email):
        for u in self.users.values():
            if u.email.lower() == email.lower():
                return u
        return None


def test_signup_successful():
    repo = InMemoryUserRepository()
    service = UserService(user_repository=repo)

    user = service.signup("praneeth", "praneeth@example.com", "secret123")
    assert user.user_id.startswith("usr_")
    assert user.username == "praneeth"
    assert user.email == "praneeth@example.com"
    assert user.password_hash != "secret123"  # Password is encrypted


def test_signup_duplicate_username():
    repo = InMemoryUserRepository()
    service = UserService(user_repository=repo)

    service.signup("praneeth", "praneeth@example.com", "secret123")
    with pytest.raises(ValueError, match="already taken"):
        service.signup("praneeth", "other@example.com", "secret123")


def test_signup_duplicate_email():
    repo = InMemoryUserRepository()
    service = UserService(user_repository=repo)

    service.signup("praneeth", "praneeth@example.com", "secret123")
    with pytest.raises(ValueError, match="already registered"):
        service.signup("another_user", "praneeth@example.com", "secret123")


def test_login_success():
    repo = InMemoryUserRepository()
    service = UserService(user_repository=repo)

    service.signup("praneeth", "praneeth@example.com", "secret123")
    user = service.login("praneeth", "secret123")
    assert user.username == "praneeth"


def test_login_invalid_password():
    repo = InMemoryUserRepository()
    service = UserService(user_repository=repo)

    service.signup("praneeth", "praneeth@example.com", "secret123")
    with pytest.raises(ValueError, match="Invalid username/email or password"):
        service.login("praneeth", "wrong_password")
