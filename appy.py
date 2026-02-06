from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime, date

app = Flask(__name__)
CORS(app)

# --------------------------
# DATABASE INIT
# --------------------------
def init_db():
    conn = sqlite3.connect("tourism.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS visits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place_code TEXT,
        people_count INTEGER,
        visit_date TEXT,
        visit_time TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# --------------------------
# ADD VISIT
# --------------------------
@app.route("/add_visit", methods=["POST"])
def add_visit():
    data = request.get_json()
    place_code = data.get("place_code")
    people_count = data.get("people_count")

    today = date.today().isoformat()
    time_now = datetime.now().strftime("%H:%M:%S")

    conn = sqlite3.connect("tourism.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO visits(place_code, people_count, visit_date, visit_time)
        VALUES(?,?,?,?)
    """, (place_code, people_count, today, time_now))

    conn.commit()
    conn.close()

    return jsonify({"message":"Visit Added Successfully"})

# --------------------------
# ALL VISITS
# --------------------------
@app.route("/all_visits")
def all_visits():
    conn = sqlite3.connect("tourism.db")
    cur = conn.cursor()

    cur.execute("SELECT place_code, people_count, visit_date, visit_time FROM visits")
    rows = cur.fetchall()
    conn.close()

    data=[]
    for r in rows:
        data.append({
            "place_code": r[0],
            "people_count": r[1],
            "visit_date": r[2],
            "visit_time": r[3]
        })

    return jsonify(data)

# --------------------------
# TODAY VISITS
# --------------------------
@app.route("/today_visits")
def today_visits():
    today = date.today().isoformat()

    conn = sqlite3.connect("tourism.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT place_code, people_count, visit_date, visit_time
        FROM visits WHERE visit_date=?
    """,(today,))

    rows = cur.fetchall()
    conn.close()

    data=[]
    for r in rows:
        data.append({
            "place_code": r[0],
            "people_count": r[1],
            "visit_date": r[2],
            "visit_time": r[3]
        })

    return jsonify(data)

# --------------------------
# RUN SERVER
# --------------------------
app.run(host="0.0.0.0", port=10000)
