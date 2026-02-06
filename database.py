import sqlite3

# Function to create the database and tables if they don't exist
def create_tables():
    # Connect to the SQLite database (creates 'tourism.db' if it doesn't exist)
    conn = sqlite3.connect('tourism.db')
    cursor = conn.cursor()
    
    # Create PLACES table
    # - id: Auto-incrementing primary key
    # - place_name: Name of the place (required)
    # - festival_code: Unique code for the place (required and unique)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PLACES (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            place_name TEXT NOT NULL,
            festival_code TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Create VISITS table
    # - id: Auto-incrementing primary key
    # - place_code: Code of the place (references festival_code from PLACES)
    # - people_count: Number of people (required)
    # - visit_date: Date of visit (stored as TEXT in YYYY-MM-DD format)
    # - visit_time: Time of visit (stored as TEXT in HH:MM:SS format)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS VISITS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            place_code TEXT NOT NULL,
            people_count INTEGER NOT NULL,
            visit_date TEXT NOT NULL,
            visit_time TEXT NOT NULL
        )
    ''')
    
    # Save changes and close the connection
    conn.commit()
    conn.close()

# Function to get a database connection
# Returns a connection with row_factory set to Row for easy dict-like access
def get_db_connection():
    conn = sqlite3.connect('tourism.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

# If this file is run directly, create the tables and print a message
if __name__ == '__main__':
    create_tables()
    print("Database and tables created successfully!")