from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal

from client.models.movie import Movie
from client.models.theatre import Theatre
from client.models.seat import Seat
from client.widgets.seat_widget import SeatWidget


class SeatSelectionView(QWidget):
    """Lets the user pick seats for a specific movie/theatre/showtime,
    and shows a running total based on selected seats."""

    back_requested = Signal()
    booking_confirmed = Signal(Movie, Theatre, str, list)  # movie, theatre, time, seats

    REGULAR_PRICE = 250.0
    PREMIUM_PRICE = 450.0

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background: transparent;")

        self._current_movie = None
        self._current_theatre = None
        self._current_time = None
        self._selected_seats = {}  # seat_id -> seat

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(30, 20, 30, 20)
        outer_layout.setSpacing(15)

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

        # -------Info heading-------
        self.info_label = QLabel()
        self.info_label.setStyleSheet("""
            color: white; font-size: 18px; font-weight: bold;
            background: transparent;
        """)
        outer_layout.addWidget(self.info_label)

        # -------Screen indicator-------
        screen_label = QLabel("🎬  SCREEN THIS WAY")
        screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        screen_label.setStyleSheet("""
            color: rgba(255, 255, 255, 150);
            font-size: 11px;
            letter-spacing: 2px;
            background: transparent;
            padding: 8px;
            border-bottom: 2px solid rgba(255, 255, 255, 60);
        """)
        outer_layout.addWidget(screen_label)

        # -------Scrollable seat grid-------
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

        self.seat_grid_widget = QWidget()
        self.seat_grid_widget.setStyleSheet("background: transparent;")
        self.seat_grid_layout = QVBoxLayout(self.seat_grid_widget)
        self.seat_grid_layout.setSpacing(8)
        self.seat_grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        scroll_area.setWidget(self.seat_grid_widget)
        outer_layout.addWidget(scroll_area)

        # -------Legend-------
        outer_layout.addWidget(self._build_legend())

        # -------Bottom bar: total price + confirm button-------
        bottom_bar = QFrame()
        bottom_bar.setObjectName("bottomBar")
        bottom_bar.setFixedHeight(70)
        bottom_bar.setStyleSheet("""
            #bottomBar {
                background-color: rgba(90, 20, 30, 160);
                border-radius: 10px;
            }
        """)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(20, 0, 20, 0)

        self.total_label = QLabel("Select seats to continue")
        self.total_label.setStyleSheet("""
            color: white; font-size: 15px; font-weight: bold;
            background: transparent;
        """)

        self.confirm_button = QPushButton("Confirm Booking")
        self.confirm_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.confirm_button.setEnabled(False)
        self.confirm_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 220);
                color: #111;
                border: none;
                border-radius: 8px;
                padding: 10px 22px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 255);
            }
            QPushButton:disabled {
                background-color: rgba(255, 255, 255, 60);
                color: rgba(255, 255, 255, 120);
            }
        """)
        self.confirm_button.clicked.connect(self._on_confirm_clicked)

        bottom_layout.addWidget(self.total_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.confirm_button)

        outer_layout.addWidget(bottom_bar)

    def _build_legend(self) -> QWidget:
        """Build a row of small colored swatches explaining seat states."""
        legend = QWidget()
        legend.setStyleSheet("background: transparent;")
        legend_layout = QHBoxLayout(legend)
        legend_layout.setSpacing(25)
        legend_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        items = [
            ("Regular", "rgba(255, 255, 255, 60)"),
            ("Premium", "rgba(255, 215, 0, 100)"),
            ("Selected", "rgba(90, 200, 90, 220)"),
            ("Booked", "rgba(120, 120, 120, 100)"),
        ]

        for label_text, color in items:
            item_layout = QHBoxLayout()
            item_layout.setSpacing(6)

            swatch = QFrame()
            swatch.setFixedSize(14, 14)
            swatch.setStyleSheet(f"background-color: {color}; border-radius: 3px;")

            text = QLabel(label_text)
            text.setStyleSheet("color: rgba(255,255,255,180); font-size: 11px; background: transparent;")

            item_layout.addWidget(swatch)
            item_layout.addWidget(text)
            legend_layout.addLayout(item_layout)

        return legend

    def set_booking_context(self, movie: Movie, theatre: Theatre, time_str: str):
        """Populate the view for a specific movie/theatre/showtime, generating
        a fresh mock seat layout."""
        self._current_movie = movie
        self._current_theatre = theatre
        self._current_time = time_str
        self._selected_seats = {}

        self.info_label.setText(f"{movie.title} - {theatre.name} - {time_str}")
        self._update_total()

        # Clear any previous seat rows
        while self.seat_grid_layout.count():
            item = self.seat_grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        seats = self._generate_mock_seats()

        rows = {}
        for seat in seats:
            rows.setdefault(seat.row, []).append(seat)

        for row_letter in sorted(rows.keys()):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(6)

            row_label = QLabel(row_letter)
            row_label.setFixedWidth(20)
            row_label.setStyleSheet("color: white; font-size: 12px; background: transparent;")
            row_layout.addWidget(row_label)

            for seat in rows[row_letter]:
                seat_widget = SeatWidget(seat)
                seat_widget.toggled_selection.connect(self._on_seat_toggled)
                row_layout.addWidget(seat_widget)

            self.seat_grid_layout.addLayout(row_layout)

    def _generate_mock_seats(self) -> list[Seat]:
        """Build an 8-row x 10-seat layout: rows A-B are Premium, C-H are Regular.
        A few random seats are marked booked for realism."""
        import random

        premium_rows = ["A", "B"]
        regular_rows = ["C", "D", "E", "F", "G", "H"]
        all_rows = premium_rows + regular_rows

        booked_seat_ids = set(random.sample(
            [f"{r}{n}" for r in all_rows for n in range(1, 11)],
            k=8  # roughly 10% of 80 seats pre-booked
        ))

        seats = []
        for row in all_rows:
            section = "Premium" if row in premium_rows else "Regular"
            price = self.PREMIUM_PRICE if section == "Premium" else self.REGULAR_PRICE
            for number in range(1, 11):
                seat = Seat(row=row, number=number, section=section, price=price)
                if seat.seat_id in booked_seat_ids:
                    seat.is_booked = True
                seats.append(seat)

        return seats

    def _on_seat_toggled(self, seat: Seat, is_selected: bool):
        if is_selected:
            self._selected_seats[seat.seat_id] = seat
        else:
            self._selected_seats.pop(seat.seat_id, None)
        self._update_total()

    def _update_total(self):
        count = len(self._selected_seats)

        if count == 0:
            self.total_label.setText("Select seats to continue")
            self.confirm_button.setEnabled(False)
            return

        total_price = sum(seat.price for seat in self._selected_seats.values())
        seat_ids = ", ".join(sorted(self._selected_seats.keys()))
        self.total_label.setText(f"{count} seat(s): {seat_ids}  —  ₹{total_price:.2f}")
        self.confirm_button.setEnabled(True)

    def _on_confirm_clicked(self):
        selected_list = list(self._selected_seats.values())
        self.booking_confirmed.emit(
            self._current_movie, self._current_theatre, self._current_time, selected_list
        )