import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, g

from utils import *


DATABASE = 'test.sqlite3'

app = Flask(__name__)


@app.route('/')
def home():
    conn = get_db(DATABASE, g)
    df = pd.DataFrame(query(conn, "SELECT * FROM Movie")[:5])
    # print(movies)

    return render_template('home.html', df=df)


@app.route("/more_info", methods=['POST', 'GET'])
def more_info():
    conn = get_db(DATABASE, g)
    df = None

    if request.method == 'POST':
        email = request.form['email']
        if len(query(conn, "SELECT * FROM Booking WHERE Email = ?", email) == 0:
            df = "No bookings from that email."
        else:
            df = query(conn, "SELECT * FROM Booking WHERE Email = ?", email)
    if not df:
        df = pd.DataFrame(query(conn, "SELECT * FROM Movie"))

    return render_template('more_info.html', df=df)
               
               
@app.route("edit_booking/<email>", methods=["POST", "GET"])
def edit_booking(email):
    conn = get_db(DATABASE, g)
    df = query(conn, "some query", email)



if __name__ == '__main__':
    app.run(debug=True)
