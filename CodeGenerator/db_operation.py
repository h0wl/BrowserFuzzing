# coding:utf-8
import sqlite3 as db

connection_url = "../../BrowserFuzzingData/db/js_corpus.db"
db_creation_ddl = 'CREATE TABLE "corpus" ("Id" INTEGER,"Content" BLOB NOT NULL);'


def init_db(sqlite_file_name):
    conn = db.connect(sqlite_file_name)
    cursor = conn.cursor()
    cursor.execute(db_creation_ddl)
    conn.commit()
    conn.close()


def insert(index, byte_array_of_content):
    conn = db.connect(connection_url)
    cursor = conn.cursor()
    sql = "INSERT INTO corpus VALUES(?, ?)"
    cursor.execute(sql, (index, byte_array_of_content))
    conn.commit()
    conn.close()


def query_all():
    conn = db.connect(connection_url)
    cursor = conn.cursor()
    sql = "SELECT * FROM corpus"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result
