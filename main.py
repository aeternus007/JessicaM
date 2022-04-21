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
            return redirect(url_for("edit_booking", email=email))
    if not df:
        df = pd.DataFrame(query(conn, "SELECT * FROM Movie"))

    return render_template('more_info.html', df=df)
               
               
@app.route("/bookings/<email>", methods=["POST", "GET"])
def bookings(email):
    conn = get_db(DATABASE, g)
    bookings = query(conn, "select * from Booking where email = ?", email)
               
    return render_template("bookings.html", bookings=bookings, email=email)
               

@app.route("/edit/<email>/<booking_id>", methods=["POST", "GET"])
def edit_booking(email, booking_id):
    conn = get_db(DATABASE, g)
    booking = query(conn, "select * from Booking where Booking_id = ?", booking_id)

    if request.method == "POST":
        query(conn, "update Booking set amount = ? where Booking_id = ?", request.form["amount"], booking_id
               
    return render_template("edit_booking.html", booking=booking, id=booking_id, ammount)


if __name__ == '__main__':
    app.run(debug=True)
