from flask import Flask, render_template, request, redirect, url_for, g

from utils import *


DATABASE = 'test.sqlite3'

app = Flask(__name__)


@app.route('/')
def home():
    conn = get_db(DATABASE, g)

    df = query(conn, "SELECT * FROM Movie")[:5]
    # print(movies)

    return render_template('home.html', df=df)


if __name__ == '__main__':
    app.run(debug=True)