from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal

from client.models.booking import Booking

class BookingConfirmationView(QWidget):
    # Shown after a successful bookig: summary details.

    done_requested  = Signal()

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background: transparent")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(30,20,30,20)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --------Confirmation card--------

        card = QFrame()
        card.setObjectName("confirmationCard")
        card.setFixedWidth(420)
        card.setStyleSheet(
            """
            #confirmationCard {
                background-color: rgba(0, 0, 0, 140);
                border-radius: 16px;
            }
            QLabel {
                color: white;
                background: transparent;
            }
            """
        )

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35,35,35,35)
        card_layout.setSpacing(10)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        checkmark = QLabel("✅")
        checkmark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        checkmark.setStyleSheet("font-size: 48px; background: transparent;")

        heading = QLabel("Booking Confirmed!")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setStyleSheet("font-size: 22px; font-weight: bold; background: transparent;")

        self.booking_id_label = QLabel()
        self.booking_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.booking_id_label.setStyleSheet("""
                    color: rgba(255, 255, 255, 160); font-size: 12px; background: transparent;
                """)

        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: rgba(255, 255, 255, 40);")

        self.details_label = QLabel()
        self.details_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.details_label.setWordWrap(True)
        self.details_label.setStyleSheet("font-size: 14px; background: transparent;")

        self.total_label = QLabel()
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_label.setStyleSheet("""
                    font-size: 18px; font-weight: bold; background: transparent;
                """)

        done_button = QPushButton("Back to Home")
        done_button.setCursor(Qt.CursorShape.PointingHandCursor)
        done_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(255, 255, 255, 220);
                        color: #111;
                        border: none;
                        border-radius: 8px;
                        padding: 12px;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 255);
                    }
                """)
        done_button.clicked.connect(self.done_requested.emit)

        card_layout.addWidget(checkmark)
        card_layout.addWidget(heading)
        card_layout.addWidget(self.booking_id_label)
        card_layout.addSpacing(10)
        card_layout.addWidget(divider)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.details_label)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.total_label)
        card_layout.addSpacing(15)
        card_layout.addWidget(done_button)

        outer_layout.addWidget(card)

    def set_booking(self, booking: Booking):
            # Populate the view with a completed booking's details.

            self.booking_id_label.setText(f"Booking ID: {booking.booking_id}")

            seat_ids = ', '.join(sorted(seat.seat_id for  seat in booking.seats))
            details_text = (
                f"<b>{booking.movie.title}<b><br>"
                f"{booking.theatre.name}<br>"
                f"{booking.theatre.location}<br>"
                f"Showtime: {booking.time_str}<br>"
                f"Seats: {seat_ids}"
            )
            self.details_label.setText(details_text)

            self.total_label.setText(f"Total Paid: ₹{booking.total_price:.2f}")