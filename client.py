import socket
from database import Database
import numpy as np
import json

class Client:
    def __init__(self, client_host, client_port, server_port):
        self.__client_host = client_host
        self.__client_port = client_port
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connection.bind(("127.0.0.1", server_port))
        self.__db = Database()

    def run(self):
        self.__connection.listen()
        self.__conn, self.__addr = self.__connection.accept()
        with self.__conn:
            while True:
                __data = self.__conn.recv(1024)
                if __data != b'':
                    print(__data)
                    if __data == b'r':
                        self.registration()
                    elif __data == b'l':
                        self.__conn.sendall(self.login())
                    elif __data == b'e':
                        print('Попытка закрытия сокета')
                        self.__connection.close()
                    elif __data == b'c':
                        print(type(self.get_chats().tolist()))
                        self.__conn.sendall(json.dumps(self.get_chats().tolist()).encode())


    def get_chats(self):
        return self.__db.get_row('chat', 'name').values


    def login(self):
        __login, __password_hash = self.__conn.recv(1024).decode().split('|')
        __row = self.__db.get_row('client', 'login', __login)
        if __row.empty:
            print('Пользователя с данным логином не найдено')
            return b'2'
        elif __row.values[0][2] != __password_hash:
            print('Неверный пароль')
            return b'3'
        else:
            print('Ура, вы смогли войти')
        return b'1'

    def registration(self):
        __login, __password_hash, __user_name = self.__conn.recv(1024).decode().split('|')
        if not self.__db.get_row('client', 'login', __login).empty:
            print('Данный логин уже существует')
        elif not self.__db.get_row('client', 'user_name', __user_name).empty:
            print('Данное имя пользователя уже занято другим пользователем')
        else:
            self.__db.set_row('client', {'login': [__login], 'password_hash': [__password_hash], 'user_name': [__user_name]})



