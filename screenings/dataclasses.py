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
    is_full: bool


@dataclass
class SeatData:
    available_seats: int
    reserved_seats: int
    is_full: bool
    cinema: CinemaData
