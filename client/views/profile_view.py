from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal

from client.models.user import User
from client.models.booking import Booking


class ProfileView(QWidget):
    """Shows the logged-in user's info and booking stats."""

    logout_requested = Signal()

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background: transparent;")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(30, 30, 30, 30)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        outer_layout.setSpacing(25)

        heading = QLabel("Profile")
        heading.setStyleSheet("""
            color: white; font-size: 22px; font-weight: bold;
            background: transparent;
        """)
        outer_layout.addWidget(heading)

        # -------Profile card: avatar + name + email-------
        profile_card = QFrame()
        profile_card.setObjectName("profileCard")
        profile_card.setStyleSheet("""
            #profileCard {
                background-color: rgba(0, 0, 0, 90);
                border: 1px solid rgba(255, 255, 255, 25);
                border-radius: 14px;
            }
            QLabel {
                color: white;
                background: transparent;
            }
        """)

        profile_layout = QHBoxLayout(profile_card)
        profile_layout.setContentsMargins(25, 25, 25, 25)
        profile_layout.setSpacing(20)

        avatar_label = QLabel("👤")
        avatar_label.setFixedSize(70, 70)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_label.setStyleSheet("""
            background-color: rgba(90, 20, 30, 160);
            border-radius: 35px;
            font-size: 32px;
        """)

        details_column = QVBoxLayout()
        details_column.setSpacing(4)

        self.username_label = QLabel()
        self.username_label.setStyleSheet("font-size: 18px; font-weight: bold; background: transparent;")

        self.email_label = QLabel()
        self.email_label.setStyleSheet("""
            color: rgba(255, 255, 255, 160); font-size: 13px; background: transparent;
        """)

        details_column.addWidget(self.username_label)
        details_column.addWidget(self.email_label)
        details_column.addStretch()

        profile_layout.addWidget(avatar_label)
        profile_layout.addLayout(details_column)
        profile_layout.addStretch()

        outer_layout.addWidget(profile_card)

        # -------Stats row-------
        stats_row = QHBoxLayout()
        stats_row.setSpacing(15)

        self.total_bookings_stat = self._build_stat_card("Total Bookings", "0")
        self.total_spent_stat = self._build_stat_card("Total Spent", "₹0.00")

        stats_row.addWidget(self.total_bookings_stat)
        stats_row.addWidget(self.total_spent_stat)

        outer_layout.addLayout(stats_row)

        # -------Logout button-------
        logout_button = QPushButton("Log Out")
        logout_button.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        logout_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(255, 255, 255, 30);
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 60);
            }
        """)
        logout_button.clicked.connect(self.logout_requested.emit)
        outer_layout.addWidget(logout_button)

        outer_layout.addStretch()

    def _build_stat_card(self, label_text: str, value_text: str) -> QFrame:
        card = QFrame()
        card.setObjectName("statCard")
        card.setStyleSheet("""
            #statCard {
                background-color: rgba(0, 0, 0, 50);
                border: 1px solid rgba(255, 255, 255, 25);
                border-radius: 12px;
            }
            QLabel {
                color: white;
                background: transparent;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(4)

        value_label = QLabel(value_text)
        value_label.setObjectName("statValue")
        value_label.setStyleSheet("font-size: 22px; font-weight: bold; background: transparent;")

        label_label = QLabel(label_text)
        label_label.setStyleSheet("""
            color: rgba(255, 255, 255, 160); font-size: 12px; background: transparent;
        """)

        card_layout.addWidget(value_label)
        card_layout.addWidget(label_label)

        card._value_label = value_label  # keep a reference so set_user can update it later
        return card

    def set_user(self, user: User, bookings: list[Booking]):
        """Populate the view with the current user and their booking stats."""
        self.username_label.setText(user.username)
        self.email_label.setText(user.email)

        total_bookings = len(bookings)
        total_spent = sum(booking.total_price for booking in bookings)

        self.total_bookings_stat._value_label.setText(str(total_bookings))
        self.total_spent_stat._value_label.setText(f"₹{total_spent:.2f}")