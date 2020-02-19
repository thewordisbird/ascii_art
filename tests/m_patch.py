from subprocess import Popen
import os

def get_terminal_size():
    terminal_size = Popen('stty size', shell=True)
    return terminal_size

def get_path():
    path = os.path.abspath(__file__)
    return path
