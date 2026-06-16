import sqlite3
import os
from datetime import datetime

# Database file name
DB_FILE = "margshree.db"

def get_db_connection():
    """Database connection create karega"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Taaki rows dictionary ki tarah access karein
    return conn

def init_db():
    """Database aur tables ko initialize karega"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table (Riders + Drivers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            role TEXT NOT NULL,  -- 'rider' ya 'driver'
            city TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Rides Table (Drivers ki offered rides)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_id INTEGER NOT NULL,
            driver_name TEXT NOT NULL,
            ride_type TEXT NOT NULL,
            vehicle_icon TEXT,
            from_city TEXT NOT NULL,
            to_city TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            seats INTEGER NOT NULL,
            price INTEGER NOT NULL,
            vehicle_number TEXT,
            rating REAL DEFAULT 5.0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (driver_id) REFERENCES users (id)
        )
    ''')

    # 3. Bookings Table (Riders ki booked rides)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ride_id INTEGER NOT NULL,
            rider_id INTEGER NOT NULL,
            rider_name TEXT NOT NULL,
            passengers INTEGER DEFAULT 1,
            booking_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'confirmed',
            FOREIGN KEY (ride_id) REFERENCES rides (id),
            FOREIGN KEY (rider_id) REFERENCES users (id)
        )
    ''')

    # 4. Ride Requests Table (Riders ki custom requests)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ride_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rider_id INTEGER NOT NULL,
            rider_name TEXT NOT NULL,
            from_city TEXT NOT NULL,
            to_city TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            passengers INTEGER DEFAULT 1,
            budget INTEGER,
            status TEXT DEFAULT 'pending',  -- 'pending', 'accepted', 'rejected'
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (rider_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database aur tables initialize ho gaye!")

# --- Users Functions ---
def add_user(name, role, phone=None, city=None):
    """Naya user add karega"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, phone, role, city)
        VALUES (?, ?, ?, ?)
    ''', (name, phone, role, city))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def get_user_by_id(user_id):
    """ID se user details lein"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user

# --- Rides Functions ---
def add_ride(driver_id, driver_name, ride_type, vehicle_icon, from_city, to_city, date, time, seats, price, vehicle_number):
    """Nayi ride add karega"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO rides (driver_id, driver_name, ride_type, vehicle_icon, from_city, to_city, date, time, seats, price, vehicle_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (driver_id, driver_name, ride_type, vehicle_icon, from_city, to_city, date, time, seats, price, vehicle_number))
    conn.commit()
    ride_id = cursor.lastrowid
    conn.close()
    return ride_id

def get_all_rides():
    """Sabhi rides lein"""
    conn = get_db_connection()
    rides = conn.execute('SELECT * FROM rides ORDER BY created_at DESC').fetchall()
    conn.close()
    return rides

def get_rides_by_filters(from_city=None, to_city=None, ride_type=None, max_price=None):
    """Filters ke according rides lein"""
    conn = get_db_connection()
    query = 'SELECT * FROM rides WHERE 1=1'
    params = []

    if from_city and from_city != 'Any' and from_city != 'Any City':
        query += ' AND from_city = ?'
        params.append(from_city)
    if to_city and to_city != 'Any' and to_city != 'Any City':
        query += ' AND to_city = ?'
        params.append(to_city)
    if ride_type and ride_type != 'All':
        query += ' AND ride_type = ?'
        params.append(ride_type)
    if max_price:
        query += ' AND price <= ?'
        params.append(max_price)

    query += ' ORDER BY created_at DESC'
    rides = conn.execute(query, params).fetchall()
    conn.close()
    return rides

# --- Ride Requests Functions ---
def add_ride_request(rider_id, rider_name, from_city, to_city, date, time, passengers, budget):
    """Nayi ride request add karega"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ride_requests (rider_id, rider_name, from_city, to_city, date, time, passengers, budget)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (rider_id, rider_name, from_city, to_city, date, time, passengers, budget))
    conn.commit()
    request_id = cursor.lastrowid
    conn.close()
    return request_id

def get_all_ride_requests():
    """Sabhi ride requests lein"""
    conn = get_db_connection()
    requests = conn.execute('SELECT * FROM ride_requests ORDER BY created_at DESC').fetchall()
    conn.close()
    return requests

# --- Bookings Functions ---
def add_booking(ride_id, rider_id, rider_name, passengers=1):
    """Nayi booking add karega"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (ride_id, rider_id, rider_name, passengers)
        VALUES (?, ?, ?, ?)
    ''', (ride_id, rider_id, rider_name, passengers))
    conn.commit()
    booking_id = cursor.lastrowid
    conn.close()
    return booking_id

def get_user_bookings(user_id):
    """User ki bookings lein"""
    conn = get_db_connection()
    bookings = conn.execute('''
        SELECT b.*, r.from_city, r.to_city, r.date AS ride_date, r.time AS ride_time, r.price, r.driver_name
        FROM bookings b
        JOIN rides r ON b.ride_id = r.id
        WHERE b.rider_id = ?
        ORDER BY b.booking_date DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return bookings

# Initialize database when file runs
if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        init_db()
        print(f"✅ Database file ban gaya: {DB_FILE}")
    else:
        print(f"ℹ️  Database already exists: {DB_FILE}")

