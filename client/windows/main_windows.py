from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Movie Ticket Booking System")

        central_widget = QWidget()

        layout = QVBoxLayout()

        label = QLabel("Welcome to Movie Ticket Booking")
        button = QPushButton("Get started")

        layout.addWidget(label, alignment = Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button, alignment = Qt.AlignmentFlag.AlignCenter)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
