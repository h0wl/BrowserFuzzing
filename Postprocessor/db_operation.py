# coding:utf-8
import os
import sqlite3 as db


class DBOperation:
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name
        self.ddl = 'CREATE TABLE ' + self.table_name + '("Id" INTEGER PRIMARY KEY AUTOINCREMENT,"Content" BLOB NOT ' \
                                                       'NULL); '

    def init_db(self):
        if os.path.exists(self.db_path) and not self.is_empty():
            os.remove(self.db_path)
        if not os.path.exists(self.db_path):
            conn = db.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(self.ddl)
            conn.commit()
            conn.close()

    def is_empty(self):
        connection = db.connect(self.db_path)
        cursor = connection.cursor()
        sql = "SELECT count(*) FROM " + self.table_name
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.close()
        return result[0][0] == 0

    def insert(self, byte_array_of_content):
        conn = db.connect(self.db_path)
        cursor = conn.cursor()
        sql = "INSERT INTO " + self.table_name + "(Content) VALUES(?)"
        cursor.execute(sql, [byte_array_of_content])
        conn.commit()
        conn.close()

    def query_all(self):
        conn = db.connect(self.db_path)
        cursor = conn.cursor()
        sql = "SELECT Content FROM " + self.table_name
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return result

    def query_count(self):
        conn = db.connect(self.db_path)
        cursor = conn.cursor()
        sql = "SELECT count(*) FROM " + self.table_name
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.close()
        return result
