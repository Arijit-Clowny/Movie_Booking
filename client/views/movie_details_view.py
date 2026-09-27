from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal

from client.models.movie import Movie
from client.widgets.movie_card import MovieCard


class MovieDetailsViews(QWidget):
    """Full details page for a single movie: poster, quick facts, synopsis,
    and cast. Reused across movies via set_movie(), rather
    than being recreated each time a card is clicked."""

    back_requested = Signal()
    book_requested = Signal(Movie)

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background: transparent;")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(30, 20, 30, 20)
        outer_layout.setSpacing(20)

        # -------Back button row-------
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

        # -------Scrollable content-------
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

        # -------Cast section (photo avatars)-------
        cast_heading = QLabel("Cast")
        cast_heading.setStyleSheet("""
            color: white; font-size: 18px; font-weight: bold;
            background: transparent;
        """)

        self.cast_row = QHBoxLayout()
        self.cast_row.setSpacing(20)
        self.cast_row.setAlignment(Qt.AlignmentFlag.AlignLeft)

        content_layout.addWidget(cast_heading)
        content_layout.addLayout(self.cast_row)

        # -------Crew section (plain text)-------
        crew_heading = QLabel("Crew")
        crew_heading.setStyleSheet("""
            color: white; font-size: 18px; font-weight: bold;
            background: transparent;
        """)

        self.crew_label = QLabel()
        self.crew_label.setStyleSheet("""
            color: rgba(255, 255, 255, 200); font-size: 14px;
            background: transparent;
        """)
        self.crew_label.setWordWrap(True)

        content_layout.addWidget(crew_heading)
        content_layout.addWidget(self.crew_label)

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

        # Clear old cast avatars before adding new ones
        while self.cast_row.count():
            item = self.cast_row.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if movie.cast:
            for name in movie.cast:
                self.cast_row.addWidget(self._build_cast_avatar(name))
        else:
            no_cast_label = QLabel("No cast information available.")
            no_cast_label.setStyleSheet("color: rgba(255,255,255,150); background: transparent;")
            self.cast_row.addWidget(no_cast_label)

        self.crew_label.setText(", ".join(movie.crew) if movie.crew else "No crew information available.")

    def _build_cast_avatar(self, name: str) -> QWidget:
        """Build a small circular avatar (initials, mock placeholder) + name
        label for one cast member. Will show a real photo (from TMDB's
        profile_path) once that data is wired in."""
        item_widget = QWidget()
        item_widget.setStyleSheet("background: transparent;")
        item_layout = QVBoxLayout(item_widget)
        item_layout.setSpacing(6)
        item_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        item_layout.setContentsMargins(0, 0, 0, 0)

        name_parts = name.split()
        initials = "".join(part[0] for part in name_parts[:2]).upper()

        avatar = QLabel(initials)
        avatar.setFixedSize(64, 64)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(f"""
            background-color: {MovieCard._placeholder_color(name)};
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 32px;
        """)

        name_label = QLabel(name)
        name_label.setFixedWidth(80)
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("""
            color: white; font-size: 11px; background: transparent;
        """)

        item_layout.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignCenter)
        item_layout.addWidget(name_label)

        return item_widget

    def _on_book_clicked(self):
        if self._current_movie is not None:
            self.book_requested.emit(self._current_movie)