from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal

from client.models.movie import Movie
from client.widgets.movie_card import MovieCard
from client.services.mock_movie_data import get_all_movies


class MoviesView(QWidget):
    """Full browsable grid of all movies."""

    movie_selected = Signal(Movie)

    COLUMNS = 5

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background: transparent;")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(30, 20, 30, 20)
        outer_layout.setSpacing(20)

        heading = QLabel("All Movies")
        heading.setStyleSheet("""
            color: white; font-size: 22px; font-weight: bold;
            background: transparent;
        """)
        outer_layout.addWidget(heading)

        # -------Scrollable grid-------
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical { background: transparent; width: 10px; }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 60);
                border-radius: 5px;
            }
        """)

        grid_container = QWidget()
        grid_container.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(grid_container)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        scroll_area.setWidget(grid_container)
        outer_layout.addWidget(scroll_area)

        self._load_movies()

    def _load_movies(self):
        movies = get_all_movies()

        for index, movie in enumerate(movies):
            row = index // self.COLUMNS
            col = index % self.COLUMNS
            card = MovieCard(movie)
            card.clicked.connect(self.movie_selected.emit)
            self.grid_layout.addWidget(card, row, col)