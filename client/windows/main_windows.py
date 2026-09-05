from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PIL import Image, ImageFilter


class MainWindow(QMainWindow):

    WINE_RED = "rgba(90, 20, 30, 110)"

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Movie Ticket Booking System")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.color_overlay = QFrame(central_widget)
        self.color_overlay.setStyleSheet(f"background-color: {self.WINE_RED};")

        self.background = QLabel(central_widget)
        self.background.setScaledContents(False)
        self.background.lower()

        self._bg_pixmap = self._load_blurred_pixmap(
            "/Users/arijitshaw/Python_projects/Movie_ticket/client/resource/Background.jpg",
            blur_radius=4
        )

        if self._bg_pixmap.isNull():
            print("Failed to load background image.")

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # -------Header Bar-------
        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")
        header_widget.setStyleSheet("""
            #headerWidget {
                background-color: rgba(90, 20, 30, 160);
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
            QPushButton {
                color: white;
                background-color: rgba(255, 255, 255, 30);
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 60);
            }
        """)

        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(15, 10, 15, 10)

        logo = QLabel("🎬 Movie Booking")

        home_button = QPushButton("Home")
        movies_button = QPushButton("Movies")
        bookings_button = QPushButton("My Bookings")
        profile_button = QPushButton("👤")

        header_layout.addWidget(logo)
        header_layout.addStretch()
        header_layout.addWidget(home_button)
        header_layout.addWidget(movies_button)
        header_layout.addWidget(bookings_button)
        header_layout.addWidget(profile_button)

        main_layout.addWidget(header_widget)
        main_layout.setAlignment(header_widget, Qt.AlignmentFlag.AlignTop)

        from client.views.home_view import HomeView
        self.home_view = HomeView()
        main_layout.addWidget(self.home_view)

        # -------Footer Bar-------
        footer_widget = self._build_footer()
        main_layout.addWidget(footer_widget)

        self.resize(1000, 700)

    def _build_footer(self) -> QWidget:
        """Build the translucent wine-red footer bar shown at the bottom of the window."""
        footer_widget = QWidget()
        footer_widget.setObjectName("footerWidget")
        footer_widget.setFixedHeight(50)
        footer_widget.setStyleSheet("""
            #footerWidget {
                background-color: rgba(90, 20, 30, 160);
            }
            QLabel {
                color: rgba(255, 255, 255, 180);
                font-size: 12px;
                background: transparent;
            }
        """)

        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(15, 0, 15, 0)

        copyright_label = QLabel("© 2026 Movie Booking. All rights reserved.")

        footer_layout.addWidget(copyright_label)
        footer_layout.addStretch()

        return footer_widget

    @staticmethod
    def _load_blurred_pixmap(path: str, blur_radius: int = 10) -> QPixmap:
        """Load an image from disk, blur it with Pillow, and return it as a QPixmap.
        Shared by any window that wants the same blurred-background look."""
        try:
            pil_image = Image.open(path).convert("RGBA")
        except (FileNotFoundError, OSError) as e:
            print(f"Could not open image at '{path}': {e}")
            return QPixmap()

        blurred = pil_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        data = blurred.tobytes("raw", "RGBA")
        qimage = QImage(
            data, blurred.width, blurred.height, QImage.Format.Format_RGBA8888
        )
        return QPixmap.fromImage(qimage)

    def _update_background_geometry(self):
        """Rescale and reposition self.background (and the color overlay on top of it)
        to fill the window. Shared logic any window with these attributes can call."""
        if not self._bg_pixmap.isNull():
            scaled_pixmap = self._bg_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self.background.setPixmap(scaled_pixmap)
            self.background.setGeometry(self.centralWidget().rect())

        if hasattr(self, "color_overlay"):
            self.color_overlay.setGeometry(self.centralWidget().rect())

    def resizeEvent(self, event):
        self._update_background_geometry()
        super().resizeEvent(event)