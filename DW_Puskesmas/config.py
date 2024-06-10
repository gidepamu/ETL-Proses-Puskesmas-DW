import pymysql
import psycopg2

def db_puskesmas():
    conn_db_puskesmas = pymysql.connect(
        host="localhost",
        user="********",
        password="********",
        database="main_source"
    )
    return conn_db_puskesmas

def dw_mysql_puskesmas():
    conn_dw_puskesmas_mysql = pymysql.connect(
        host="localhost",
        user="********",
        password="********",
        database="dw_skripsi_puskesmas_MYSQL"
    )
    conn_dw_puskesmas_mysql.cursor().execute('SET SQL_MODE=ANSI_QUOTES')
    return conn_dw_puskesmas_mysql

def dw_PG_puskesmas():
    conn_dw_PG = psycopg2.connect(
        host = "localhost",
        port = 0000,
        database = "PG_SKRIPSI",
        user = "********",
        password ="********"          
    )        
    return conn_dw_PG