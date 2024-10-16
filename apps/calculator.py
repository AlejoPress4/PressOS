import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
import math

class ScientificCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculadora Científica')
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                color: #333;
            }
            QPushButton {
                background-color: #fff;
                border: 1px solid #ddd;
                padding: 15px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
            QLineEdit {
                background-color: #fff;
                border: 1px solid #ddd;
                padding: 10px;
                font-size: 24px;
            }
        """)

        layout = QVBoxLayout()
        
        # Display
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        layout.addWidget(self.display)

        # Buttons
        buttons = [
            ('7', '8', '9', '/', 'C'),
            ('4', '5', '6', '*', '('),
            ('1', '2', '3', '-', ')'),
            ('0', '.', '=', '+', 'backspace'),
            ('sin', 'cos', 'tan', 'sqrt', '^'),
            ('log', 'ln', 'e', 'π', '%')
        ]

        button_grid = QGridLayout()
        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                button = QPushButton(button_text)
                button.clicked.connect(self.on_button_click)
                button_grid.addWidget(button, i, j)

        layout.addLayout(button_grid)
        self.setLayout(layout)

    def on_button_click(self):
        button = self.sender()
        key = button.text()

        if key == '=':
            try:
                result = eval(self.display.text())
                self.display.setText(str(result))
            except:
                self.display.setText('Error')
        elif key == 'C':
            self.display.clear()
        elif key == 'backspace':
            current = self.display.text()
            self.display.setText(current[:-1])
        elif key in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt']:
            current = self.display.text()
            if key == 'sin':
                result = math.sin(math.radians(float(current)))
            elif key == 'cos':
                result = math.cos(math.radians(float(current)))
            elif key == 'tan':
                result = math.tan(math.radians(float(current)))
            elif key == 'log':
                result = math.log10(float(current))
            elif key == 'ln':
                result = math.log(float(current))
            elif key == 'sqrt':
                result = math.sqrt(float(current))
            self.display.setText(str(result))
        elif key == '^':
            self.display.setText(self.display.text() + '**')
        elif key == 'π':
            self.display.setText(self.display.text() + str(math.pi))
        elif key == 'e':
            self.display.setText(self.display.text() + str(math.e))
        else:
            self.display.setText(self.display.text() + key)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = ScientificCalculator()
    calc.show()
    sys.exit(app.exec_())