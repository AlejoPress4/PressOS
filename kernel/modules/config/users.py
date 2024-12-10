import json
import os

class Usuario:  # Diccionario de clase para almacenar los usuarios

    def __init__(self, username, password, permisos, photo=None, user_path=None):
        self.username = username
        self.password = password
        self.permisos = permisos
        self.photo = photo
        self.user_path = self.create_user_path()
        

    def create_user_path(self):
        base_path = 'users_files'
        user_path = os.path.join(base_path, self.username)
        os.makedirs(user_path, exist_ok=True)

        # Crear carpetas por defecto
        default_folders = ['Documentos', 'Descargas', 'Musica', 'Imagenes', 'Videos']
        for folder in default_folders:
            os.makedirs(os.path.join(user_path, folder), exist_ok=True)

        return user_path
    
    def check_permissions(self, permiso):
        return permiso in self.permisos

    # Setters
    def set_username(self, username):
        self.username = username
    
    def set_password(self, password):
        self.password = password
    
    def set_permisos(self, permisos):
        self.permisos = permisos
    
    def set_photo(self, photo):
        self.photo = photo
    
    # Getters
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def get_permisos(self):
        return self.permisos

    def get_photo(self):
        return self.photo

    def get_user_path(self):
        return self.user_path

    # Metodos

    def __str__(self):
        return f"Usuario(username={self.username}, permisos={self.permisos}, foto={self.photo}, path={self.user_path})"


# # Ejemplo de uso
# usuarios = Usuario.from_json('kernel/users.json')
# print(usuarios['Press'].get_user_path())

# # Crear un nuevo usuario
# nuevo_usuario = Usuario('francisco', '1234', ['admin', 'user'], 'photo.jpg')