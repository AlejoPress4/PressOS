import os, sys
from kernel.secrets import *

class press_os ():

    


    def read_users (self, path):
        with open (path, 'r') as file:
            users = file.readlines()
        print (users)

    def login (self, password):
        print(password, def_usr['password'])
        if password == def_usr['password']:
            print("Login?")
            return True
        else:
            return False
        