from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserData:
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    date_joined: datetime | None
