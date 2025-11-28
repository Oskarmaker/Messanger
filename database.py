import psycopg2
import sqlalchemy
import pandas as pd
from urllib.parse import quote_plus

from psycopg2.errorcodes import SQL_ROUTINE_EXCEPTION
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.exc import SQLAlchemyError


class Database:
    def __init__(self):
        __password = quote_plus("TestDatabaseToMessenger")
        self.__engine = sqlalchemy.create_engine(f'postgresql+psycopg2://postgres:{__password}@localhost:5432/postgres')
        self.__tables_names = ['client', 'chat', 'message', 'chat_client']
        self.__dfs = [pd.read_sql(f'SELECT * FROM public.{__table}', self.__engine) for __table in self.__tables_names]

    def get_row(self, table_name, column_name, column_value=None): # Получить данные о клиенте
        __index = self.__tables_names.index(table_name)
        __df = self.__dfs[__index]
        if column_value:
            __row = __df[__df[column_name] == column_value]
            return __row
        return __df[column_name]

    def set_row(self, table_name, data, call_function=True): # Функция добавляющая нового клиента
        __new_row = pd.DataFrame(data)
        print('DataFrame: ', __new_row)
        __index = self.__tables_names.index(table_name)
        __df = self.__dfs[__index]
        __df = pd.concat([__df, __new_row], ignore_index=True)
        try:
            __new_row.to_sql(table_name, self.__engine, if_exists='append', index=False)
            print('All good')
        except SQLAlchemyError as e:
            print(f'ОШИБКА при попытке записи в таблицу {table_name}:', e.args[0][43:])

        if call_function:
            with self.__engine.connect() as conn: # Вызов SQL-функции для правильного нумерования индексов
                conn.execute(sqlalchemy.text(f'SELECT renumber_{table_name}_ids();'))
                conn.commit()

if __name__ == "__main__":
    db = Database()
    print(db.get_row('client', 'login', 'Andrey@mail.ru').values[0])
    # db.set_row('client', 'Andrey@mail.ru', '0987654', 'andrey')

