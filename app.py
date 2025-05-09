from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
from pm25 import (
    get_pm25_data,
    update_db,
    get_pm25_by_site,
    get_all_counties,
    get_all_sites,
)
import json

app = Flask(__name__)


@app.route("/pm25-county-site")
def pm25_county_site():
    county = request.args.get("county")
    sites = get_all_sites(county)
    result = json.dumps(sites, ensure_ascii=False)
    return result


@app.route("/pm25-site")
def pm25_site():
    counties = get_all_counties()
    return render_template("pm25-site.html", counties=counties)


@app.route("/pm25-data-site")
def pm25_by_site():
    # 取得縣市和測站
    county = request.args.get("county")
    site = request.args.get("site")

    if not county or not site:
        result = json.dumps({"error": "請提供正確縣市和測站參數"}, ensure_ascii=False)

    else:
        datas, columns = get_pm25_by_site(county, site)
        df = pd.DataFrame(datas, columns=columns)
        date = df["datacreationdate"].apply(lambda x: x.strftime("%Y-%m-%d %H"))

        data = {
            "county": county,
            "site": site,
            "x_data": date.to_list(),
            "y_data": df["pm25"].to_list(),
            "higher": df["pm25"].max(),
            "lower": df["pm25"].min(),
        }

        result = json.dumps(data, ensure_ascii=False)

    return result


@app.route("/update_db")
def update_pm25():
    row_counts, message = update_db()
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = json.dumps(
        {"更新比數": row_counts, "結果": message, "時間": time}, ensure_ascii=False
    )

    return result


@app.route("/")
def index():
    # 取得最新資料
    datas, columns = get_pm25_data()
    # 取出不同縣市資料
    df = pd.DataFrame(datas, columns=columns)
    # 排序縣市
    counties = sorted(df["county"].unique().tolist())
    # print(counties)

    # 取得特定縣市資料(預設ALL)
    county = request.args.get("county", "全部縣市")

    if county == "全部縣市":
        # 取得所有縣市的平均值，以縣市為單位
        df1 = df.groupby("county")["pm25"].mean().reset_index()
        x_data = df1["county"].to_list()
    else:
        # 取得特定縣市資料，以測站為單位
        df = df.groupby("county").get_group(county)
        # 取得繪製資料
        x_data = df["site"].tolist()

    y_data = df["pm25"].tolist()
    columns = df.columns.tolist()
    datas = df.values.tolist()
    # print(columns, datas)

    return render_template(
        "index.html",
        columns=columns,
        datas=datas,
        counties=counties,
        selected_county=county,
        x_data=x_data,
        y_data=y_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
