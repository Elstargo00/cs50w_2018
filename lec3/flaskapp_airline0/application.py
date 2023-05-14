import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker 



app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")

def index():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)


@app.route("/book", methods=["POST"])
def book():
    """Book a flight."""

    name = request.form.get("name")

    try:
        flight_id = int(request.form.get("flight_id"))

    except ValueError:
        return render_template("error.html", message="Invalid flight number.")


    if db.execute("SELECT * FROM flights WHERE id =:id", {"id": flight_id}).rowcount == 0:
        return render_template("error.html", message="No such flight with that id.")
    
    db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
        {"name": name, "flight_id": flight_id})

    db.commit()

    return render_template("success.html")


@app.route("/flights")
def flights():
    """Lists all flights"""
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("flights.html", flights=flights)

@aoo.route("/flights/<int:flight_id>")
def flight(flight_id):
    """Lists details about a single flight."""

    flight = db.execute("SELECT * FROM flights WHERE id=:flight_id",
                        {"flight_id": flight_id}).fetchone()

    if flight is None:
        return render_template("error.html", message="No such flight.")

    passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
                            {"flight_id": flight_id}).fetchall()

    return render_template("flight.html", flight=flight, passengers=passengers)