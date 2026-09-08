from PySide6.QtWidgets import *
from PySide6.QtCore import Qt,Signal

from client.models.movie import Movie
from client.widgets.movie_card import MovieCard


class HomeView(QWidget):
    """The home screen content: a horizontally scrollable row of movie cards
    plus a quote banner below it."""

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background: transparent;")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(60, 30, 60, 30)
        outer_layout.setSpacing(50)

        section_label = QLabel("Now Showing")
        section_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
            background: transparent;
        """)
        outer_layout.addWidget(section_label)

        # -------Scroll area holding a single row of movie cards-------
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFixedHeight(MovieCard.POSTER_HEIGHT + 120)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:horizontal {
                background: transparent;
                height: 10px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(255, 255, 255, 60);
                border-radius: 5px;
            }
        """)

        row_container = QWidget()
        row_container.setStyleSheet("background: transparent;")
        self.row_layout = QHBoxLayout(row_container)
        self.row_layout.setSpacing(20)
        self.row_layout.setContentsMargins(0, 0, 0, 0)
        self.row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        scroll_area.setWidget(row_container)
        outer_layout.addWidget(scroll_area)

        outer_layout.addSpacing(40)

        # -------Quote banner-------
        outer_layout.addWidget(self._build_quote_banner())

        outer_layout.addStretch()

        self._load_mock_movies()

    def _build_quote_banner(self) -> QWidget:
        """Build a translucent banner displaying an inspirational cinema quote."""
        banner = QFrame()
        banner.setObjectName("quoteBanner")
        banner.setFixedHeight(160)
        banner.setStyleSheet("""
            #quoteBanner {
                background-color: rgba(90, 20, 30, 190);
                border-radius: 14px;
                border: 1px solid rgba(90, 20, 30, 220);
            }
            QLabel#quoteText {
                color: white;
                font-size: 26px;
                font-style: italic;
                background: transparent;
            }
            QLabel#quoteAuthor {
                color: rgba(255, 255, 255, 160);
                font-size: 12px;
                background: transparent;
            }
        """)

        banner_layout = QVBoxLayout(banner)
        banner_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner_layout.setSpacing(6)

        quote_text = QLabel("\u201cEvery great story deserves a great seat.\u201d")
        quote_text.setObjectName("quoteText")
        quote_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quote_text.setWordWrap(False)

        quote_author = QLabel("— Movie Booking")
        quote_author.setObjectName("quoteAuthor")
        quote_author.setAlignment(Qt.AlignmentFlag.AlignCenter)

        banner_layout.addWidget(quote_text)
        banner_layout.addWidget(quote_author)

        return banner

    def _load_mock_movies(self):
        """Populate the row with placeholder movie data.
        Will be replaced with real TMDB data later."""
        mock_movies = [
            Movie(
                title="Inception",
                rating=8.8,
                genres=["Sci-Fi", "Thriller"],
                language="English",
                duration_minutes=148,
                synopsis="A skilled thief who steals corporate secrets through dream-sharing technology is given a chance at redemption if he can plant an idea into a target's subconscious.",
                cast=["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
                crew=["Christopher Nolan (Director)"],
                showtimes=["2:00 PM", "5:30 PM", "9:00 PM"],
            ),
            Movie(
                title="The Dark Knight",
                rating=9.0,
                genres=["Action", "Crime"],
                language="English",
                duration_minutes=152,
                synopsis="When a mysterious criminal mastermind known as the Joker unleashes chaos on Gotham, Batman must confront one of the greatest psychological tests of his ability to fight injustice.",
                cast=["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
                crew=["Christopher Nolan (Director)"],
                showtimes=["1:00 PM", "4:30 PM", "8:00 PM"],
            ),
            Movie(
                title="Interstellar",
                rating=8.6,
                genres=["Sci-Fi", "Drama"],
                language="English",
                duration_minutes=169,
                synopsis="With Earth becoming uninhabitable, a group of explorers undertake a mission through a wormhole in search of a new home for humanity, testing the limits of time and love.",
                cast=["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
                crew=["Christopher Nolan (Director)"],
                showtimes=["12:30 PM", "4:00 PM", "7:45 PM"],
            ),
            Movie(
                title="Parasite",
                rating=8.5,
                genres=["Thriller", "Drama"],
                language="Korean",
                duration_minutes=132,
                synopsis="Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
                cast=["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong"],
                crew=["Bong Joon-ho (Director)"],
                showtimes=["3:00 PM", "6:15 PM", "9:30 PM"],
            ),
            Movie(
                title="Dune: Part Two",
                rating=8.4,
                genres=["Sci-Fi", "Adventure"],
                language="English",
                duration_minutes=166,
                synopsis="Paul Atreides unites with the Fremen to seek revenge against the conspirators who destroyed his family, facing a choice between the love of his life and the fate of the known universe.",
                cast=["Timothée Chalamet", "Zendaya", "Rebecca Ferguson"],
                crew=["Denis Villeneuve (Director)"],
                showtimes=["1:30 PM", "5:00 PM", "8:30 PM"],
            ),
            Movie(
                title="Oppenheimer",
                rating=8.3,
                genres=["Biography", "Drama"],
                language="English",
                duration_minutes=180,
                synopsis="The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.",
                cast=["Cillian Murphy", "Emily Blunt", "Robert Downey Jr."],
                crew=["Christopher Nolan (Director)"],
                showtimes=["11:30 AM", "3:30 PM", "7:30 PM"],
            ),
            Movie(
                title="Spirited Away",
                rating=8.6,
                genres=["Animation", "Fantasy"],
                language="Japanese",
                duration_minutes=125,
                synopsis="During her family's move to a new neighborhood, a sullen ten-year-old girl wanders into a world ruled by gods, witches, and spirits, where humans are changed into beasts.",
                cast=["Rumi Hiiragi", "Miyu Irino", "Mari Natsuki"],
                crew=["Hayao Miyazaki (Director)"],
                showtimes=["2:15 PM", "5:45 PM"],
            ),
            Movie(
                title="The Matrix",
                rating=8.7,
                genres=["Sci-Fi", "Action"],
                language="English",
                duration_minutes=136,
                synopsis="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
                cast=["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
                crew=["Lana Wachowski (Director)", "Lilly Wachowski (Director)"],
                showtimes=["12:00 PM", "3:15 PM", "6:45 PM", "10:00 PM"],
            ),
        ]

        for movie in mock_movies:
            card = MovieCard(movie)
            card.clicked.connect(self._on_movie_clicked)
            self.row_layout.addWidget(card)

    movie_selected = Signal(Movie)  # add this near the top of the class, e.g. right after class HomeView(QWidget):

    def _on_movie_clicked(self, movie: Movie):
        self.movie_selected.emit(movie)