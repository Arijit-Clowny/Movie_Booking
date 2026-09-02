import sys
from PySide6.QtWidgets import *
from client.windows.main_windows import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
window.showMaximized()

sys.exit(app.exec())