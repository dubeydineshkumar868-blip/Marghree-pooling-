import sqlite3
import os
from datetime import datetime
import hashlib

# Database file name
DB_FILE = "margshree.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables with IF NOT EXISTS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            city TEXT,
            is_verified INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
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
            budget INTEGER, status TEXT DEFAULT 'pending', created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (rider_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS driver_verification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            aadhar_number TEXT,
            driving_license TEXT,
            rc_number TEXT,
            pan_number TEXT,
            verification_status TEXT DEFAULT 'pending',
            submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- Authentication Functions ---
def signup_user(name, password, role, email=None, phone=None, city=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check duplicates
        existing = None
        if email:
            existing = cursor.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if not existing and phone:
            existing = cursor.execute('SELECT id FROM users WHERE phone = ?', (phone,)).fetchone()
        
        if existing:
            conn.close()
            return None, "Email or phone already registered!"
        
        hashed_pw = hash_password(password)
        
        cursor.execute('''
            INSERT INTO users (name, email, phone, password, role, city)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, hashed_pw, role, city))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return user_id, "Signup successful!"
    except Exception as e:
        print(f"Signup error: {e}")
        return None, f"Error creating account: {str(e)}"

def login_user(email_phone, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        user = cursor.execute('''
            SELECT * FROM users WHERE email = ? OR phone = ?
        ''', (email_phone, email_phone)).fetchone()
        
        conn.close()
        
        if not user:
            return None, "User not found!"
        
        hashed_input = hash_password(password)
        if dict(user)['password'] != hashed_input:
            return None, "Incorrect password!"
        
        return dict(user), "Login successful!"
    except Exception as e:
        print(f"Login error: {e}")
        return None, f"Login error: {str(e)}"

# --- User Functions ---
def add_user(name, role, phone=None, city=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, phone, role, city, password)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, phone, role, city, hash_password("demo123")))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None

# --- Rides Functions ---
def add_ride(driver_id, driver_name, ride_type, vehicle_icon, from_city, to_city, date, time, seats, price, vehicle_number):
    try:
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
    except Exception as e:
        print(f"Add ride error: {e}")
        return None

def get_all_rides():
    try:
        conn = get_db_connection()
        rides = conn.execute('SELECT * FROM rides ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(r) for r in rides]
    except Exception as e:
        print(f"Get rides error: {e}")
        return []

def get_rides_by_filters(from_city=None, to_city=None, ride_type=None, max_price=None):
    try:
        conn = get_db_connection()
        query = 'SELECT * FROM rides WHERE 1=1'
        params = []
        
        if from_city and from_city not in ['Any', 'Any City']:
            query += ' AND from_city = ?'
            params.append(from_city)
        if to_city and to_city not in ['Any', 'Any City']:
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
        return [dict(r) for r in rides]
    except Exception as e:
        print(f"Filter rides error: {e}")
        return []

# --- Ride Requests Functions ---
def add_ride_request(rider_id, rider_name, from_city, to_city, date, time, passengers, budget):
    try:
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
    except Exception as e:
        print(f"Add request error: {e}")
        return None

def get_all_ride_requests():
    try:
        conn = get_db_connection()
        requests = conn.execute('SELECT * FROM ride_requests ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(r) for r in requests]
    except Exception as e:
        print(f"Get requests error: {e}")
        return []

# --- Bookings Functions ---
def add_booking(ride_id, rider_id, rider_name, passengers=1):
    try:
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
    except Exception as e:
        print(f"Add booking error: {e}")
        return None

def get_user_bookings(user_id):
    try:
        conn = get_db_connection()
        bookings = conn.execute('''
            SELECT b.*, r.from_city, r.to_city, r.date as ride_date, r.time as ride_time, r.price, r.driver_name
            FROM bookings b
            JOIN rides r ON b.ride_id = r.id
            WHERE b.rider_id = ?
            ORDER BY b.booking_date DESC
        ''', (user_id,)).fetchall()
        conn.close()
        return [dict(b) for b in bookings]
    except Exception as e:
        print(f"Get bookings error: {e}")
        return []

# --- Driver Verification ---
def submit_driver_verification(user_id, aadhar=None, license=None, rc=None, pan=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        existing = cursor.execute('SELECT id FROM driver_verification WHERE user_id = ?', (user_id,)).fetchone()
        
        if existing:
            cursor.execute('''
                UPDATE driver_verification 
                SET aadhar_number=?, driving_license=?, rc_number=?, pan_number=?, verification_status='pending'
                WHERE user_id=?
            ''', (aadhar, license, rc, pan, user_id))
        else:
            cursor.execute('''
                INSERT INTO driver_verification (user_id, aadhar_number, driving_license, rc_number, pan_number)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, aadhar, license, rc, pan))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Verification error: {e}")

# Initialize database
if __name__ == "__main__":
    init_db()
