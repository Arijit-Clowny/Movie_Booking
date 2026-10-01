from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base

class User(Base):
    __tablename__  = "users"

    id: Mapped[int] = mapped_column(
    primary_key = True,
    autoincrement = True
    )

    name:  Mapped[str] = mapped_column(
        String(100),
        nullable = False
    )

    email: Mapped[str]  = mapped_column(
        String(255),
        nullable = False,
        unique =  True,
        index = True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default = func.now()
    )