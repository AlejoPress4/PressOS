import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout, QSizePolicy, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
import re

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Otter Browser')
        self.setGeometry(100, 100, 1200, 800)

        # Main container
        main_container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header with logo and title
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap('./graphic_resources/icons/Otter_Browser.png')
        scaled_pixmap = logo_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Title
        title_label = QLabel('Otter Browser')
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #333;
            }
        """)
        title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Navigation bar
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(5)
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self.search_button = QPushButton('↵')
        self.search_button.clicked.connect(self.navigate_to_url)
        
        self.back_button = QPushButton('<')
        self.forward_button = QPushButton('>')
        self.reload_button = QPushButton('⟳')
        
        buttons = [self.search_button, self.back_button, self.forward_button, self.reload_button]
        for button in buttons:
            button.setFixedSize(40, 40)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        nav_layout.addWidget(self.url_bar)
        for button in buttons:
            nav_layout.addWidget(button)

        # Web view container
        web_container = QWidget()
        web_layout = QVBoxLayout()
        web_layout.setContentsMargins(0, 10, 0, 0)
        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://otter-browser.org/"))
        self.browser.loadFinished.connect(self.update_url)

        # Add all layouts to main layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.browser)

        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        # Connect buttons after browser is defined
        self.back_button.clicked.connect(self.browser.back)
        self.forward_button.clicked.connect(self.browser.forward)
        self.reload_button.clicked.connect(self.browser.reload)

        # Add all layouts to main layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(web_container)

        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }

            QLineEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 20px;
                padding: 5px 15px;
                font-size: 14px;
                min-height: 40px;
            }

            QPushButton {
                background-color: #1e90ff;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                min-width: 40px;
                min-height: 40px;
            }

            QPushButton:hover {
                background-color: #187bcd;
            }

            #search_button {
                background-color: #4CAF50;
            }

            #search_button:hover {
                background-color: #45a049;
            }

            QWebEngineView {
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        self.browser.setUrl(QUrl(url))
        
    def update_url(self, _):
        self.url_bar.setText(self.browser.url().toString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())