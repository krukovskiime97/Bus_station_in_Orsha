from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# connect on bd pgadmin
conn = psycopg2.connect(
    host="localhost",
    database="avtovokzal",
    user="postgres",
    password="12345"
)
cur = conn.cursor()

# create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS bus_stations (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        address VARCHAR(255),
        phone VARCHAR(20)
    )
""")
conn.commit()


# offical page site
@app.route('/')
def index():
    cur.execute("SELECT * FROM bus_stations")
    stations = cur.fetchall()
    return render_template('index.html', stations=stations)


# page add bus_station
@app.route('/add', methods=['GET', 'POST'])
def add_station():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']

        cur.execute("""
            INSERT INTO bus_stations (name, address, phone)
            VALUES (%s, %s, %s)
        """, (name, address, phone))
        conn.commit()

    return render_template('add_station.html')


if __name__ == '__main__':
    app.run(debug=True)

