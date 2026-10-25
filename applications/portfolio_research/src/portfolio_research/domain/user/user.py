from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class User:
    user_id: str
    username: str
    email: str
    password_hash: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
