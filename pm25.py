import pymysql
import pandas as pd


def open_db():
    conn = None
    try:
        conn = pymysql.connect(
            host="127.0.0.1", port=3306, user="root", password="kim60309", db="demo"
        )
    except Exception as e:
        print("Error connecting to the database:", e)

    return conn


def get_pm25_data():
    conn = None
    datas, columns = None, None
    try:
        conn = open_db()
        cur = conn.cursor()

        sqlstr = "select * from pm25;"
        cur.execute(sqlstr)
        print(cur.description)
        columns = [col[0] for col in cur.description]
        datas = cur.fetchall()

    except Exception as e:
        print("Error executing SQL query:", e)
    finally:
        if conn is not None:
            conn.close()

    return datas, columns


if __name__ == "__main__":
    conn = open_db()
    print(conn)
    datas, columns = get_pm25_data()
    print(datas, columns)
