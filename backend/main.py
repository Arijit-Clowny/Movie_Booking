from fastapi  import FastAPI
from sqlalchemy import  text

from backend.database import Base, engine
from backend.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Movie Ticket Booking API",
    version = "1.0.0"
)

@app.get("/")
def root():
    return {"message": "Movie Ticket Booking API  is running"}

@app.get("/db-test")
def test_database():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        return {
            "database": "connected",
            "result":  result.scalar()
        }