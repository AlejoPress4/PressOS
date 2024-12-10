import re
import subprocess
import os, sys, cv2
import json
from PyQt5 import QtCore
from kernel.modules.config.users import Usuario

class press_os:
    usuarios = {}
    current_user = None
    current_user_directory = None

    def __init__(self):
        self.usuarios = self.load_json('kernel/users.json')
        self.current_user = self.usuarios.get('Press')

    def add_user(self, username, password, permisos, photo=None):
        if username in self.usuarios:
            return False
        self.usuarios[username] = Usuario(username, password, permisos, photo)
        self.save_json('kernel/users.json')
        return True
    
    def remove_user(self, username):
        if username not in self.usuarios:
            return False
        self.usuarios.pop(username)
        self.save_json('kernel/users.json')
        return True

    def login(self, username, password):
        usuario = self.usuarios.get(username)
        if usuario:
            if usuario.password == password:
                self.set_current_user(username)
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
    
    # Setters
    def set_current_user(self, username):
        self.current_user = self.usuarios.get(username)
        self.current_user_directory = self.current_user.user_path
        return True
        

# # Ejemplo de uso
# config = press_os()
# print(config.login('TonTon','Molton321#'))
# print(config.current_user.check_permissions('wirte'))
# print(config.get_current_user())
# print(config.get_user_directory())
#config.add_user('hamburguesa', '1234', ['mostaza', 'ketchup', 'mayonesa', 'salsa de piña', 'BBQ'])
#config.set_current_user('TonTon')

# print(config.get_current_user())