from dataclasses import dataclass


@dataclass
class CinemaData:
    id: int
    name: str
    city: str
    is_disabled: bool
    capacity: int
    created_at: str
