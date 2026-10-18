from sqlalchemy import ForeignKey, Float, UniqueConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from backend.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    booking_id : Mapped[int] = mapped_column(
        primary_key = True,
        autoincrement = True
    )

    user_id : Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable = False
    )

    show_id : Mapped[int] = mapped_column(
        ForeignKey("shows.show_id"),
        nullable = False
    )

    seat_id : Mapped[int] = mapped_column(
        ForeignKey("seats.seat_id"),
        nullable = False
    )

    booking_time : Mapped[datetime] = mapped_column(
        DateTime,
        nullable = False
    )

    total_amt :  Mapped[float] = mapped_column(
        Float,
        nullable = False
    )

    __table_args__ = (
        UniqueConstraint(
            "show_id",
            "seat_id",
            name = "unique_show_seat"
        ),
    )