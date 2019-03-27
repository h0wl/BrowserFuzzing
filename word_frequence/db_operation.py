# coding:utf-8
import os
import sqlite3 as db


class DBOperation:                                      # 1
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name
        self.ddl = 'CREATE TABLE ' + self.table_name + '( "id" INTEGER NOT NULL, ".anchor" TEXT NOT NULL, ".big" TEXT NOT NULL, ".blink" TEXT NOT NULL, ".bold" TEXT NOT NULL, ".charAt" TEXT NOT NULL, ' \
                                                       '".charCodeAt" TEXT NOT NULL, ".fixed" TEXT NOT NULL, ".fontcolor" TEXT NOT NULL, ".fontsize" TEXT NOT NULL, ".indexOf" TEXT NOT NULL, ".italics" TEXT NOT NULL,' \
                                                       ' ".lastIndexOf" TEXT NOT NULL, ".link" TEXT NOT NULL, ".localeCompare" TEXT NOT NULL, ".match" TEXT NOT NULL, ".replace" TEXT NOT NULL, ".search" TEXT NOT NULL, ' \
                                                       '".small" TEXT NOT NULL, ".split" TEXT NOT NULL, ".strike" TEXT NOT NULL, ".sub" TEXT NOT NULL, ".substr" TEXT NOT NULL, ".substring" TEXT NOT NULL, ".sup" TEXT NOT NULL, ' \
                                                       '".toLocaleLowerCase" TEXT NOT NULL, ".toLocaleUpperCase" TEXT NOT NULL, ".toLowerCase" TEXT NOT NULL, ".toUpperCase" TEXT NOT NULL, PRIMARY KEY ("id")); '
        self.connection = None

    def init_db(self):
        if os.path.exists(self.db_path) and not self.is_empty():
            os.remove(self.db_path)
        if not os.path.exists(self.db_path):
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(self.ddl)

    def is_empty(self):
        connection = self.get_connection()
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

    def insert_frequencies(self, column_names: list, frequencies: list):
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
        cursor.execute(sql, frequencies)

    def query_all(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        sql = "SELECT Content FROM " + self.table_name
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def query_count(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        sql = "SELECT count(*) FROM " + self.table_name         #该表总行数
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

# if __name__ == "__main__":
#         db_path = "../../BrowserFuzzingData/db/js_corpus_final_top_1000.db"
#         db_op = DBOperation(db_path, "corpus")
#         db_op.insert_frequencies([".toSource", ".toString", ".valueOf"], [1, 1, 1])
