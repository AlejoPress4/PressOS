import sys
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListView, QTreeView, QFileSystemModel, QToolBar, QAction, 
                             QInputDialog, QMessageBox, QLineEdit, QMenu, QSplitter)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDir, QUrl
from PyQt5.QtGui import QDesktopServices
from kernel.modules.config.functions import press_os

class FileManager(QMainWindow):
    def __init__(self, press_os_instance):
        super().__init__()
        self.press_os_instance = press_os_instance
        self.current_path = self.press_os_instance.get_current_user_directory()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Administrador de Archivos')
        self.setGeometry(100, 100, 800, 600)

        # Toolbar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Back action
        back_action = QAction(QIcon.fromTheme('go-previous'), 'Back', self)
        back_action.triggered.connect(self.go_back)
        self.toolbar.addAction(back_action)

        # Forward action
        forward_action = QAction(QIcon.fromTheme('go-next'), 'Forward', self)
        forward_action.triggered.connect(self.go_forward)
        self.toolbar.addAction(forward_action)

        # Up action
        up_action = QAction(QIcon.fromTheme('go-up'), 'Up', self)
        up_action.triggered.connect(self.go_up)
        self.toolbar.addAction(up_action)

        # Address bar
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.navigate_to_path)
        self.toolbar.addWidget(self.address_bar)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search...')
        self.search_bar.returnPressed.connect(self.search_files)
        self.toolbar.addWidget(self.search_bar)

        # Splitter for tree view and list view
        splitter = QSplitter(Qt.Horizontal)
        layout = QVBoxLayout()
        layout.addWidget(splitter)

        # Tree view
        self.tree_view = QTreeView()
        self.tree_model = QFileSystemModel()
        self.tree_model.setRootPath('')
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setRootIndex(self.tree_model.index(self.current_path))
        self.tree_view.clicked.connect(self.tree_item_clicked)
        splitter.addWidget(self.tree_view)

        # List view
        self.list_view = QListView()
        self.list_model = QFileSystemModel()
        self.list_model.setRootPath('')
        self.list_view.setModel(self.list_model)
        self.list_view.setRootIndex(self.list_model.index(self.current_path))
        self.list_view.doubleClicked.connect(self.list_item_double_clicked)
        self.list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.show_context_menu)
        splitter.addWidget(self.list_view)

        # Central widget and layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Status bar
        self.statusBar().showMessage('Ready')

        self.update_address_bar()

    def update_address_bar(self):
        self.address_bar.setText(self.current_path)

    def navigate_to_path(self):
        path = self.address_bar.text()
        if os.path.exists(path):
            self.current_path = path
            self.list_view.setRootIndex(self.list_model.index(path))
            self.update_address_bar()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid path')

    def go_back(self):
        # Implement back functionality
        pass

    def go_forward(self):
        # Implement forward functionality
        pass

    def go_up(self):
        parent = os.path.dirname(self.current_path)
        if parent != self.current_path:
            self.current_path = parent
            self.list_view.setRootIndex(self.list_model.index(parent))
            self.update_address_bar()

    def tree_item_clicked(self, index):
        path = self.tree_model.filePath(index)
        self.current_path = path
        self.list_view.setRootIndex(self.list_model.index(path))
        self.update_address_bar()

    def list_item_double_clicked(self, index):
        path = self.list_model.filePath(index)
        if os.path.isdir(path):
            self.current_path = path
            self.list_view.setRootIndex(index)
            self.update_address_bar()
        else:
            # Open file with default application
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def show_context_menu(self, position):
        menu = QMenu()
        new_file_action = menu.addAction("New File")
        new_folder_action = menu.addAction("New Folder")
        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")
        
        action = menu.exec_(self.list_view.mapToGlobal(position))
        
        if action == new_file_action:
            self.create_new_file()
        elif action == new_folder_action:
            self.create_new_folder()
        elif action == rename_action:
            self.rename_item()
        elif action == delete_action:
            self.delete_item()

    def create_new_file(self):
        file_name, ok = QInputDialog.getText(self, "New File", "Enter file name:")
        if ok and file_name:
            file_path = os.path.join(self.current_path, file_name)
            with open(file_path, 'w') as f:
                pass
            self.list_model.setRootPath('')

    def create_new_folder(self):
        folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        if ok and folder_name:
            folder_path = os.path.join(self.current_path, folder_name)
            os.makedirs(folder_path)
            self.list_model.setRootPath('')

    def rename_item(self):
        index = self.list_view.currentIndex()
        if not index.isValid():
            return
        old_path = self.list_model.filePath(index)
        new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:")
        if ok and new_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            os.rename(old_path, new_path)
            self.list_model.setRootPath('')

    def delete_item(self):
        index = self.list_view.currentIndex()
        if not index.isValid():
            return
        file_path = self.list_model.filePath(index)
        reply = QMessageBox.question(self, 'Delete', f"Are you sure you want to delete {file_path}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if os.path.isdir(file_path):
                os.rmdir(file_path)
            else:
                os.remove(file_path)
            self.list_model.setRootPath('')

    def search_files(self):
        search_term = self.search_bar.text()
        if search_term:
            # Implement file search functionality
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    press_os_instance = press_os()
    if press_os_instance.login("Press", "0424"):  # Ejemplo de login
        file_manager = FileManager(press_os_instance)
        file_manager.show()
        sys.exit(app.exec_())