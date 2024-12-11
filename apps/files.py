import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTreeView, QFileSystemModel, 
                             QVBoxLayout, QHBoxLayout, QWidget, QMenu, QAction, QMessageBox, QFileDialog,
                             QLineEdit, QPushButton, QLabel, QSplitter)
from PyQt5.QtCore import QDir, Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from kernel.modules.config.functions import press_os

class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Obtener el sistema y el usuario actual
        self.sistema = press_os()
        self.current_user = self.sistema.get_current_user()
        
        # Configurar la ventana
        self.setWindowTitle(f'Gestor de Archivos - {self.current_user.get_username()}')
        self.setGeometry(300, 300, 1000, 700)

        # Configurar el modelo de sistema de archivos
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        
        # Establecer el directorio raíz del usuario
        self.user_directory = self.current_user.get_user_path()

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Crear la barra de herramientas
        toolbar_layout = QHBoxLayout()
        self.path_input = QLineEdit(self.user_directory)
        self.path_input.returnPressed.connect(self.navigate_to_path)
        go_button = QPushButton("Ir")
        go_button.clicked.connect(self.navigate_to_path)
        toolbar_layout.addWidget(QLabel("Ruta:"))
        toolbar_layout.addWidget(self.path_input)
        toolbar_layout.addWidget(go_button)

        main_layout.addLayout(toolbar_layout)

        # Crear el árbol de vista
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.user_directory))
        
        # Configurar columnas y menú contextual
        self.tree.setColumnWidth(0, 250)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.open_context_menu)

        # Crear un QSplitter para permitir redimensionar las columnas
        splitter = QSplitter()
        splitter.addWidget(self.tree)

        main_layout.addWidget(splitter)

        # Configurar widget central
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.apply_styles()

    def navigate_to_path(self):
        path = self.path_input.text()
        if os.path.exists(path):
            self.tree.setRootIndex(self.model.index(path))
        else:
            QMessageBox.warning(self, 'Error', 'La ruta especificada no existe.')

    def open_context_menu(self, position):
        indexes = self.tree.selectedIndexes()
        if indexes:
            file_path = self.model.filePath(indexes[0])
            menu = QMenu()

            # Acción de Abrir
            open_action = QAction(QIcon.fromTheme("document-open"), "Abrir", self)
            open_action.triggered.connect(lambda: self.open_file(file_path))
            menu.addAction(open_action)

            # Acción de Eliminar
            delete_action = QAction(QIcon.fromTheme("edit-delete"), "Eliminar", self)
            delete_action.triggered.connect(lambda: self.delete_file(file_path))
            menu.addAction(delete_action)

            # Acción de Nuevo archivo
            new_file_action = QAction(QIcon.fromTheme("document-new"), "Nuevo Archivo", self)
            new_file_action.triggered.connect(lambda: self.create_new_file(file_path))
            menu.addAction(new_file_action)

            # Acción de Nueva carpeta
            new_folder_action = QAction(QIcon.fromTheme("folder-new"), "Nueva Carpeta", self)
            new_folder_action.triggered.connect(lambda: self.create_new_folder(file_path))
            menu.addAction(new_folder_action)

            menu.exec_(self.tree.viewport().mapToGlobal(position))

    def open_file(self, file_path):
        if os.path.isfile(file_path):
            os.startfile(file_path)
        else:
            QMessageBox.warning(self, 'Error', 'No se puede abrir el archivo.')

    def delete_file(self, file_path):
        try:
            # Confirmación de eliminación
            reply = QMessageBox.question(self, 'Confirmar', 
                                         '¿Está seguro que desea eliminar este archivo/carpeta?',
                                         QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
                
                QMessageBox.information(self, 'Éxito', 'Archivo/Carpeta eliminado correctamente.')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'No se pudo eliminar: {e}')

    def create_new_file(self, current_path):
        # Si es un archivo, usar su directorio padre
        if os.path.isfile(current_path):
            current_path = os.path.dirname(current_path)
        
        # Diálogo para nombrar el archivo
        file_name, ok = QFileDialog.getSaveFileName(self, "Crear Nuevo Archivo", 
                                                    current_path, 
                                                    "Todos los archivos (*.*)")
        
        if ok:
            try:
                with open(file_name, 'w') as f:
                    pass  # Crear archivo vacío
                QMessageBox.information(self, 'Éxito', f'Archivo {file_name} creado.')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'No se pudo crear el archivo: {e}')

    def create_new_folder(self, current_path):
        # Si es un archivo, usar su directorio padre
        if os.path.isfile(current_path):
            current_path = os.path.dirname(current_path)
        
        # Diálogo para nombrar la carpeta
        folder_name = QFileDialog.getExistingDirectory(self, "Crear Nueva Carpeta", current_path)
        
        if folder_name:
            try:
                os.makedirs(folder_name)
                QMessageBox.information(self, 'Éxito', f'Carpeta {folder_name} creada.')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'No se pudo crear la carpeta: {e}')

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTreeView {
                background-color: white;
                border: 1px solid #d0d0d0;
                font-size: 14px;
            }
            QTreeView::item {
                padding: 5px;
            }
            QTreeView::item:hover {
                background-color: #e6f3ff;
            }
            QTreeView::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 5px 10px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
            QLabel {
                font-size: 14px;
            }
            QMenu {
                background-color: white;
                border: 1px solid #d0d0d0;
            }
            QMenu::item {
                padding: 5px 20px 5px 20px;
            }
            QMenu::item:selected {
                background-color: #0078d7;
                color: white;
            }
        """)

def main():
    app = QApplication(sys.argv)
    file_manager = FileManager()
    file_manager.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()