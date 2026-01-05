import socket
from client import Client
import threading
import json


def next_free_port(port=1024, max_port=65535 ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        try:
            sock.bind(('127.0.0.1', port))
            sock.close()
            return port
        except OSError:
            port += 1
    return 2

class Server:
    def __init__(self):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connection.bind(('127.0.0.1', 8000))
        self.__clients = []
        self.__go = True

    def __assign_port__(self):
        self.__connection.listen()
        self.__conn, self.__addr = self.__connection.accept()
        with self.__conn:
            __data = json.loads(self.__conn.recv(1024))
            if __data['flag'] == '1':
                print(f'Connection by {self.__addr}')
                print(f'Message received: {__data}')
                __new_port = next_free_port()
                print(__new_port)
                self.__conn.sendall(str(__new_port).encode())
                __client = Client(*self.__addr, __new_port)
                thread = threading.Thread(target=__client.run)
                thread.start()

    def run(self):
        while self.__go:
            self.__assign_port__()


if __name__ == "__main__":
    server = Server()
    server.run()
    # server.__assign_port__()