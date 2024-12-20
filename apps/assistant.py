import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os
from groq import Groq

class AsistenteGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asistente IA")
        self.setMinimumSize(400, 500)
        # Configurar el cliente Groq
        api_key = "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"  # Reemplaza esto con tu clave API real
        self.client = Groq(api_key=api_key)
        
        # Configurar el widget central y el layout principal
        central_widget = QWidget(self)
        central_widget.setObjectName("centralwidget")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Área de chat
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        main_layout.addWidget(self.chat_area)
        
        # Layout para entrada de texto y botón
        input_layout = QHBoxLayout()
        
        # Campo de entrada
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Escribe tu mensaje aquí...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        # Botón de enviar
        self.send_button = QPushButton("Enviar")
        self.send_button.setObjectName("send_button")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        main_layout.addLayout(input_layout)
        
        # Estilos generales
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTextEdit, QLineEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.set_fonts()
        self.raise_()
        self.activateWindow()

    def set_fonts(self):
        font = QFont("Arial", 10)
        self.chat_area.setFont(font)
        self.input_field.setFont(font)

    def send_message(self):
        user_message = self.input_field.text()
        if user_message:
            self.chat_area.append(f"Tú: {user_message}")
            self.input_field.clear()
            
            # Obtener respuesta del asistente
            response = self.get_assistant_response(user_message)
            self.chat_area.append(f"Asistente: {response}")
            
            # Desplazar al final del chat
            self.chat_area.verticalScrollBar().setValue(
                self.chat_area.verticalScrollBar().maximum()
            )

    def get_assistant_response(self, user_message):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error al obtener respuesta: {str(e)}"

    def resizeEvent(self, event):
        # Ajustar tamaños para diseño responsive
        super().resizeEvent(event)
        window_width = self.width()
        if window_width < 600:
            self.chat_area.setMinimumHeight(int(self.height() * 0.6))
        else:
            self.chat_area.setMinimumHeight(int(self.height() * 0.7))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AsistenteGUI()
    window.show()
    sys.exit(app.exec_())

