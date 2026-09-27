from client.models.movie import Movie


def get_all_movies() -> list[Movie]:
    """Returns the shared mock movie catalog. Used by both HomeView and
    MoviesView so they stay in sync. Will be replaced by a real TMDB-backed
    service later."""
    return [
        Movie(
            title="Inception", rating=8.8, genres=["Sci-Fi", "Thriller"],
            language="English", duration_minutes=148,
            synopsis="A skilled thief who steals corporate secrets through dream-sharing technology is given a chance at redemption if he can plant an idea into a target's subconscious.",
            cast=["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
            crew=["Christopher Nolan (Director)"],
            showtimes=["2:00 PM", "5:30 PM", "9:00 PM"],
        ),
        Movie(
            title="The Dark Knight", rating=9.0, genres=["Action", "Crime"],
            language="English", duration_minutes=152,
            synopsis="When a mysterious criminal mastermind known as the Joker unleashes chaos on Gotham, Batman must confront one of the greatest psychological tests of his ability to fight injustice.",
            cast=["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
            crew=["Christopher Nolan (Director)"],
            showtimes=["1:00 PM", "4:30 PM", "8:00 PM"],
        ),
        Movie(
            title="Interstellar", rating=8.6, genres=["Sci-Fi", "Drama"],
            language="English", duration_minutes=169,
            synopsis="With Earth becoming uninhabitable, a group of explorers undertake a mission through a wormhole in search of a new home for humanity, testing the limits of time and love.",
            cast=["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
            crew=["Christopher Nolan (Director)"],
            showtimes=["12:30 PM", "4:00 PM", "7:45 PM"],
        ),
        Movie(
            title="Parasite", rating=8.5, genres=["Thriller", "Drama"],
            language="Korean", duration_minutes=132,
            synopsis="Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
            cast=["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong"],
            crew=["Bong Joon-ho (Director)"],
            showtimes=["3:00 PM", "6:15 PM", "9:30 PM"],
        ),
        Movie(
            title="Dune: Part Two", rating=8.4, genres=["Sci-Fi", "Adventure"],
            language="English", duration_minutes=166,
            synopsis="Paul Atreides unites with the Fremen to seek revenge against the conspirators who destroyed his family, facing a choice between the love of his life and the fate of the known universe.",
            cast=["Timothée Chalamet", "Zendaya", "Rebecca Ferguson"],
            crew=["Denis Villeneuve (Director)"],
            showtimes=["1:30 PM", "5:00 PM", "8:30 PM"],
        ),
        Movie(
            title="Oppenheimer", rating=8.3, genres=["Biography", "Drama"],
            language="English", duration_minutes=180,
            synopsis="The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.",
            cast=["Cillian Murphy", "Emily Blunt", "Robert Downey Jr."],
            crew=["Christopher Nolan (Director)"],
            showtimes=["11:30 AM", "3:30 PM", "7:30 PM"],
        ),
        Movie(
            title="Spirited Away", rating=8.6, genres=["Animation", "Fantasy"],
            language="Japanese", duration_minutes=125,
            synopsis="During her family's move to a new neighborhood, a sullen ten-year-old girl wanders into a world ruled by gods, witches, and spirits, where humans are changed into beasts.",
            cast=["Rumi Hiiragi", "Miyu Irino", "Mari Natsuki"],
            crew=["Hayao Miyazaki (Director)"],
            showtimes=["2:15 PM", "5:45 PM"],
        ),
        Movie(
            title="The Matrix", rating=8.7, genres=["Sci-Fi", "Action"],
            language="English", duration_minutes=136,
            synopsis="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
            cast=["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
            crew=["Lana Wachowski (Director)", "Lilly Wachowski (Director)"],
            showtimes=["12:00 PM", "3:15 PM", "6:45 PM", "10:00 PM"],
        ),
    ]