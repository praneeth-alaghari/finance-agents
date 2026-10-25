from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user):
        pass

    @abstractmethod
    def get_by_id(self, user_id):
        pass

    @abstractmethod
    def get_by_username(self, username):
        pass

    @abstractmethod
    def get_by_email(self, email):
        pass
