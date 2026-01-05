import json
import socket
import time

from messageDTO import MessageDTO
from message import Message
import hashlib


class User:
    def __init__(self):
        self.SERVER_HOST, self.SERVER_PORT = "127.0.0.1", 8000
        self.__go = True
        self.__user_inf = None


    def login_(self, login, password_hash):
        self.login = login
        self.__password_hash = password_hash
        self.connection.sendall(json.dumps(MessageDTO('l', f'{login}|{password_hash}').__dict__).encode())
        data = json.loads(self.connection.recv(1024))
        if data[0] == '1':
            print("Успешный вход")
            self.__user_inf = data[1]
            print(self.__user_inf)
        else:
            print(data[0])

    def connect(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.SERVER_HOST, self.SERVER_PORT))
        self.connection.sendall(json.dumps(MessageDTO('1', '').__dict__).encode())
        self.SERVER_PORT = int(self.connection.recv(1024).decode())  # Возможно добавления функции кодирования и декодирования сообщения, сообщение новый свободный порт на сервере
        if self.SERVER_PORT is None:
            raise Exception('Все порты сервера заняты и он не может присвоить вам порт')
        else:
            self.connection.close()
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print((self.SERVER_HOST, self.SERVER_PORT))
            self.connection.connect((self.SERVER_HOST, self.SERVER_PORT))
            return None

    def create_chat(self, chat_name):
        self.connection.sendall(json.dumps(MessageDTO('ch', f'{chat_name}').__dict__).encode())
        if self.connection.recv(1024) == b'cc':
            print('Чат успешно создан')
            return True
        return None

    def send_message(self, text, chat_id):
        message = Message(text, self.__user_inf[0], chat_id) # В будущем планируется каждому пользователю присваивать уникальный id и вводить его в поля sender и recipient
        self.connection.sendall(json.dumps(MessageDTO('m', message).__dict__).encode())
        time.sleep(1)

    def registration(self, login, password_hash, user_name):
        print(f'|{login}|{password_hash}|{user_name}')
        self.connection.sendall(json.dumps(MessageDTO('r', f'{login}|{password_hash}|{user_name}').__dict__).encode())
        data = json.loads(self.connection.recv(1024))
        if data[0] == '1':
            print("Успешная регистрация")
            self.__user_inf = data[1]
            print(self.__user_inf)
        else:
            print(data[0])

    def disconnect(self):
        print('Ну я пытался')
        self.connection.sendall(json.dumps(MessageDTO('e', '').__dict__).encode())
        self.connection.close()

    def create_new_friend(self, username):
        self.connection.sendall(json.dumps(MessageDTO('cf', username).__dict__).encode())

    def get_chats(self):
        self.connection.sendall(json.dumps(MessageDTO('c', '').__dict__).encode())
        data_json = self.connection.recv(1024).decode()
        data = json.loads(data_json)
        return data

    def add_to_chat(self, new_users, chat_name):
        self.connection.sendall(json.dumps(MessageDTO('atc', [new_users, chat_name]).__dict__).encode())
        time.sleep(1)
        self.connection.sendall(chat_name)
        self.connection.sendall(json.dumps(new_users))


if __name__ == "__main__":
    try:
        user = User()
        user.connect()
        # user.registration('mymail@mail.ru', hashlib.sha256(b'password').hexdigest(), 'myname')
        user.login_('mymail@mail.ru', hashlib.sha256(b'password').hexdigest())
        user.create_new_friend('alexey')
        user.get_chats()
        user.disconnect()
    except Exception as e:
        if 'user' in globals():
            user.disconnect()
        print(e)