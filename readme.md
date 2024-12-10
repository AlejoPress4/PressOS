# PressOS

PressOS es un sistema operativo simulado desarrollado con Python y PyQt5. Este proyecto incluye una interfaz gráfica de usuario (GUI) para la gestión de usuarios y la simulación de un escritorio.

## Requisitos

- Python 3.6 o superior
- PyQt5
- OpenCV

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu_usuario/PressOS.git
    cd PressOS
    ```

2. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta la aplicación:
    ```sh
    python kernel/modules/config/functions.py
    ```

2. Inicia sesión con un usuario existente o crea uno nuevo.

## Estructura del Proyecto

- `kernel/`: Contiene los módulos principales del sistema operativo simulado.
  - `screens/`: Contiene las interfaces gráficas de usuario (GUI).
  - `modules/`: Contiene los módulos de configuración y funcionalidad.
    - `config/`: Contiene los archivos de configuración y funciones.
    - `users.py`: Módulo para la gestión de usuarios.

## Funcionalidades

- **Gestión de Usuarios**: Crear, eliminar y autenticar usuarios.
- **Simulación de Escritorio**: Interfaz gráfica para simular un escritorio con carpetas predeterminadas.

## Ejemplo de Uso

```python
from kernel.modules.config.functions import press_os

# Crear una instancia de press_os
sistema = press_os()

# Iniciar sesión
if sistema.login('usuario', 'contraseña'):
    print(f"Bienvenido, {sistema.get_current_user().get_username()}!")
else:
    print("Credenciales incorrectas.")