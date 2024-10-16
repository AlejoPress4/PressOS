import sys
import os
import psutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QTableWidget, QTableWidgetItem, QTabWidget, 
                             QHeaderView)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot

class AdvancedTaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Tareas Avanzado")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow, QTableWidget, QTabWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTableWidget {
                gridline-color: #2d2d2d;
                border: none;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #3d3d3d;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Crear pestañas
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Pestaña de procesos
        processes_tab = QWidget()
        processes_layout = QVBoxLayout(processes_tab)
        self.processes_table = QTableWidget()
        self.processes_table.setColumnCount(5)
        self.processes_table.setHorizontalHeaderLabels(["PID", "Nombre", "CPU %", "Memoria %", "Hilos"])
        self.processes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        processes_layout.addWidget(self.processes_table)
        self.tab_widget.addTab(processes_tab, "Procesos")

        # Timer para actualizar la lista de procesos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_process_list)
        self.timer.start(2000)  # Actualizar cada 2 segundos

        self.update_process_list()

    @pyqtSlot()
    def update_process_list(self):
        self.processes_table.setRowCount(0)
        project_path = os.path.dirname(os.path.abspath(__file__))

        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'num_threads', 'exe']):
            try:
                if process.info['exe'] and project_path in process.info['exe']:
                    row_position = self.processes_table.rowCount()
                    self.processes_table.insertRow(row_position)
                    self.processes_table.setItem(row_position, 0, QTableWidgetItem(str(process.info['pid'])))
                    self.processes_table.setItem(row_position, 1, QTableWidgetItem(process.info['name']))
                    self.processes_table.setItem(row_position, 2, QTableWidgetItem(f"{process.info['cpu_percent']:.2f}"))
                    self.processes_table.setItem(row_position, 3, QTableWidgetItem(f"{process.info['memory_percent']:.2f}"))
                    self.processes_table.setItem(row_position, 4, QTableWidgetItem(str(process.info['num_threads'])))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    task_manager = AdvancedTaskManager()
    task_manager.show()
    sys.exit(app.exec_())