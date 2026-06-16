import sqlite3
import os
from datetime import datetime
import hashlib
import base64

# Database file name
DB_FILE = "margshree.db"

def get_db_connection():
    """Database connection create karega"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Password ko secure hash mein convert karein"""
    # Simple but secure enough for demo
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Database aur tables ko initialize karega"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table (Updated with password and verification fields)
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

    # 2. Rides Table (No change needed, just for reference)
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

    # 3. Bookings Table (No change needed)
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

    # 4. Ride Requests Table (No change needed)
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
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (rider_id) REFERENCES users (id)
        )
    ''')

    # 5. Driver Verification Table (New!)
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
    print("✅ Database aur tables initialize ho gaye!")

# --- Authentication Functions ---
def signup_user(name, password, role, email=None, phone=None, city=None):
    """Naya user register karega"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if email/phone already exists
    existing = None
    if email:
        existing = cursor.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
    if not existing and phone:
        existing = cursor.execute('SELECT id FROM users WHERE phone = ?', (phone,)).fetchone()
    
    if existing:
        conn.close()
        return None, "Email ya phone already registered hai!"
    
    # Hash password
    hashed_pw = hash_password(password)
    
    cursor.execute('''
        INSERT INTO users (name, email, phone, password, role, city)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, phone, hashed_pw, role, city))
    
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id, "Signup successful!"

def login_user(email_phone, password):
    """User ko login karega"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    user = cursor.execute('''
        SELECT * FROM users WHERE email = ? OR phone = ?
    ''', (email_phone, email_phone)).fetchone()
    
    conn.close()
    
    if not user:
        return None, "User nahi mila!"
    
    # Verify password
    hashed_input = hash_password(password)
    if user['password'] != hashed_input:
        return None, "Galat password!"
    
    return dict(user), "Login successful!"

# --- Existing User Functions (Updated) ---
def add_user(name, role, phone=None, city=None):
    """Naya user add karega (simple, no password - for demo fallback)"""
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
    """ID se user details lein"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None

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
    return [dict(r) for r in rides]

def get_rides_by_filters(from_city=None, to_city=None, ride_type=None, max_price=None):
    """Filters ke according rides lein"""
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
    return [dict(r) for r in requests]

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
    return [dict(b) for b in bookings]

# --- Driver Verification Functions ---
def submit_driver_verification(user_id, aadhar=None, license=None, rc=None, pan=None):
    """Driver verification submit karega"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if already exists
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

# Initialize database when file runs
if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        init_db()
        print(f"✅ Database file ban gaya: {DB_FILE}")
    else:
        print(f"ℹ️ Database already exists: {DB_FILE}")
