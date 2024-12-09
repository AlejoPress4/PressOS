class Usuario:
    def __init__(self, username, password, permisos, photo=None):
        self.username = username
        self.password = password
        self.permisos = permisos
        self.photo = photo

    def __str__(self):
        return f"Usuario(username={self.username}, permisos={self.permisos}, foto={self.photo})"

# Lista de usuarios
usuarios = [
    Usuario("Press", "0424", ["admin", "read", "write"], "./graphic_resources/photoProfile/photo_profile.jpg"),
    Usuario("TonTon", "dimelopau", ["read"], "./graphic_resources/photoProfile/tonton.jpg"),
    Usuario("Mari", "alejo4", ["read", "write"], "./graphic_resources/photoProfile/mari.jpg"),
]


