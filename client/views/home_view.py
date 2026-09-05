from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

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
            Movie(title="Inception", rating=8.8, genres=["Sci-Fi", "Thriller"]),
            Movie(title="The Dark Knight", rating=9.0, genres=["Action", "Crime"]),
            Movie(title="Interstellar", rating=8.6, genres=["Sci-Fi", "Drama"]),
            Movie(title="Parasite", rating=8.5, genres=["Thriller", "Drama"]),
            Movie(title="Dune: Part Two", rating=8.4, genres=["Sci-Fi", "Adventure"]),
            Movie(title="Oppenheimer", rating=8.3, genres=["Biography", "Drama"]),
            Movie(title="Spirited Away", rating=8.6, genres=["Animation", "Fantasy"]),
            Movie(title="The Matrix", rating=8.7, genres=["Sci-Fi", "Action"]),
        ]

        for movie in mock_movies:
            card = MovieCard(movie)
            self.row_layout.addWidget(card)