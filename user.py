import json
import socket
import time

from message import Message
import hashlib


class User:
    def __init__(self):
        self.login = None
        self.__password_hash = None
        self.connection = None
        self.id = 'I'
        self.SERVER_HOST, self.SERVER_PORT = "127.0.0.1", 8000
        self.__go = True

    def login_(self, login, password_hash):
        self.login = login
        self.__password_hash = password_hash
        self.connection.sendall(b'l')
        time.sleep(1)
        self.connection.sendall(f'{login}|{password_hash}'.encode())
        data = self.connection.recv(1024)
        if data == b'1':
            return 1
        elif data == b'2':
            return 2
        elif data == b'3':
            return 3

    def connect(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.SERVER_HOST, self.SERVER_PORT))
        self.connection.sendall(b'1')
        self.SERVER_PORT = int(self.connection.recv(1024).decode()) # Возможно добавления функции кодирования и декодирования сообщения, сообщение новый свободный порт на сервере
        # print(self.SERVER_PORT)
        if self.SERVER_PORT is None:
            raise Exception('Все порты сервера заняты и он не может присвоить вам порт')
        else:
            self.connection.close()
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print((self.SERVER_HOST, self.SERVER_PORT))
            self.connection.connect((self.SERVER_HOST, self.SERVER_PORT))
            return None

    def send_message(self):
        message = Message("Hello", self.id, "Friend") # В будущем планируется каждому пользователю присваивать уникальный id и вводить его в поля sender и recipient
        self.connection.sendall(message.text)

    def registration(self, login, password_hash, user_name):
        print(f'|{login}|{password_hash}|{user_name}')
        self.connection.sendall(b'r')
        time.sleep(1)
        self.connection.sendall(f'{login}|{password_hash}|{user_name}'.encode())

    def disconnect(self):
        print('Ну я пытался')
        self.connection.sendall(b'e')
        self.connection.close()

    def get_chats(self):
        self.connection.sendall(b'c')
        data_json = self.connection.recv(1024).decode()
        data = json.loads(data_json)
        return data


if __name__ == "__main__":
    user = User()
    user.connect()
    # user.registration('mymail@mail.ru', hashlib.sha256(b'password').hexdigest(), 'myname')
    # user.login_('mymail@mail.ru', hashlib.sha256(b'password').hexdigest())
    user.get_chats()
    user.disconnect()