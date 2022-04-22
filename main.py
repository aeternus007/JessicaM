import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, g, flash

from utils import query, get_db


DATABASE = 'test.sqlite3'

app = Flask(__name__)


@app.route('/')
def home():
    conn = get_db(DATABASE, g)
    df = pd.DataFrame(query(conn, "SELECT * FROM Movie")[:5])

    return render_template('home.html', df=df)


@app.route("/more_info", methods=['POST', 'GET'])
def more_info():
    conn = get_db(DATABASE, g)
    df = None

    if request.method == 'POST':
        email = request.form['email']
        if len(query(conn, "SELECT * FROM Booking WHERE Email = ?", (email, ))) == 0:
            df = "No bookings from that email."
        else:
            return redirect(url_for("bookings", email=email))
    if not df:
        df = pd.DataFrame(query(conn, "SELECT * FROM Movie"))

    return render_template('more_info.html', df=df)
               
               
@app.route("/bookings/<email>", methods=["POST", "GET"])
def bookings(email):
    conn = get_db(DATABASE, g)
    bookings = query(conn, "select * from Booking where Email = ?", (email, ))
    if len(bookings) < 1:
        flash("there are no bookings with that email!", "warning")
        bookings = ["There are no bookings"]
               
    return render_template("bookings.html", bookings=bookings, email=email)
               

@app.route("/edit/<email>/<booking_id>", methods=["POST", "GET"])
def edit_bookings(email, booking_id):
    conn = get_db(DATABASE, g)
    booking = query(conn, "select * from Booking where Booking_id = ?", (booking_id,))
    amount = booking[0][-1]
    viewing = query(conn, "select Movie_id from Viewing where Viewing_id = ?", (booking[0][1],))
    movie = query(conn, "select Title from Movie where Movie_ID = ?", (viewing[0][0],))[0][0][0:]
  
    if request.method == "POST":
        query(conn, "update Booking set No_Booking = ? where Booking_id = ?", (request.form["amount"], booking_id))
        booking = query(conn, "select * from Booking where Booking_id = ?", (booking_id,))
        amount = booking[0][-1]
        flash(f"succesfully edited ticket amount to {amount}", "succes")    
        
    return render_template("edit_bookings.html", booking=booking, id=booking_id, amount=amount, email=email, film_title=movie)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
