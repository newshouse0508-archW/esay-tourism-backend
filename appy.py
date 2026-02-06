from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db_connection, create_tables  # Import functions from database.py
from datetime import datetime, date

# Create the Flask app
app = Flask(__name__)

# Enable CORS for all routes (allows requests from different origins, e.g., a frontend)
CORS(app)

# Create tables when the app starts (ensures database is ready)
create_tables()

# POST /add_place
# Adds a new place to the PLACES table
# Input: JSON with 'place_name' and 'festival_code'
# Output: Success message or error if festival_code is not unique
@app.route('/add_place', methods=['POST'])
def add_place():
    # Get JSON data from the request
    data = request.get_json()
    place_name = data.get('place_name')
    festival_code = data.get('festival_code')
    
    # Validate input
    if not place_name or not festival_code:
        return jsonify({'error': 'place_name and festival_code are required'}), 400
    
    # Connect to the database
    conn = get_db_connection()
    try:
        # Insert the new place
        conn.execute('INSERT INTO PLACES (place_name, festival_code) VALUES (?, ?)', (place_name, festival_code))
        conn.commit()
        return jsonify({'message': 'Place added successfully'}), 201
    except sqlite3.IntegrityError:
        # Handle unique constraint violation
        return jsonify({'error': 'Festival code already exists'}), 400
    finally:
        conn.close()

# POST /add_visit
# Adds a new visit to the VISITS table
# Input: JSON with 'place_code' and 'people_count'
# Automatically stores current date and time
# Output: Success message
@app.route('/add_visit', methods=['POST'])
def add_visit():
    # Get JSON data from the request
    data = request.get_json()
    place_code = data.get('place_code')
    people_count = data.get('people_count')
    
    # Validate input
    if not place_code or people_count is None or people_count < 0:
        return jsonify({'error': 'place_code and valid people_count are required'}), 400
    
    # Get current date and time
    now = datetime.now()
    visit_date = now.strftime('%Y-%m-%d')  # Format: YYYY-MM-DD
    visit_time = now.strftime('%H:%M:%S')  # Format: HH:MM:SS
    
    # Connect to the database
    conn = get_db_connection()
    conn.execute('INSERT INTO VISITS (place_code, people_count, visit_date, visit_time) VALUES (?, ?, ?, ?)', 
                 (place_code, people_count, visit_date, visit_time))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Visit added successfully'}), 201

# GET /all_visits
# Returns all visits from the VISITS table
# Output: JSON list of all visits
@app.route('/all_visits', methods=['GET'])
def all_visits():
    # Connect to the database
    conn = get_db_connection()
    visits = conn.execute('SELECT * FROM VISITS').fetchall()
    conn.close()
    
    # Convert rows to dictionaries and return as JSON
    return jsonify([dict(row) for row in visits])

# GET /today_visits
# Returns only today's visits from the VISITS table
# Output: JSON list of today's visits
@app.route('/today_visits', methods=['GET'])
def today_visits():
    # Get today's date
    today = date.today().strftime('%Y-%m-%d')
    
    # Connect to the database
    conn = get_db_connection()
    visits = conn.execute('SELECT * FROM VISITS WHERE visit_date = ?', (today,)).fetchall()
    conn.close()
    
    # Convert rows to dictionaries and return as JSON
    return jsonify([dict(row) for row in visits])

# GET /crowd_status/<place_code>
# Returns the total people count for today for the given place_code
# Output: JSON with place_code and total_people
@app.route('/crowd_status/<place_code>', methods=['GET'])
def crowd_status(place_code):
    # Get today's date
    today = date.today().strftime('%Y-%m-%d')
    
    # Connect to the database
    conn = get_db_connection()
    result = conn.execute('SELECT SUM(people_count) as total FROM VISITS WHERE place_code = ? AND visit_date = ?', 
                          (place_code, today)).fetchone()
    conn.close()
    
    # Get the total (default to 0 if no visits)
    total = result['total'] if result['total'] else 0
    
    return jsonify({'place_code': place_code, 'total_people': total})

# Run the app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)  # Debug mode for development