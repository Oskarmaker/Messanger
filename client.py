#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
        self.__row = None

    def run(self):
        self.__connection.listen()
        self.__conn, self.__addr = self.__connection.accept()
        try:
            with self.__conn:
                while True:
                    __data = self.__conn.recv(1024)
                    if __data != b'':
                        print(__data)
                        if __data == b'r':
                            self.__conn.sendall(self.registration())
                        elif __data == b'l':
                            self.__conn.sendall(self.login())
                        elif __data == b'e':
                            self.__connection.close()
                        elif __data == b'c':
                            self.__conn.sendall(json.dumps(self.get_chats().tolist()).encode())
                        elif __data == b'm':
                            self.send_message()
                        elif __data == b'ch':
                            self.create_chat()
                        elif __data == b'cf':
                            self.create_new_friend()
                        elif __data == b'atc':
                            self.add_to_chat()
        except Exception as e:
            self.__connection.close()
            print(e)

    def send_message(self):
        __message = json.loads(self.__conn.recv(1024).decode())
        self.__db.set_row("", )

    def create_chat(self):
        __chat_name = self.__conn.recv(1024).decode()
        self.__db.set_row("chat", {'name': [__chat_name]})
        self.__conn.sendall(b'cc')

    def add_to_chat(self):
        __chat_name = self.__conn.recv(1024).decode()
        __users = json.loads(self.__conn.recv(1024).decode())
        for __user in __users:
            __row_client = self.__db.get_row("client", "username", __user)
            __row_chat = self.__db.get_row("chat", "name", __chat_name)
            if __row_client.empty:
                __row_chat = __row_chat.values[0]
                __row_client = __row_client.values[0]
                self.__db.set_row("chat_client",
                                  {'chat_id': [__row_chat[0]], 'client_id': [__row_client[0]]}, False)

    def create_new_friend(self):
        __username = self.__conn.recv(1024).decode()
        print(__username)
        print(self.__db.get_row("client", "user_name", __username).values)
        __row_client = self.__db.get_row("client", "user_name", __username)
        if not __row_client.empty:
            __row_client = __row_client.values[0]
            print(__row_client)
            self.__db.set_row("chat", {'name': [__username]})
            __chat_id = self.__db.get_row("chat", "name", __username).values[0][0]
            print("Проверка Ошибки: ", __row_client)
            self.__db.set_row("chat_client",
                              {'chat_id': [__chat_id], 'client_id': [__row_client[0]]}, False)
            print("Проверка Ошибки: ", self.__row)
            self.__db.set_row("chat_client",
                              {'chat_id': [__chat_id], 'client_id': [self.__row[0]]}, False)



    def get_chats(self):
        return self.__db.get_row('chat', 'name').values


    def login(self):
        __login, __password_hash = self.__conn.recv(1024).decode().split('|')
        __row = self.__db.get_row('client', 'login', __login)
        if __row.empty:
            return json.dumps('Пользователя с данным логином не найдено').encode()
        elif __row.values[0][2] != __password_hash:
            return json.dumps(['Неверный пароль']).encode()
        else:
            data = ['1', __row.values[0].tolist()]
            self.__row = __row.values[0]
            return json.dumps(data).encode()

    def registration(self):
        __login, __password_hash, __user_name = self.__conn.recv(1024).decode().split('|')
        if not self.__db.get_row('client', 'login', __login).empty:
            return 'Данный логин уже существует'.encode()
        elif not self.__db.get_row('client', 'user_name', __user_name).empty:
            return 'Данное имя пользователя уже занято другим пользователем'.encode()
        else:
            self.__db.set_row('client', {'login': [__login], 'password_hash': [__password_hash], 'user_name': [__user_name]})
            self.__row = self.__db.get_row("client", "login", __login).values[0]
            return json.dumps(['1', self.__row.tolist()]).encode()



