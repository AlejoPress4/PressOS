import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
import math

class ScientificCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculadora Científica Avanzada')
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #34495e;
                border: none;
                color: #ecf0f1;
                padding: 15px;
                font-size: 18px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                background-color: #34495e;
                border: 2px solid #2980b9;
                color: #ecf0f1;
                padding: 10px;
                font-size: 24px;
                border-radius: 5px;
            }
        """)

        layout = QVBoxLayout()
        
        # Display
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont('Arial', 20))
        layout.addWidget(self.display)

        # Buttons
        buttons = [
            ('C', '(', ')', 'backspace', '÷'),
            ('7', '8', '9', 'x²', '×'),
            ('4', '5', '6', '√', '-'),
            ('1', '2', '3', '^', '+'),
            ('±', '0', '.', 'π', '='),
            ('sin', 'cos', 'tan', 'log', 'ln'),
            ('asin', 'acos', 'atan', '10^x', 'e^x')
        ]

        button_grid = QGridLayout()
        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                button = QPushButton(button_text)
                button.clicked.connect(self.on_button_click)
                if button_text in ['=', 'C']:
                    button.setStyleSheet("""
                        background-color: #e74c3c;
                        font-weight: bold;
                    """)
                elif button_text.isdigit():
                    button.setStyleSheet("""
                        background-color: #3498db;
                    """)
                button_grid.addWidget(button, i, j)

        layout.addLayout(button_grid)
        self.setLayout(layout)

    def on_button_click(self):
        button = self.sender()
        key = button.text()

        if key == '=':
            try:
                result = eval(self.display.text().replace('×', '*').replace('÷', '/'))
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif key == 'C':
            self.display.clear()
        elif key == 'backspace':
            current = self.display.text()
            self.display.setText(current[:-1])
        elif key in ['sin', 'cos', 'tan', 'log', 'ln', 'asin', 'acos', 'atan']:
            try:
                current = float(self.display.text())
                if key == 'sin':
                    result = math.sin(math.radians(current))
                elif key == 'cos':
                    result = math.cos(math.radians(current))
                elif key == 'tan':
                    result = math.tan(math.radians(current))
                elif key == 'log':
                    result = math.log10(current)
                elif key == 'ln':
                    result = math.log(current)
                elif key == 'asin':
                    result = math.degrees(math.asin(current))
                elif key == 'acos':
                    result = math.degrees(math.acos(current))
                elif key == 'atan':
                    result = math.degrees(math.atan(current))
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif key == '√':
            try:
                result = math.sqrt(float(self.display.text()))
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif key == 'x²':
            try:
                result = float(self.display.text()) ** 2
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif key == '±':
            try:
                current = float(self.display.text())
                self.display.setText(str(-current))
            except:
                self.display.setText('Error')
        elif key == 'π':
            self.display.setText(self.display.text() + str(math.pi))
        elif key == '10^x':
            try:
                result = 10 ** float(self.display.text())
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif key == 'e^x':
            try:
                result = math.exp(float(self.display.text()))
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        else:
            self.display.setText(self.display.text() + key)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = ScientificCalculator()
    calc.show()
    sys.exit(app.exec_())