import psycopg2
from psycopg2 import Error
import config
from datetime import datetime


def create_bd():
    try:
        connection = psycopg2.connect(user=config.USER,
                                      password=config.PASSWORD,
                                      host=config.HOST,
                                      port=config.PORT,
                                      database=config.DATABASE)

        cursor = connection.cursor()

        cursor.execute("CREATE TABLE user_data ("
                       "ID TEXT PRIMARY KEY NOT NULL,"
                       "EMAIL TEXT NOT NULL,"
                       "PASSWORD TEXT NOT NULL,"
                       "TIME TEXT)")
        connection.commit()
    except(Exception, Error) as errorDB:
        print(errorDB)
    finally:
        if connection:
            cursor.close()
            connection.close()


def drop_bd():
    try:
        connection = psycopg2.connect(user=config.USER,
                                      password=config.PASSWORD,
                                      host=config.HOST,
                                      port=config.PORT,
                                      database=config.DATABASE)

        cursor = connection.cursor()

        cursor.execute("DROP TABLE user_data")
        connection.commit()

    except(Exception, Error) as errorDB:
        print(errorDB)
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_all_info():
    try:
        connection = psycopg2.connect(user=config.USER,
                                      password=config.PASSWORD,
                                      host=config.HOST,
                                      port=config.PORT,
                                      database=config.DATABASE)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        buf_requests = cursor.fetchall()
        connection.commit()
    except(Exception, Error) as errorDB:
        print(errorDB)
    finally:
        if connection:
            cursor.close()
            connection.close()
            if len(buf_requests) == 0:
                return None
            else:
                return buf_requests


def get_info_debug():
    connection = psycopg2.connect(user=config.USER,
                                  password=config.PASSWORD,
                                  host=config.HOST,
                                  port=config.PORT,
                                  database=config.DATABASE)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    print(cursor.fetchall())
    connection.commit()


def add_user(uid, email, password):
    flag = False
    try:
        connection = psycopg2.connect(user=config.USER,
                                      password=config.PASSWORD,
                                      host=config.HOST,
                                      port=config.PORT,
                                      database=config.DATABASE)

        cursor = connection.cursor()
        buffer_requests = "INSERT INTO user_data (ID, EMAIL, PASSWORD) VALUES ('{}', '{}', '{}')".format(uid,
                                                                                                         email,
                                                                                                         password)
        cursor.execute(buffer_requests)
        connection.commit()
        flag = True
    except(Exception, Error) as errorDB:
        print(errorDB)
    finally:
        if connection:
            cursor.close()
            connection.close()
            return flag


def add_data(uid, time):
    flag = False
    try:
        connection = psycopg2.connect(user=config.USER,
                                      password=config.PASSWORD,
                                      host=config.HOST,
                                      port=config.PORT,
                                      database=config.DATABASE)

        cursor = connection.cursor()
        buffer_requests = "UPDATE user_data set time = '{}' where id = '{}'".format(time, uid)
        cursor.execute(buffer_requests)
        connection.commit()
        flag = True
    except(Exception, Error) as errorDB:
        print(errorDB)
    finally:
        if connection:
            cursor.close()
            connection.close()
        return flag


def get_info(uid):
    try:
        connection = psycopg2.connect(user=config.USER,
                                      password=config.PASSWORD,
                                      host=config.HOST,
                                      port=config.PORT,
                                      database=config.DATABASE)

        cursor = connection.cursor()
        buf_requests = "SELECT * FROM user_data where id = '{}'".format(uid)
        cursor.execute(buf_requests)
        buf_requests = cursor.fetchall()
        connection.commit()
    except(Exception, Error) as errorDB:
        print(errorDB)
    finally:
        if connection:
            cursor.close()
            connection.close()
            if len(buf_requests) == 0:
                return None
            else:
                return buf_requests

drop_bd()