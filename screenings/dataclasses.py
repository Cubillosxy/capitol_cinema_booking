from dataclasses import dataclass
from datetime import datetime

from cinemas.dataclasses import CinemaData
from movies.dataclasses import MovieData


@dataclass
class ScreeningData:
    id: int
    movie: MovieData
    movie_id: int
    cinema: CinemaData
    cinema_id: int
    date: datetime
    price: float
    is_dubbed: bool
    is_subtitled: bool
    is_disabled: bool
    created_at: datetime
    available_seats: int
    reserved_seats: int
    is_full: bool


@dataclass
class SeatData:
    id: int
    screening: ScreeningData
    screening_id: int
    booking_id: int | None
    number: int
    is_reserved: bool
    created_at: datetime | None
    updated_at: datetime | None
