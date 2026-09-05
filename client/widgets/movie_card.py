from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
import hashlib

from client.models.movie import Movie

class MovieCard(QFrame):

    """ A card widget showing a movie's poster, title, rating, genre tags."""

    CARD_WIDGET = 200
    POSTER_HEIGHT = 240

    def __init__(self, movie:Movie):
        super().__init__()

        self.movie = movie

        self.setFixedWidth(self.CARD_WIDGET)
        self.setObjectName("movieCard")
        self.setStyleSheet("""
            #movieCard {
                background-color: rgba(255, 255, 255, 15);
                border-radius: 10px;
            }
            QLabel#titleLabel {
                color: white;
                font-size: 13px;
                font-weight: bold;
            }
            QLabel#ratingLabel {
                color: #ffd700;
                font-size: 12px;
            }
            QLabel#genreTag {
                color: white;
                background-color: rgba(255, 255, 255, 25);
                border-radius: 8px;
                padding: 2px 8px;
                font-size: 10px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8,8,8,8)
        layout.setSpacing(6)

        # -------------Poster------------

        self.poster_label = QLabel()
        self.poster_label.setFixedSize(self.CARD_WIDGET - 16, self.POSTER_HEIGHT)
        self.poster_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.poster_label.setWordWrap(True)
        self.poster_label.setText(movie.title)
        self.poster_label.setStyleSheet(f"""
            background-color: {self._placeholder_color(movie.title)};
            color: white;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px;
        """)

        # ---------Title--------

        title_label = QLabel(movie.title)
        title_label.setObjectName("titleLabel1")
        title_label.setWordWrap(True)

        # ----------Rating--------

        rating_label = QLabel(f"⭐️ {movie.rating:.1f}")
        rating_label.setObjectName("ratingLabel")

        # -------Genre tags-------

        genre_row = QHBoxLayout()
        genre_row.setSpacing(4)
        for genre in movie.genres:
            tag = QLabel(genre)
            tag.setObjectName("genreTag")
            genre_row.addWidget(tag)
        genre_row.addStretch()

        layout.addWidget(self.poster_label)
        layout.addWidget(title_label)
        layout.addWidget(rating_label)
        layout.addLayout(genre_row)

    @staticmethod
    def _placeholder_color(title: str) -> str:

        """Generate a consistent color per movie title, so placeholders look
           varied but same movies always gets the same color."""

        hash_value = int(hashlib.md5(title.encode()).hexdigest(), 16)
        hue = hash_value % 360
        return f"hsl{hue}, 45%, 35%"
