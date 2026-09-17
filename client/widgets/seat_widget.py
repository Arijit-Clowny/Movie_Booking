from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, Signal

from client.models.seat import Seat


class SeatWidget(QPushButton):
    """A single clickable seat button. Visually reflects its state:
    available, selected, booked, or premium."""

    toggled_selection = Signal(Seat, bool)  # seat, now_selected

    AVAILABLE_STYLE = """
        QPushButton {
            background-color: rgba(255, 255, 255, 30);
            color: white;
            border: 1px solid rgba(255, 255, 255, 60);
            border-radius: 6px;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 60);
        }
    """

    PREMIUM_STYLE = """
        QPushButton {
            background-color: rgba(255, 215, 0, 40);
            color: white;
            border: 1px solid rgba(255, 215, 0, 100);
            border-radius: 6px;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: rgba(255, 215, 0, 80);
        }
    """

    SELECTED_STYLE = """
        QPushButton {
            background-color: rgba(90, 200, 90, 220);
            color: #111;
            border: 1px solid rgba(90, 200, 90, 255);
            border-radius: 6px;
            font-size: 11px;
            font-weight: bold;
        }
    """

    BOOKED_STYLE = """
        QPushButton {
            background-color: rgba(120, 120, 120, 80);
            color: rgba(255, 255, 255, 100);
            border: 1px solid rgba(120, 120, 120, 100);
            border-radius: 6px;
            font-size: 11px;
        }
    """

    def __init__(self, seat: Seat):
        super().__init__(seat.seat_id)

        self.seat = seat
        self.is_selected = False

        self.setFixedSize(36, 32)

        if seat.is_booked:
            self.setEnabled(False)
            self.setStyleSheet(self.BOOKED_STYLE)
            self.setCursor(Qt.CursorShape.ForbiddenCursor)
        else:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self._apply_unselected_style()
            self.clicked.connect(self._on_clicked)

    def _apply_unselected_style(self):
        if self.seat.section == "Premium":
            self.setStyleSheet(self.PREMIUM_STYLE)
        else:
            self.setStyleSheet(self.AVAILABLE_STYLE)

    def _on_clicked(self):
        self.is_selected = not self.is_selected

        if self.is_selected:
            self.setStyleSheet(self.SELECTED_STYLE)
        else:
            self._apply_unselected_style()

        self.toggled_selection.emit(self.seat, self.is_selected)