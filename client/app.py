from PySide6.QtWidgets import QApplication
from client.views.login import LoginWindow
from client.windows.main_windows import MainWindow
import sys

app = QApplication(sys.argv)

login_window = LoginWindow()
main_window = None  # created only after successful login

def on_login_success(username):
    global main_window
    main_window = MainWindow()
    main_window.showMaximized()
    login_window.close()

login_window.login_successful.connect(on_login_success)
login_window.showMaximized()

sys.exit(app.exec())