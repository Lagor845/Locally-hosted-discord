import socket
from threading import Thread

class client():
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Ip_address = ""
        self.Port = 34051