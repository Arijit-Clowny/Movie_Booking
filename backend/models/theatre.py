from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base

class Theatre(Base):
    __tablename__ = "theatres"

    theatre_id : Mapped[int] =  mapped_column(
        primary_key = True,
        autoincrement =  True
    )

    theatre_name : Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    theatre_location : Mapped[str] = mapped_column(
        String(400),
        nullable = False
    )
