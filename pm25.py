import pymysql
import pandas as pd


def open_db():
    conn = None
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="kim60309",
            db="demo",
        )
    except Exception as e:
        print("Error connecting to database:", e)
    return conn


def update_db():
    api_url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=540e2ca4-41e1-4186-8497-fdd67024ac44&limit=1000&sort=datacreationdate%20desc&format=CSV"
    sqlstr = """
        insert ignore into pm25(site,county,pm25,datacreationdate,itemunit) 
        value(%s, %s, %s, %s, %s)
        """
    row_counts = 0
    message = ""
    try:
        # 取得最新資料
        df = pd.read_csv(api_url)
        df["datacreationdate"] = pd.to_datetime(df["datacreationdate"])
        df1 = df.dropna()
        values = df1.values.tolist()
        # 寫入資料庫
        conn = open_db()
        cur = conn.cursor()
        cur.executemany(sqlstr, values)
        row_counts = cur.rowcount
        conn.commit()

        print(f"更新{row_counts}筆資料")
        message = "更新成功"

    except Exception as e:
        print("Error connecting to database:", e)
        message = f"更新失敗:{e}"

    finally:
        if conn is not None:
            conn.close()

    return row_counts, message


def get_all_counties():
    conn = None
    counties = []
    try:
        conn = open_db()
        cur = conn.cursor()
        sqlstr = "SELECT distinct county FROM pm25;"
        cur.execute(sqlstr)
        datas = cur.fetchall()
        counties = [data[0] for data in datas]

    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
    return counties


def get_all_sites(county):
    conn = None
    sites = []
    try:
        conn = open_db()
        cur = conn.cursor()
        sqlstr = "SELECT distinct site FROM pm25 where county=%s;"
        cur.execute(sqlstr, (county,))
        datas = cur.fetchall()
        sites = [data[0] for data in datas]

    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
    return sites


def get_pm25_by_site(county, site):
    conn = None
    datas = None
    colnames = None
    try:
        conn = open_db()
        cur = conn.cursor()
        sqlstr = "SELECT * FROM pm25 where county = %s and site = %s;"
        cur.execute(sqlstr, (county, site))
        # print(cur.description)
        columns = [i[0] for i in cur.description]
        datas = cur.fetchall()
    except Exception as e:
        print("Error executing SQL query:", e)
    finally:
        if conn is not None:
            conn.close()
    return datas, columns


def get_pm25_data():
    conn = None
    datas = None
    colnames = None
    try:
        conn = open_db()
        cur = conn.cursor()
        sqlstr = "SELECT * FROM pm25 where datacreationdate = (select MAX(datacreationdate) from pm25);"
        cur.execute(sqlstr)
        # print(cur.description)
        columns = [i[0] for i in cur.description]
        datas = cur.fetchall()
    except Exception as e:
        print("Error executing SQL query:", e)
    finally:
        if conn is not None:
            conn.close()
    return datas, columns


if __name__ == "__main__":
    # get_pm25_by_site("臺北市", "大同")
    # print(get_all_counties())
    get_all_sites("臺北市")
