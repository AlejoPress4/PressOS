import subprocess
import os, sys, cv2
import json
from PyQt5 import QtCore
from users import Usuario

class press_os:
    usuarios = {}
    current_user = None
    current_user_directory = None

    def __init__(self):
        self.usuarios = self.load_json('kernel/users.json')
        self.current_user = self.usuarios.get('Press')

    def login(self, username, password):
        usuario = self.usuarios.get(username)
        if usuario:
            if usuario.password == password:
                self.current_user = usuario
                self.current_user_directory = usuario.user_path
                return True
            else:
                return False
        else:
            return False

    def load_json(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.usuarios = {user['username']: Usuario(**user) for user in data}
        return self.usuarios

    def save_json(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump([user.__dict__ for user in self.usuarios.values()], file, ensure_ascii=False, indent=4)

    # Getters
    def get_current_user(self):
        return self.current_user

    def get_user_directory(self):
        return self.current_user_directory

    def get_users(self):
        return self.usuarios


# Ejemplo de uso
config = press_os()
print(config.get_current_user())

