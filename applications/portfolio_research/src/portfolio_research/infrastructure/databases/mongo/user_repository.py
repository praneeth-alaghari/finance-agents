import os
from pymongo import MongoClient, ASCENDING
from portfolio_research.domain.user.user import User
from portfolio_research.repositories.user_repository import UserRepository


class MongoUserRepository(UserRepository):
    """MongoDB concrete implementation of UserRepository contract."""

    def __init__(self, mongo_uri=None, db_name="finance_agents"):
        if not mongo_uri:
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        self._db = self._client[db_name]
        self._collection = self._db["users"]
        self._ensure_indexes()

    def _ensure_indexes(self):
        """Ensure unique indexes exist for username, email, and user_id."""
        try:
            self._collection.create_index([("user_id", ASCENDING)], unique=True)
            self._collection.create_index([("username", ASCENDING)], unique=True)
            self._collection.create_index([("email", ASCENDING)], unique=True)
        except Exception:
            # Avoid crashing if Mongo is temporarily unreachable during startup
            pass

    def create_user(self, user):
        """Persist a User entity to MongoDB."""
        user_doc = {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "password_hash": user.password_hash,
            "created_at": user.created_at,
        }
        self._collection.insert_one(user_doc)
        return user

    def get_by_id(self, user_id):
        """Retrieve a User by user_id."""
        doc = self._collection.find_one({"user_id": user_id})
        return self._to_entity(doc)

    def get_by_username(self, username):
        """Retrieve a User by username (case-insensitive search)."""
        doc = self._collection.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
        return self._to_entity(doc)

    def get_by_email(self, email):
        """Retrieve a User by email (case-insensitive search)."""
        doc = self._collection.find_one({"email": {"$regex": f"^{email}$", "$options": "i"}})
        return self._to_entity(doc)

    def _to_entity(self, doc):
        """Converts Mongo document to User domain entity."""
        if not doc:
            return None
        return User(
            user_id=doc.get("user_id"),
            username=doc.get("username"),
            email=doc.get("email"),
            password_hash=doc.get("password_hash"),
            created_at=doc.get("created_at"),
        )
