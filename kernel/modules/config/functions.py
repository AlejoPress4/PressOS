import subprocess
import os, sys, cv2
from PyQt5 import QtCore
from kernel.modules.users import usuarios, Usuario

class press_os:
    def __init__(self):
        self.default_user = Usuario("Press", "0424", ["admin", "read", "write"])
        self.current_user = self.default_user
        self.usuarios = usuarios

    def read_users(self, path):
        with open(path, 'r') as file:
            users = file.readlines()
        print(users)

    def login(self, username, password):
        usuario = self.autenticar(username, password)
        if usuario:
            self.current_user = usuario
            return True
        else:
            return False

    def get_current_user(self):
        return self.current_user
    
    def get_current_user_directory(self):
        return self.current_user_directory

    def set_default_user(self):
        self.current_user = self.default_user

# Función para autenticar usuarios
    def autenticar(self, username, password):
        for usuario in self.usuarios:
            if usuario.username == username and usuario.password == password:
                return usuario
        return None

    # Función para agregar un nuevo usuario
    def agregar_usuario(self, username, password, permisos, photo=None):
        if not any(usuario.username == username for usuario in self.usuarios):
            self.usuarios.append(Usuario(username, password, permisos, photo))
            return True
        return False

    # Función para eliminar un usuario
    def eliminar_usuario(self, username):
        self.usuarios = [usuario for usuario in self.usuarios if usuario.username != username]

    # Función para verificar permisos
    def tiene_permiso(self, usuario, permiso):
        return permiso in usuario.permisos

    # Función para obtener todos los usuarios
    def obtener_usuarios(self):
        return self.usuarios
    
    # def crear_directorios_usuarios(self):
    #     for usuario in self.usuarios:
    #         os.mkdir(f"./users/{usuario.username}")
    
    def crear_directorios_usuarios():
        base_path = './user_files'
        if not os.path.exists(base_path):
            os.makedirs(base_path)