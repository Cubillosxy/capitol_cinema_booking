from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserData:
    id: int
    username: str
    email: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
