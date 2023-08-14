from dataclasses import dataclass
from datetime import datetime

from screenings.dataclasses import ScreeningData, SeatData
from users.dataclasses import UserData


@dataclass
class BookingData:
    id: int
    user_id: int
    screening_id: int
    is_cancelled: bool
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None
    user: UserData
    screening: ScreeningData
    seats: list[SeatData]
