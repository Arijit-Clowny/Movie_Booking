from sqlalchemy import URL,  create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.config import (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME
)

DATABASE_URL = URL.create(
    drivername = "mysql+pymysql",
    username = DB_USER,
    password = DB_PASSWORD,
    host = DB_HOST,
    port = int(DB_PORT),
    database = DB_NAME
)

engine = create_engine(
    DATABASE_URL,
    echo = True
)

SessionLocal = sessionmaker(
    bind = engine,
    autoflush = False,
    expire_on_commit = False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db =  SessionLocal()
    try:
        yield db
    finally:
        db.close()