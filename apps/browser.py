import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QTabWidget, QLabel, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt, QSize
from PyQt5.QtGui import QPixmap

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Otter Browser')
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)  # Set minimum window size for responsiveness
        self.initUI()

    def initUI(self):
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
        nav_layout.setSpacing(8)  # Adjusted spacing between buttons
        
        # Navigation buttons container
        nav_buttons_layout = QHBoxLayout()
        nav_buttons_layout.setSpacing(8)
        
        self.back_button = QPushButton('<')
        self.forward_button = QPushButton('>')
        self.reload_button = QPushButton('⟳')
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Add navigation buttons
        nav_buttons = [self.back_button, self.forward_button, self.reload_button]
        for button in nav_buttons:
            button.setFixedSize(40, 40)
            nav_buttons_layout.addWidget(button)
        
        nav_layout.addLayout(nav_buttons_layout)
        nav_layout.addWidget(self.url_bar)

        # Tab widget for multiple pages
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Add tab button
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.setFixedSize(40, 40)
        self.add_tab_button.clicked.connect(self.add_new_tab)
        nav_layout.addWidget(self.add_tab_button)

        # Add all layouts to main layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.tabs)

        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        # Connect buttons
        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)
        self.reload_button.clicked.connect(self.reload_page)

        # Add first tab
        self.add_new_tab("https://otter-browser.org/")

        self.apply_styles()

    def add_new_tab(self, url=None):
        browser = QWebEngineView()
        
        # Configure web settings
        settings = browser.settings()
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        
        # Create and set custom web page
        page = QWebEnginePage()
        browser.setPage(page)

        if url:
            browser.setUrl(QUrl(url))
        
        # Set size policy for responsive behavior
        browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))
        browser.loadFinished.connect(lambda _, i=index, browser=browser: self.update_title(i, browser))
        
        return browser

    def update_url(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def update_title(self, i, browser):
        if browser != self.tabs.widget(i):
            return
        title = browser.page().title()
        self.tabs.setTabText(i, title[:30] + '...' if len(title) > 30 else title)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.add_new_tab()

    def navigate_to_url(self):
        url = self.url_bar.text()
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url))
            
    # def navigate_to_url(self):
    #     url = self.url_bar.text()
    #     if not url.startswith(('http://', 'https://')):
    #         url = 'http://' + url
    #     print(f"Navigating to: {url}")  # Debugging print
    #     current_browser = self.tabs.currentWidget()
    #     if current_browser:
    #         current_browser.setUrl(QUrl(url))

    def go_back(self):
        if self.tabs.currentWidget():
            self.tabs.currentWidget().back()

    def go_forward(self):
        if self.tabs.currentWidget():
            self.tabs.currentWidget().forward()

    def reload_page(self):
        if self.tabs.currentWidget():
            self.tabs.currentWidget().reload()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Add responsive adjustments here if needed

    def apply_styles(self):
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

            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }

            QTabBar::tab {
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                border-bottom-color: #ddd;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 5px;
                min-width: 100px;
            }

            QTabBar::tab:selected, QTabBar::tab:hover {
                background-color: #fff;
            }

            QTabBar::tab:selected {
                border-color: #9B9B9B;
                border-bottom-color: #fff;
            }

            QWebEngineView {
                background-color: white;
                border: none;
            }
        """)

if __name__ == '__main__':
    # Enable High DPI display
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())

