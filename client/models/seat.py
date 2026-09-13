from dataclasses import dataclass

@dataclass
class Seat:
    row: str        # e,g,"A" , "B", ....
    number: int     # e.g. 1 to 10
    section: str    # Premium or Regular
    price: float
    is_booked: bool = False

    @property
    def seat_id(self) -> str:
        """ Human-readable identifier, e.g. 'A5'. """
        return f"{self.row}{self.number}"