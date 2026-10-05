from sqlalchemy import ForeignKey, String
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