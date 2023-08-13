from dataclasses import dataclass


@dataclass
class MovieData:
    id: int
    title: str
    genre: str
    duration: int
    created_at: str
    is_disabled: bool
