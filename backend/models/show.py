from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from datetime import date, time

from backend.database import Base

class show(Base):
    __tablename__ = "shows"

    show_id : Mapped[int] = mapped_column(
        primary_key = True,
        autoincrement = True
    )

    movie_id : Mapped[int] = mapped_column(
        ForeignKey("movies.movie_id"),
        nullable = False
    )

    screen_id : Mapped[int] = mapped_column(
        ForeignKey("screens.screen_id"),
        nullable = False
    )

    show_date : Mapped[date] = mapped_column(
        date,
        nullable = False
    )

    show_time : Mapped[time] = mapped_column(
        time,
        nullable = False
    )

