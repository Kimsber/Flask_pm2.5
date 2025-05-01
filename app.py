from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
from pm25 import get_pm25_data, update_db
import json

app = Flask(__name__)


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
    datas, columns = get_pm25_data()
    # print(datas, columns)
    return render_template("index.html", **locals())


@app.route("/books")
def books_recommand():
    books = [
        {
            "name": "Python book",
            "price": 299,
            "image_url": "https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348",
        },
        {
            "name": "Java book",
            "price": 399,
            "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348",
        },
        {
            "name": "C# book",
            "price": 499,
            "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348",
        },
    ]

    if books:
        for book in books:
            print(book["name"])
            print(book["price"])
            print(book["image_url"])
    else:
        print("No books found")

    username = "Kim"
    login_time = datetime.now().strftime("%Y-%m-%d")
    print(username, login_time)
    return render_template("books.html", name=username, time=login_time, books=books)


@app.route("/bmi")
def get_bmi():
    height = eval(request.args.get("height"))
    weight = eval(request.args.get("weight"))
    bmi = round(weight / (height / 100) ** 2, 2)
    return render_template("bmi.html", **locals())


if __name__ == "__main__":
    app.run(debug=True)
