from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base

class Seat(Base):
    __tablename__ = "seats"

    seat_id : Mapped[int] = mapped_column(
        primary_key = True,
        autoincrement = True
    )

    screen_id  :  Mapped[int] = mapped_column(
        ForeignKey("screens.screen_id"),
        nullable = False
    )

    row : Mapped[str] = mapped_column(
        String(5),
        nullable = False
    )

    seat_number : Mapped[str] = mapped_column(
        String(10),
        nullable = False,
    )

    seat_type : Mapped[str] = mapped_column(
        String(20),
        nullable = False
    )

    __table_args__ =  (
        UniqueConstraint("screen_id", "seat_number"),
    )