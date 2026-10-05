from sqlalchemy import String, Text, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base

class Movies(Base):
    __tablename__ = "movies"

    movie_id: Mapped[int] = mapped_column(
        primary_key = True,
        autoincrement = True
    )

    tmdb_id: Mapped[int] = mapped_column(
        unique = True,
        nullable = False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable = False
    )

    poster_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable = False
    )

    duration: Mapped[int | None] = mapped_column(
        Integer,
        nullable = True
    )

    rating: Mapped[float | None] = mapped_column(
        Float,
        nullable = True
    )

