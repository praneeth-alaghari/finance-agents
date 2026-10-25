import os
from pymongo import MongoClient, ASCENDING
from portfolio_research.domain.user.user import User
from portfolio_research.repositories.user_repository import UserRepository


class MongoUserRepository(UserRepository):
    def __init__(self, mongo_uri=None, db_name="finance_agents"):
        uri = mongo_uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self._client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        self._collection = self._client[db_name]["users"]
        self._ensure_indexes()

    def _ensure_indexes(self):
        try:
            self._collection.create_index([("user_id", ASCENDING)], unique=True)
            self._collection.create_index([("username", ASCENDING)], unique=True)
            self._collection.create_index([("email", ASCENDING)], unique=True)
        except Exception:
            pass

    def create_user(self, user):
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
        doc = self._collection.find_one({"user_id": user_id})
        return self._to_entity(doc)

    def get_by_username(self, username):
        doc = self._collection.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
        return self._to_entity(doc)

    def get_by_email(self, email):
        doc = self._collection.find_one({"email": {"$regex": f"^{email}$", "$options": "i"}})
        return self._to_entity(doc)

    def _to_entity(self, doc):
        if not doc:
            return None
        return User(
            user_id=doc.get("user_id"),
            username=doc.get("username"),
            email=doc.get("email"),
            password_hash=doc.get("password_hash"),
            created_at=doc.get("created_at"),
        )
