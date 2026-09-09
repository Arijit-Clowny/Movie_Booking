from PySide6.QtWidgets import *
from PySide6.QtCore import Qt,Signal

from client.models.movie import Movie
from client.models.theatre import Theatre

class TheatreSelectionView(QWidget):
    """Lets the user pick a theatre and showtime for a specific movie."""

    back_requested = Signal()
    showtime_selected = Signal(Movie, Theatre, str) # movie, theatre, chosen time.

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background: transparent")
        self._current_movie = None

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(30,20,30,20)
        outer_layout.setSpacing(20)

        # ------Back Button------

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

        # ------Movie title heading------

        self.movie_title_label = QLabel()
        self.movie_title_label.setStyleSheet("""
            color: white; font-size: 22px; font-weight: bold;
            background: transparent;
        """)
        outer_layout.addWidget(self.movie_title_label)

        subtitle = QLabel("Select a theatre and showtime")
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 160); font-size: 13px;
            background: transparent;
        """)
        outer_layout.addWidget(subtitle)

        # -------Scrollable list of theatre cards-------

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

        self.theatre_list_widget = QWidget()
        self.theatre_list_widget.setStyleSheet("background: transparent;")
        self.theatre_list_layout = QVBoxLayout(self.theatre_list_widget)
        self.theatre_list_layout.setSpacing(15)
        self.theatre_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll_area.setWidget(self.theatre_list_widget)
        outer_layout.addWidget(scroll_area)

    def set_movie(self, movie: Movie, theatres: list[Theatre]):
        """Populate the view with a movie and the list of theatres showing it."""
        self._current_movie = movie
        self.movie_title_label.setText(movie.title)

        # Clear any previously shown theatre cards
        while self.theatre_list_layout.count():
            item = self.theatre_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for theatre in theatres:
            self.theatre_list_layout.addWidget(self._build_theatre_card(theatre))

    def _build_theatre_card(self, theatre: Theatre) -> QWidget:
        """Build a card for one theatre showing its name, location, and
        clickable showtime buttons."""
        card = QFrame()
        card.setObjectName("theatreCard")
        card.setStyleSheet("""
            #theatreCard {
                background-color: rgba(255, 255, 255, 15);
                border-radius: 10px;
            }
            QLabel#theatreName {
                color: white;
                font-size: 15px;
                font-weight: bold;
                background: transparent;
            }
            QLabel#theatreLocation {
                color: rgba(255, 255, 255, 160);
                font-size: 12px;
                background: transparent;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(8)

        name_label = QLabel(theatre.name)
        name_label.setObjectName("theatreName")

        location_label = QLabel(theatre.location)
        location_label.setObjectName("theatreLocation")

        showtimes_row = QHBoxLayout()
        showtimes_row.setSpacing(10)

        if theatre.showtimes:
            for time_str in theatre.showtimes:
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
                # Default-argument trick to correctly capture the current
                # loop values (theatre, time_str) for each button's click
                time_button.clicked.connect(
                    lambda checked=False, t=theatre, ts=time_str: self._on_showtime_clicked(t, ts)
                )
                showtimes_row.addWidget(time_button)
        else:
            no_shows_label = QLabel("No showtimes available.")
            no_shows_label.setStyleSheet("color: rgba(255,255,255,120); background: transparent;")
            showtimes_row.addWidget(no_shows_label)

        showtimes_row.addStretch()

        card_layout.addWidget(name_label)
        card_layout.addWidget(location_label)
        card_layout.addLayout(showtimes_row)

        return card

    def _on_showtime_clicked(self, theatre: Theatre, time_str: str):
        if self._current_movie is not None:
            self.showtime_selected.emit(self._current_movie, theatre, time_str)
