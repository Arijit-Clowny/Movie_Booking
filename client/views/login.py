from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
from client.windows.main_windows import MainWindow

class LoginWindow(QMainWindow):
    login_successful = Signal(str) #emits username on success.

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Movie Ticket Booking System - Login")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # -------Background Image (reusing MainWindow's blur logic)-------

        self.background = QLabel(central_widget)
        self.background.setScaledContents(False)
        self.background.lower()

        self._bg_pixmap = MainWindow._load_blurred_pixmap(
            "/Users/arijitshaw/Python_projects/Movie_ticket/client/resource/Background.jpg", blur_radius=10
        )
        if self._bg_pixmap.isNull():
            print("Failed to load background image.")

        #--------Center The Login Card--------

        outer_layer = QVBoxLayout(central_widget)
        outer_layer.setContentsMargins(0,0,0,0)
        outer_layer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_card = QWidget()
        login_card.setObjectName(("loginCard"))
        login_card.setFixedWidth(360)

        login_card.setStyleSheet("""
            #loginCard{
            background-color: rgba(0,0,0,140);
            border-radius: 14px;
            }
            QLabel {
                color: white;
                background: transparent;
            }
            QLabel#titleLabel {
                font-size: 22px;
                font-weight: bold;
            }
            QLabel#subtitleLabel {
                font-size: 12px;
                color: rgba(255, 255, 255, 160);
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 25);
                color: white;
                border: 1px solid rgba(255, 255, 255, 60);
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(255, 255, 255, 140);
            }
            QPushButton#loginButton {
                background-color: rgba(255, 255, 255, 220);
                color: #111;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#loginButton:hover {
                background-color: rgba(255, 255, 255, 255);
            }
            QLabel#errorLabel {
                color: #ff6b6b;
                font-size: 12px;
            }
            QPushButton#linkButton {
                background: transparent;
                border: none;
                color: rgba(255, 255, 255, 180);
                font-size: 12px;
                text-decoration: underline;
            }
        """)

        card_layout = QVBoxLayout(login_card)
        card_layout.setContentsMargins(30,30,30,30)

        card_layout.setSpacing(12)

        title = QLabel("🎬 Welcome Back")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Log in to book your tickets")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.hide()

        login_button = QPushButton("Log In")
        login_button.setObjectName("loginButton")
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        login_button.clicked.connect(self._handel_login)

        signup_button = QPushButton("Don't have an account? Sign up")
        signup_button.setObjectName("linkButton")
        signup_button.setCursor(Qt.CursorShape.PointingHandCursor)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.error_label)
        card_layout.addWidget(login_button)

        card_layout.addWidget(
            signup_button,
            alignment = Qt.AlignmentFlag.AlignCenter
        )

        outer_layer.addWidget(login_card)

        self.password_input.returnPressed.connect(self._handel_login)
        self.resize(1000,700)

    def _handel_login(self):
            username = self.username_input.text().strip()
            password = self.password_input.text()

            if not username or not password:
                self.error_label.setText(
                    "Please enter both username and paassword."
                )
                self.error_label.show()
                return

            is_valid = self._authenticate(username,password)

            if is_valid:
                self.error_label.hide()
                self.login_successful.emit(username)
            else:
                self.error_label.setText(
                    "Invalid username or password."
                )
                self.error_label.show()

    def _authenticate(self ,username: str ,password: str, )->bool:
        """Placeholder authentication logic — wire this up to your backend."""
        return bool(username and password)

    def resizeEvent(self, event):
        # Reusing MainWindow's geometry-update logic (works because both
        # windows share the same self.background / self._bg_pixmap / self.centralWidget() shape)
        MainWindow._update_background_geometry(self)
        super().resizeEvent(event)



