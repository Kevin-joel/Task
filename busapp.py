from flask import Flask, render_template, request, redirect, url_for, flash
from math import ceil

app = Flask(__name__)
app.secret_key = "simple-key"

# In-memory data
buses = {
    "Hyderabad": ["GreenLine Express", "CityLink Travels"],
    "Chennai": ["RedBus", "SkyLine"],
    "Banglore":["Intrcity","flixbus"],
    "Vizag":["SRKT","Dasari"]
}

bookings = {}  # { (destination, bus): [seat_numbers] }

@app.route('/')
def index():
    return render_template("index.html", buses=buses)

@app.route('/choose_bus', methods=['POST'])
def choose_bus():
    destination = request.form['destination']
    return render_template("bus.html", destination=destination, buses=buses[destination])

@app.route('/seats', methods=['POST'])
def seats():
    destination = request.form['destination']
    bus = request.form['bus']
    key = (destination, bus)
    booked = bookings.get(key, [])

    # simple seat layout: 12 seats, 4 per row
    seat_rows = []
    seats = 12
    cols = 4
    for r in range(ceil(seats/cols)):
        row = []
        for c in range(1, cols+1):
            seat_no = f"{chr(65+r)}{c}"
            if (r*cols + c-1) < seats:
                row.append(seat_no)
        seat_rows.append(row)

    return render_template("seats.html", destination=destination, bus=bus, seat_rows=seat_rows, booked=booked)

@app.route('/book', methods=['POST'])
def book():
    destination = request.form['destination']
    bus = request.form['bus']
    seat = request.form['seat_number']
    key = (destination, bus)

    if not seat:
        flash("Please select a seat")
        return redirect(url_for('index'))

    if seat in bookings.get(key, []):
        flash("Seat already booked")
        return redirect(url_for('index'))

    bookings.setdefault(key, []).append(seat)
    flash(f"Seat {seat} reserved in {bus} to {destination}!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
