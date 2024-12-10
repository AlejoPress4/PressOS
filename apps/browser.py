import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from styles import apply_styles, browserST

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Otter Browser')
        self.setGeometry(100, 100, 1200, 800)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://otter-browser.org/"))

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.back_button = QPushButton('<')
        self.back_button.clicked.connect(self.browser.back)

        self.forward_button = QPushButton('>')
        self.forward_button.clicked.connect(self.browser.forward)

        self.reload_button = QPushButton('⟳')
        self.reload_button.clicked.connect(self.browser.reload)

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.url_bar)
        top_layout.addWidget(self.back_button)
        top_layout.addWidget(self.forward_button)
        top_layout.addWidget(self.reload_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        # Apply styles
        apply_styles(self, browserST)

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())