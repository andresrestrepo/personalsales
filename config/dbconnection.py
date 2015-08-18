import sqlite3


def get_db_connection():
    sql_connection = sqlite3.connect('../db/personal_sale.db')
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('PRAGMA foreign_keys = ON')
    sql_cursor.close()
    return sql_connection
