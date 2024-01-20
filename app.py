from flask import Flask, render_template, request
import psycopg2

# Flask app
app = Flask(__name__)

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="avtovokzal",
    user="postgres",
    password="12345"
)
cur = conn.cursor()

# Create table bus_stations
cur.execute("""
    CREATE TABLE IF NOT EXISTS bus_stations (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        address VARCHAR(255),
        phone VARCHAR(20),
        seats_available INTEGER
    )
""")
conn.commit()


# SQL request
@app.route('/')
def index():
    cur.execute("SELECT * FROM bus_stations")
    stations = cur.fetchall()
    return render_template('index.html', stations=stations)


# GET, POST, request
@app.route('/add', methods=['GET', 'POST'])
def add_station():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        seats_available = request.form['seats_available']

        cur.execute("""
            INSERT INTO bus_stations (name, address, phone, seats_available)
            VALUES (%s, %s, %s, %s)
        """, (name, address, phone, seats_available))
        conn.commit()

    return render_template('add_station.html')


# Flask app
if __name__ == '__main__':
    app.run(debug=True)

