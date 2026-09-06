from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
from client.windows.main_windows import MainWindow

class SignupWindow(QMainWindow):
    signup_successful = Signal(str)   #emit username on success

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Movie Ticket Booking System - Sign Up")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.color_overlay = QFrame(central_widget)
        self.color_overlay.setStyleSheet(f"background-color : {MainWindow.WINE_RED};")

        # ------------Background Image------------

        self.background = QLabel(central_widget)
        self.background.setScaledContents(False)
        self.background.lower()

        self._bg_pixmap = MainWindow._load_blurred_pixmap(
            "/Users/arijitshaw/Python_projects/Movie_ticket/client/resource/Background.jpg",
            blur_radius=4
        )
        if self._bg_pixmap.isNull():
            print("Failed to load background image.")

        # ---------Center The Signup Card----------

        outer_layout = QVBoxLayout(central_widget)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        signup_card = QWidget()
        signup_card.setObjectName("signupCard")
        signup_card.setFixedWidth(360)
        signup_card.setStyleSheet("""
                    #signupCard {
                        background-color: rgba(0, 0, 0, 140);
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
                    QPushButton#signupButton {
                        background-color: rgba(255, 255, 255, 220);
                        color: #111;
                        border: none;
                        border-radius: 6px;
                        padding: 10px;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton#signupButton:hover {
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

        card_layout = QVBoxLayout(signup_card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(12)

        title = QLabel("🎬 Create Account")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Sign up to start booking tickets")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.hide()

        signup_button = QPushButton("Sign Up")
        signup_button.setObjectName("signupButton")
        signup_button.setCursor(Qt.CursorShape.PointingHandCursor)
        signup_button.clicked.connect(self._handle_signup)

        self.login_link_button = QPushButton("Already have an account? Log in")
        self.login_link_button.setObjectName("linkButton")
        self.login_link_button.setCursor(Qt.CursorShape.PointingHandCursor)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.confirm_password_input)
        card_layout.addWidget(self.error_label)
        card_layout.addWidget(signup_button)
        card_layout.addWidget(
            self.login_link_button,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        outer_layout.addWidget(signup_card)

        self.confirm_password_input.returnPressed.connect(self._handle_signup)
        self.resize(1000, 700)

    def _handle_signup(self):

        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.password_input.text()

        if not username or not email or not password or not confirm_password:
            self.error_label.setText("Please fill in all fields.")
            self.error_label.show()
            return

        if "@" not in email or "." not in email:
            self.error_label.setText("Please enter a valid email address.")
            self.error_label.show()
            return

        if password != confirm_password:
            self.error_label.setText("Passwords do not match.")
            self.error_label.show()
            return

        if len(password) < 6:
            self.error_label.setText("Password must be at least 6 characters.")
            self.error_label.show()
            return

            # TODO: replace with real signup logic (API call / DB insert)
        self.error_label.hide()
        self.signup_successful.emit(username)

    def resizeEvent(self, event):
        MainWindow._update_background_geometry(self)
        super().resizeEvent(event)

