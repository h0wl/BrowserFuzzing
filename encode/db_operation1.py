# coding:utf-8
import os
import sqlite3 as db


class DBOperation:
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name
        self.ddl = 'CREATE TABLE ' + self.table_name + '("Id" INTEGER PRIMARY KEY AUTOINCREMENT,"Content" BLOB NOT ' \
                                                       'NULL); '
        self.connection = None

    def init_db(self):
        if os.path.exists(self.db_path) and not self.is_empty():
            os.remove(self.db_path)
        if not os.path.exists(self.db_path):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(self.ddl)

    def is_empty(self):
        connection = db.connect(self.db_path)
        cursor = connection.cursor()
        sql = "SELECT count(*) FROM " + self.table_name
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0] == 0

    def get_connection(self):
        if self.connection is None:
            self.connection = db.connect(self.db_path)
        return self.connection

    def finalize(self):
        self.connection.commit()
        self.connection.close()

    def insert(self, column_names: list, values: list):
        connection = self.get_connection()
        cursor = connection.cursor()
        sql = "INSERT INTO " + self.table_name + "("
        param_list = ""
        if column_names.__len__() > 0:
            sql += column_names[0]
            param_list += "?"
        for i in range(1, column_names.__len__()):
            sql += ","
            sql += column_names[i]
            param_list += ",?"
        sql = sql + ") VALUES(" + param_list + ")"
        cursor.execute(sql, values)

    def query_all(self, columns: list):
        conn = self.get_connection()
        cursor = conn.cursor()

        sql = "SELECT "
        if columns.__len__() > 0:
            sql += columns[0]
        for i in range(1, columns.__len__()):
            sql += ", "
            sql += columns[i]
        sql += " FROM " + self.table_name

        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def query_count(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        sql = "SELECT count(*) FROM " + self.table_name
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

    # def write(self,functions):
    #     db_path = "./output/final.db"
    #     db_op = DBOperation(db_path, 'corpus')
    #     db_op.init_db()
    #     # callables = db_op.query_all(["Content"])
    #     # print(callables[0][0].decode('utf-8'))
    #     for function in functions:
    #         db_op.insert(["Content"], [str(function)])
    #
    #     db_op.finalize()

# if __name__ == "__main__":
#     db_path = "../../BrowserFuzzingData/db/a.db"
#     db_op = DBOperation(db_path, 'corpus')
#     db_op.init_db()
#     callables = db_op.query_all(["Content"])
#     print(callables[0][0].decode('utf-8'))
#     db_op.insert(["Content"], ["function"])
#     db_op.finalize()
