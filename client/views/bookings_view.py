from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from client.models.booking import Booking


class BookingsView(QWidget):
    """Shows the user's past bookings."""

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background: transparent;")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(30, 20, 30, 20)
        outer_layout.setSpacing(20)

        heading = QLabel("My Bookings")
        heading.setStyleSheet("""
            color: white; font-size: 22px; font-weight: bold;
            background: transparent;
        """)
        outer_layout.addWidget(heading)

        # -------Scrollable list-------
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

        self.list_container = QWidget()
        self.list_container.setStyleSheet("background: transparent;")
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setSpacing(15)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll_area.setWidget(self.list_container)
        outer_layout.addWidget(scroll_area)

        self.empty_label = QLabel("You haven't booked any tickets yet.")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("""
            color: rgba(255, 255, 255, 150); font-size: 14px;
            background: transparent;
        """)
        self.empty_label.hide()
        outer_layout.addWidget(self.empty_label)

    def set_bookings(self, bookings: list[Booking]):
        """Rebuild the list from the given bookings. Called every time this
        view is shown, so it always reflects the latest booking history."""
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not bookings:
            self.empty_label.show()
            return

        self.empty_label.hide()

        # Most recent booking first
        for booking in reversed(bookings):
            self.list_layout.addWidget(self._build_booking_card(booking))

    def _build_booking_card(self, booking: Booking) -> QWidget:
        card = QFrame()
        card.setObjectName("bookingCard")
        card.setStyleSheet("""
             #bookingCard {
                background-color: rgba(0, 0, 0, 90);
                border: 1px solid rgba(255, 255, 255, 25);
                border-radius: 10px;
            }
            QLabel {
                color: white;
                background: transparent;
            }
        """)

        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(18, 14, 18, 14)

        info_column = QVBoxLayout()
        info_column.setSpacing(4)

        title_label = QLabel(booking.movie.title)
        title_label.setStyleSheet("font-size: 15px; font-weight: bold; background: transparent;")

        seat_ids = ", ".join(sorted(seat.seat_id for seat in booking.seats))
        details_label = QLabel(
            f"{booking.theatre.name}  •  {booking.time_str}  •  Seats: {seat_ids}"
        )
        details_label.setStyleSheet("""
            color: rgba(255, 255, 255, 160); font-size: 12px; background: transparent;
        """)

        booking_id_label = QLabel(f"Booking ID: {booking.booking_id}")
        booking_id_label.setStyleSheet("""
            color: rgba(255, 255, 255, 120); font-size: 11px; background: transparent;
        """)

        info_column.addWidget(title_label)
        info_column.addWidget(details_label)
        info_column.addWidget(booking_id_label)

        price_label = QLabel(f"₹{booking.total_price:.2f}")
        price_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        price_label.setStyleSheet("""
            color: #ffd700; font-size: 16px; font-weight: bold; background: transparent;
        """)

        card_layout.addLayout(info_column)
        card_layout.addStretch()
        card_layout.addWidget(price_label)

        return card