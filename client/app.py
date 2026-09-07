from PySide6.QtWidgets import QApplication
from client.views.login import LoginWindow
from client.views.signup import SignupWindow
from client.windows.main_windows import MainWindow
import sys

app = QApplication(sys.argv)

login_window = LoginWindow()
signup_window = SignupWindow()
main_window = None


def show_main_window(username):
    global main_window
    main_window = MainWindow()
    main_window.showMaximized()
    login_window.close()
    signup_window.close()


def show_signup_window():
    signup_window.username_input.clear()
    signup_window.email_input.clear()
    signup_window.password_input.clear()
    signup_window.confirm_password_input.clear()
    signup_window.error_label.hide()

    signup_window.showMaximized()
    login_window.close()


def show_login_window():
    login_window.username_input.clear()
    login_window.password_input.clear()
    login_window.error_label.hide()

    login_window.showMaximized()
    signup_window.close()


login_window.login_successful.connect(show_main_window)
signup_window.signup_successful.connect(show_main_window)

login_window.signup_link_button.clicked.connect(show_signup_window)
signup_window.login_link_button.clicked.connect(show_login_window)

login_window.showMaximized()

sys.exit(app.exec())