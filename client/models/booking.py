from dataclasses import dataclass, field

from client.models.movie import Movie
from client.models.theatre import Theatre
from client.models.seat import Seat

@dataclass
class Booking:
    movie: Movie
    theatre: Theatre
    time_str: str
    seats: list[Seat] = field(default_factory=list)
    booking_id: str = ""

    @property
    def total_price(self) -> float:
        return sum(seat.price for seat in self.seats)
