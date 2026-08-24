from abc import ABC, abstractmethod


class UserRepository(ABC):
    """Abstract interface defining the user data persistence contract."""

    @abstractmethod
    def create_user(self, user):
        """Persist a new User domain entity."""
        pass

    @abstractmethod
    def get_by_id(self, user_id):
        """Retrieve a User domain entity by user_id."""
        pass

    @abstractmethod
    def get_by_username(self, username):
        """Retrieve a User domain entity by username."""
        pass

    @abstractmethod
    def get_by_email(self, email):
        """Retrieve a User domain entity by email."""
        pass
