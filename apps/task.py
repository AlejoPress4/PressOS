import sys
import psutil
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QListWidget, QListWidgetItem, QTabWidget, 
                             QProgressBar, QLineEdit, QComboBox, QSlider, QCheckBox)
from PyQt5.QtGui import QIcon, QFont, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QLineSeries, QValueAxis

class SystemMonitor(QThread):
    update_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            data = {
                'cpu': cpu_percent,
                'memory': memory.percent,
                'disk': disk.percent,
                'network_sent': network.bytes_sent,
                'network_recv': network.bytes_recv
            }
            
            self.update_signal.emit(data)
            time.sleep(1)

    def stop(self):
        self.running = False

class ProcessItem(QWidget):
    def __init__(self, process):
        super().__init__()
        self.process = process
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.name_label = QLabel(self.process.name())
        self.cpu_label = QLabel(f"CPU: {self.process.cpu_percent()}%")
        self.memory_label = QLabel(f"RAM: {self.process.memory_percent():.2f}%")
        self.pid_label = QLabel(f"PID: {self.process.pid}")

        layout.addWidget(self.name_label)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)
        layout.addWidget(self.pid_label)

        self.setLayout(layout)

    def update_info(self):
        self.cpu_label.setText(f"CPU: {self.process.cpu_percent()}%")
        self.memory_label.setText(f"RAM: {self.process.memory_percent():.2f}%")

class CustomProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setTextVisible(False)
        self.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 20px;
            }
        """)

class AdvancedTaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.system_monitor = SystemMonitor()
        self.system_monitor.update_signal.connect(self.update_system_info)
        self.system_monitor.start()

    def initUI(self):
        self.setWindowTitle('Task Manager Avanzado')
        self.setGeometry(100, 100, 1200, 800)

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Left panel (navigation)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.create_nav_buttons(left_layout)
        main_layout.addWidget(left_panel, 1)

        # Right panel (content)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.create_content_area(right_layout)
        main_layout.addWidget(right_panel, 4)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #34495e;
                color: #ecf0f1;
                border: none;
                padding: 10px;
                margin: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4a6b8a;
            }
            QLabel {
                color: #ecf0f1;
            }
            QListWidget {
                background-color: #34495e;
                color: #ecf0f1;
                border: none;
                border-radius: 5px;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background-color: #34495e;
                color: #ecf0f1;
                padding: 10px;
                margin-right: 5px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #4a6b8a;
            }
        """)

        self.process_list = []
        self.update_process_list()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_process_list)
        self.timer.start(800)  # Update every 5 seconds

    def create_nav_buttons(self, layout):
        buttons = ['Resumen', 'Procesos', 'Rendimiento', 'Aplicaciones', 'Usuarios']
        for button_text in buttons:
            button = QPushButton(button_text)
            button.clicked.connect(self.change_view)
            layout.addWidget(button)

    def create_content_area(self, layout):
        self.content_tabs = QTabWidget()
        self.content_tabs.setTabPosition(QTabWidget.West)

        # Summary tab
        summary_tab = QWidget()
        summary_layout = QVBoxLayout(summary_tab)
        self.cpu_bar = CustomProgressBar()
        self.ram_bar = CustomProgressBar()
        self.disk_bar = CustomProgressBar()
        summary_layout.addWidget(QLabel("CPU Usage:"))
        summary_layout.addWidget(self.cpu_bar)
        summary_layout.addWidget(QLabel("RAM Usage:"))
        summary_layout.addWidget(self.ram_bar)
        summary_layout.addWidget(QLabel("Disk Usage:"))
        summary_layout.addWidget(self.disk_bar)
        self.content_tabs.addTab(summary_tab, "Resumen")

        # Processes tab
        processes_tab = QWidget()
        processes_layout = QVBoxLayout(processes_tab)
        self.process_list_widget = QListWidget()
        processes_layout.addWidget(self.process_list_widget)
        self.content_tabs.addTab(processes_tab, "Procesos")

        # Performance tab
        performance_tab = QWidget()
        performance_layout = QVBoxLayout(performance_tab)
        self.cpu_chart = self.create_line_chart("CPU Usage Over Time")
        self.ram_chart = self.create_line_chart("RAM Usage Over Time")
        performance_layout.addWidget(self.cpu_chart)
        performance_layout.addWidget(self.ram_chart)
        self.content_tabs.addTab(performance_tab, "Rendimiento")

        # Applications tab
        applications_tab = QWidget()
        applications_layout = QVBoxLayout(applications_tab)
        self.app_list_widget = QListWidget()
        applications_layout.addWidget(self.app_list_widget)
        self.content_tabs.addTab(applications_tab, "Aplicaciones")

        layout.addWidget(self.content_tabs)

    def create_line_chart(self, title):
        chart = QChart()
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        series = QLineSeries()
        chart.addSeries(series)

        axis_x = QValueAxis()
        axis_x.setRange(0, 60)
        axis_x.setLabelFormat("%d")
        axis_x.setTitleText("Time (s)")
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setLabelFormat("%d")
        axis_y.setTitleText("Usage (%)")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        return chart_view

    def change_view(self):
        sender = self.sender()
        self.content_tabs.setCurrentIndex(self.content_tabs.indexOf(self.content_tabs.findChild(QWidget, sender.text())))

    def update_process_list(self):
        self.process_list_widget.clear()
        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                process_item = ProcessItem(process)
                list_item = QListWidgetItem(self.process_list_widget)
                list_item.setSizeHint(process_item.sizeHint())
                self.process_list_widget.addItem(list_item)
                self.process_list_widget.setItemWidget(list_item, process_item)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def update_system_info(self, data):
        self.cpu_bar.setValue(int(data['cpu']))
        self.ram_bar.setValue(int(data['memory']))
        self.disk_bar.setValue(int(data['disk']))

        # Update CPU chart
        cpu_series = self.cpu_chart.chart().series()[0]
        if cpu_series.count() > 60:
            cpu_series.remove(0)
        cpu_series.append(cpu_series.count(), data['cpu'])

        # Update RAM chart
        ram_series = self.ram_chart.chart().series()[0]
        if ram_series.count() > 60:
            ram_series.remove(0)
        ram_series.append(ram_series.count(), data['memory'])

    def closeEvent(self, event):
        self.system_monitor.stop()
        self.system_monitor.wait()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    task_manager = AdvancedTaskManager()
    task_manager.show()
    sys.exit(app.exec_())