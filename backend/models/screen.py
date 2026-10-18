from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base

class Screen(Base):
    __tablename__ = "screens"

    screen_id : Mapped[int] = mapped_column(
        primary_key = True,
        autoincrement = True
    )

    screen_name : Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    theatre_id : Mapped[int] = mapped_column(
        ForeignKey("theatres.theatre_id"),
        nullable = False
    )

    __table_args__ = (
        UniqueConstraint(
        "screen_id",
        "show_date",
        "show_time",
        name =  "unique_show_datetime"
        ),
    )