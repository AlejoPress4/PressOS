import subprocess
import os, sys, cv2
from kernel.secrets import *
from PyQt5 import QtCore

class press_os ():
    def read_users (self, path):
        with open (path, 'r') as file:
            users = file.readlines()
        print (users)

    def login (self, password):
        if password == def_usr['password']:
            return True
        else:
            return False
    