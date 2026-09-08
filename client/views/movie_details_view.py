from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal

from client.models.movie import Movie
from client.widgets.movie_card import MovieCard

class MovieDetailsViews(QWidget):

    """Full details page for a single movie: poster, quick facts, synopsis,
        cast/crew, and showtimes. Reused across movies via set_movie(), rather
        than being recreated each time a card is clicked."""

    back_requested = Signal()   # User clicked the back button.
    book_requested = Signal(Movie)

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background: transparent;")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(30,20,30,20)
        outer_layout.setSpacing(20)

        # ------Back button row------

        back_row = QHBoxLayout()
        back_button = QPushButton("⬅ Back")
        back_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(255, 255, 255, 30);
                border: none;
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 60);
            }
        """)
        back_button.clicked.connect(self.back_requested.emit)

        back_row.addWidget(back_button)
        back_row.addStretch()
        outer_layout.addLayout(back_row)

        # --------Scrollable Content--------

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

        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(25)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # -------Top section: poster (left) + quick facts (right)-------
        top_row = QHBoxLayout()
        top_row.setSpacing(30)
        top_row.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.poster_label = QLabel()
        self.poster_label.setFixedSize(260, 380)
        self.poster_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.poster_label.setWordWrap(True)

        facts_column = QVBoxLayout()
        facts_column.setSpacing(10)
        facts_column.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("""
                    color: white; font-size: 28px; font-weight: bold;
                    background: transparent;
                """)
        self.title_label.setWordWrap(True)

        self.rating_label = QLabel()
        self.rating_label.setStyleSheet("""
                    color: #ffd700; font-size: 16px; background: transparent;
                """)

        self.language_label = QLabel()
        self.language_label.setStyleSheet("""
                    color: white; font-size: 14px; background: transparent;
                """)

        self.duration_label = QLabel()
        self.duration_label.setStyleSheet("""
                    color: white; font-size: 14px; background: transparent;
                """)

        book_button = QPushButton("Book Tickets")
        book_button.setCursor(Qt.CursorShape.PointingHandCursor)
        book_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(255, 255, 255, 220);
                        color: #111;
                        border: none;
                        border-radius: 8px;
                        padding: 12px 20px;
                        font-size: 15px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 255);
                    }
                """)
        book_button.clicked.connect(self._on_book_clicked)
        self._book_button = book_button

        facts_column.addWidget(self.title_label)
        facts_column.addWidget(self.rating_label)
        facts_column.addWidget(self.language_label)
        facts_column.addWidget(self.duration_label)
        facts_column.addSpacing(15)
        facts_column.addWidget(book_button)
        facts_column.addStretch()

        top_row.addWidget(self.poster_label)
        top_row.addLayout(facts_column)
        top_row.addStretch()

        content_layout.addLayout(top_row)

        # -------Synopsis section-------
        synopsis_heading = QLabel("Synopsis")
        synopsis_heading.setStyleSheet("""
                    color: white; font-size: 18px; font-weight: bold;
                    background: transparent;
                """)

        self.synopsis_label = QLabel()
        self.synopsis_label.setStyleSheet("""
                    color: rgba(255, 255, 255, 200); font-size: 14px;
                    background: transparent;
                """)
        self.synopsis_label.setWordWrap(True)

        content_layout.addWidget(synopsis_heading)
        content_layout.addWidget(self.synopsis_label)

        # -------Cast & Crew section-------
        cast_heading = QLabel("Cast & Crew")
        cast_heading.setStyleSheet("""
                    color: white; font-size: 18px; font-weight: bold;
                    background: transparent;
                """)

        self.cast_crew_label = QLabel()
        self.cast_crew_label.setStyleSheet("""
                    color: rgba(255, 255, 255, 200); font-size: 14px;
                    background: transparent;
                """)
        self.cast_crew_label.setWordWrap(True)

        content_layout.addWidget(cast_heading)
        content_layout.addWidget(self.cast_crew_label)

        # -------Showtimes section-------
        showtimes_heading = QLabel("Showtimes")
        showtimes_heading.setStyleSheet("""
                    color: white; font-size: 18px; font-weight: bold;
                    background: transparent;
                """)

        self.showtimes_row = QHBoxLayout()
        self.showtimes_row.setSpacing(10)

        content_layout.addWidget(showtimes_heading)
        content_layout.addLayout(self.showtimes_row)

        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        outer_layout.addWidget(scroll_area)

        self._current_movie = None

    def set_movie(self, movie: Movie):
        """Populate the view with a specific movie's data. Called every time
        the user navigates here, instead of creating a new view per movie."""
        self._current_movie = movie

        self.poster_label.setText(movie.title)
        self.poster_label.setStyleSheet(f"""
                    background-color: {MovieCard._placeholder_color(movie.title)};
                    color: white;
                    font-size: 20px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 15px;
                """)

        self.title_label.setText(movie.title)
        self.rating_label.setText(f"⭐ {movie.rating:.1f} / 10")
        self.language_label.setText(f"🗣️ {movie.language}")

        hours = movie.duration_minutes // 60
        minutes = movie.duration_minutes % 60
        self.duration_label.setText(f"⏱️ {hours}h {minutes}m")

        self.synopsis_label.setText(movie.synopsis or "No synopsis available.")

        cast_crew_text = ""
        if movie.cast:
            cast_crew_text += "Cast: " + ", ".join(movie.cast)
        if movie.crew:
            if cast_crew_text:
                cast_crew_text += "\n"
            cast_crew_text += "Crew: " + ", ".join(movie.crew)
        self.cast_crew_label.setText(cast_crew_text or "No cast/crew info available.")

        # Clear old showtime buttons before adding new ones
        while self.showtimes_row.count():
            item = self.showtimes_row.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if movie.showtimes:
            for time_str in movie.showtimes:
                time_button = QPushButton(time_str)
                time_button.setCursor(Qt.CursorShape.PointingHandCursor)
                time_button.setStyleSheet("""
                            QPushButton {
                                color: white;
                                background-color: rgba(255, 255, 255, 30);
                                border: none;
                                border-radius: 6px;
                                padding: 8px 16px;
                                font-size: 13px;
                            }
                            QPushButton:hover {
                                background-color: rgba(255, 255, 255, 60);
                            }
                        """)
                self.showtimes_row.addWidget(time_button)
        else:
            no_shows_label = QLabel("No showtimes available.")
            no_shows_label.setStyleSheet("color: rgba(255,255,255,150); background: transparent;")
            self.showtimes_row.addWidget(no_shows_label)

        self.showtimes_row.addStretch()

    def _on_book_clicked(self):
        if self._current_movie is not None:
            self.book_requested.emit(self._current_movie)