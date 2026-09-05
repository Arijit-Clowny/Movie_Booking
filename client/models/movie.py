from dataclasses import dataclass,field

@dataclass # Generates __init__ and all parameters automatically.
class Movie:
    title: str
    rating: float
    genres: list[str] = field(default_factory = list) # Calls list fresh for every movie.
    poster_path: str | None = None # Will hold a TMDB image URL/path later.

