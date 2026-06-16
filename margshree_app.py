import streamlit as st
import random
from datetime import datetime, timedelta
import database as db

# Initialize database
db.init_db()

# Page Configuration
st.set_page_config(
    page_title="Margshree - India's Ride Sharing",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .hero-section {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #6366f1 100%);
        padding: 3rem 2rem;
        border-radius: 0 0 2.5rem 2.5rem;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 20px 60px rgba(79, 70, 229, 0.3);
    }
    .hero-title {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-align: center;
        text-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 1.5rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        max-width: 1000px;
        margin: 0 auto 2rem auto;
    }
    .ride-card {
        background: white;
        border-radius: 1.25rem;
        padding: 1.75rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    .ride-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        border-color: #4f46e5;
    }
    .ride-card-car { border-left: 5px solid #3b82f6; }
    .ride-card-bus { border-left: 5px solid #10b981; }
    .ride-card-rickshaw { border-left: 5px solid #f59e0b; }
    .price-tag {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1.25rem;
        border-radius: 0.5rem;
        font-weight: 700;
        font-size: 1.5rem;
        display: inline-block;
    }
    .role-card {
        background: white;
        padding: 2.5rem 2rem;
        border-radius: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 25px rgba(0,0,0,0.08);
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .role-card:hover {
        border-color: #4f46e5;
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(79, 70, 229, 0.2);
    }
    .role-icon { font-size: 5rem; margin-bottom: 1rem; }
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    .vehicle-icon { font-size: 1.5rem; margin-right: 0.5rem; }
    
    /* Fix login/signup text colors */
    .role-card div, .role-card h3, .role-card p,
    [data-testid="stTabs"] button,
    [data-testid="stTextInput"] label,
    [data-testid="stNumberInput"] label,
    [data-testid="stSelectbox"] label,
    [data-testid="stRadio"] label,
    [data-testid="stDateInput"] label,
    [data-testid="stTimeInput"] label,
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] div,
    [data-testid="stRadio"] div,
    .stTabs,
    .stMarkdown h3,
    .stMarkdown p {
        color: #1e293b !important;
    }
    
    /* Ensure input fields have proper contrast */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #f8fafc !important;
        border-color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Data Lists
INDIAN_CITIES = [
    "Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad",
    "Noida", "Mainpuri", "Agra", "Jaipur", "Lucknow", "Kanpur", "Varanasi", "Patna",
    "Surat", "Vadodara", "Rajkot", "Nagpur", "Indore", "Bhopal", "Ludhiana", "Chandigarh",
    "Kochi", "Thiruvananthapuram", "Coimbatore", "Madurai", "Visakhapatnam", "Vijayawada",
    "Guwahati", "Shillong", "Imphal", "Srinagar", "Amritsar", "Dehradun", "Rishikesh",
    "Haridwar", "Gurugram", "Faridabad", "Ghaziabad", "Meerut", "Prayagraj", "Jabalpur",
    "Raipur", "Bhubaneswar", "Cuttack", "Ranchi", "Dhanbad", "Jamshedpur", "Asansol",
    "Siliguri", "Dibrugarh", "Jorhat"
]
VEHICLE_TYPES = [
    ("Car", "🚗"),
    ("Bus", "🚌"),
    ("Battery Rickshaw", "🛺"),
    ("Bike", "🏍️"),
    ("SUV", "🚙")
]

# Helper Functions
def get_vehicle_class(ride_type):
    if ride_type == "Car":
        return "ride-card-car"
    elif ride_type == "Bus":
        return "ride-card-bus"
    elif ride_type == "Battery Rickshaw":
        return "ride-card-rickshaw"
    else:
        return "ride-card-car"

def add_sample_data():
    """Demo ke liye sample data add karein"""
    rides = db.get_all_rides()
    if len(rides) == 0:
        driver_names = ["Rajesh Kumar", "Suresh Singh", "Amit Sharma", "Priya Patel", "Rahul Verma"]
        for i in range(5):
            ride_type, icon = random.choice(VEHICLE_TYPES)
            from_city = random.choice(INDIAN_CITIES)
            to_city = random.choice([c for c in INDIAN_CITIES if c != from_city])
            date = (datetime.now() + timedelta(days=random.randint(0, 7))).strftime("%d %B %Y")
            time = f"{random.randint(6, 22):02d}:{random.choice(['00', '15', '30', '45'])}"
            seats = random.randint(2, 6)
            price = random.randint(100, 3000)
            vehicle_num = f"UP{random.randint(10, 99)}{random.choice(['ABC', 'XYZ', 'DEF'])}{random.randint(1000, 9999)}"
            db.add_ride(i+1, driver_names[i], ride_type, icon, from_city, to_city, date, time, seats, price, vehicle_num)
add_sample_data()

# Session State Init
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "login"

# --- Main App ---

# Hero Banner (Always Show)
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🚌 Margshree</h1>
    <p class="hero-subtitle">India's Most Trusted Ride Sharing Platform • Car • Bus • Auto • Bike</p>
</div>
""", unsafe_allow_html=True)

# --- Authentication Logic ---
if not st.session_state.logged_in:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">🔐</div>
            <h3 style="margin-bottom: 1.5rem; color: #1e293b;">Welcome! Please Login or Signup</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Login/Signup Tabs
        login_tab, signup_tab = st.tabs(["Login", "Signup"])
        
        with login_tab:
            st.markdown("### Login to Your Account")
            login_email_phone = st.text_input("Email/Phone", placeholder="Enter your email or phone")
            login_password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.button("Login", key="login_btn", use_container_width=True, type="primary"):
                if login_email_phone and login_password:
                    user, message = db.login_user(login_email_phone, login_password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.current_user = user
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please fill all fields!")
        
        with signup_tab:
            st.markdown("### Create New Account")
            signup_name = st.text_input("Full Name", placeholder="Enter your full name")
            signup_email = st.text_input("Email (Optional)", placeholder="Enter your email")
            signup_phone = st.text_input("Phone", placeholder="Enter your phone number")
            signup_password = st.text_input("Password", type="password", placeholder="Create a password")
            signup_city = st.selectbox("City", ["Select City"] + INDIAN_CITIES)
            signup_role = st.radio("I am a:", ["Rider", "Driver"], horizontal=True)
            
            if st.button("Create Account", key="signup_btn", use_container_width=True):
                if signup_name and signup_password:
                    city_val = signup_city if signup_city != "Select City" else None
                    role = "rider" if signup_role == "Rider" else "driver"
                    
                    user_id, message = db.signup_user(
                        signup_name, signup_password, role, 
                        email=signup_email or None,
                        phone=signup_phone or None,
                        city=city_val
                    )
                    
                    if user_id:
                        user = db.get_user_by_id(user_id)
                        st.session_state.logged_in = True
                        st.session_state.current_user = user
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Name and Password are required!")

else:
    # --- Logged In View ---
    user = st.session_state.current_user
    
    # Header with User Info
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; background: white; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
        <div>
            <h3 style="margin: 0; color: #1e293b;">👋 Welcome, {user['name']}!</h3>
            <p style="margin: 0; color: #64748b; font-size: 0.9rem;">
                Role: {'🚗 Driver' if user['role'] == 'driver' else '🧑‍💼 Rider'} • 
                City: {user['city'] or 'Not Set'}
            </p>
        </div>
        <div style="display: flex; gap: 1rem;">
    """, unsafe_allow_html=True)
    
    if st.button("Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Search Container
    st.markdown("""
    <div class="search-container">
        <h3 style="text-align: center; color: #1e293b; margin-bottom: 1.5rem; font-size: 1.75rem; font-weight: 700;">Find Your Perfect Ride</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 2, 1.5, 1.5])
    with col1:
        from_city = st.selectbox("From City", ["Any City"] + INDIAN_CITIES, key="home_from")
    with col2:
        to_city = st.selectbox("To City", ["Any City"] + INDIAN_CITIES, key="home_to")
    with col3:
        date_input = st.date_input("Date", datetime.now(), key="home_date")
    with col4:
        vehicle_filter = st.selectbox("Vehicle", ["All"] + [vt[0] for vt in VEHICLE_TYPES], key="home_vehicle")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Role Specific Dashboard ---
    if user['role'] == 'rider':
        # Rider Dashboard
        rider_tab1, rider_tab2, rider_tab3 = st.tabs(["🔍 Find Rides", "📋 Request Ride", "📝 My Bookings"])
        
        with rider_tab1:
            filtered_rides = db.get_rides_by_filters(from_city, to_city, vehicle_filter)
            
            if len(filtered_rides) > 0:
                st.markdown(f"### ✨ {len(filtered_rides)} Rides Found")
                for ride in filtered_rides:
                    card_class = get_vehicle_class(ride['ride_type'])
                    st.markdown(f"""
                    <div class="ride-card {card_class}">
                        <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 1rem;">
                            <div style="flex: 1; min-width: 250px;">
                                <h4 style="margin: 0 0 0.5rem 0; color: #1e293b; font-weight: 700;">
                                    {ride['vehicle_icon']} {ride['ride_type']} • {ride['from_city']} → {ride['to_city']}
                                </h4>
                                <p style="color: #64748b; margin: 0.25rem 0;">
                                    📅 {ride['date']} • ⏰ {ride['time']} • 💺 {ride['seats']} seats • 
                                    Driver: {ride['driver_name']} ({ride['vehicle_number']})
                                </p>
                            </div>
                            <div style="text-align: center;">
                                <div class="price-tag">₹{ride['price']}</div>
                                <p style="color: #64748b; margin-top: 0.5rem; font-size: 0.875rem;">per seat</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Book Now - {ride['driver_name']}", key=f"book_{ride['id']}", type="primary"):
                        db.add_booking(ride['id'], user['id'], user['name'])
                        st.balloons()
                        st.success("✅ Ride Booked Successfully!")
            else:
                st.info("No rides found. Try different filters!")
        
        with rider_tab2:
            st.markdown("### Request a Custom Ride")
            col_a, col_b = st.columns(2)
            with col_a:
                r_from = st.selectbox("From", INDIAN_CITIES, key="req_from_city")
                r_date = st.date_input("Date", key="req_date")
                r_budget = st.number_input("Your Budget (₹)", 50, 5000, 500)
            with col_b:
                r_to = st.selectbox("To", INDIAN_CITIES, key="req_to_city")
                r_time = st.time_input("Time", key="req_time")
                r_pass = st.number_input("Passengers", 1, 10, 1, key="req_pass")
            if st.button("Submit Request", type="primary"):
                db.add_ride_request(user['id'], user['name'], r_from, r_to, 
                                   r_date.strftime("%d %B %Y"), r_time.strftime("%H:%M"), 
                                   r_pass, r_budget)
                st.balloons()
                st.success("✅ Ride Request Submitted! Drivers will see your request.")
        
        with rider_tab3:
            st.markdown("### My Bookings")
            bookings = db.get_user_bookings(user['id'])
            if len(bookings) > 0:
                for b in bookings:
                    st.markdown(f"""
                    <div class="ride-card">
                        <h4 style="margin: 0 0 0.5rem 0; color: #1e293b; font-weight: 700;">
                            {b['from_city']} → {b['to_city']}
                        </h4>
                        <p style="color: #64748b; margin: 0;">
                            Driver: {b['driver_name']} • Date: {b['ride_date']} • Time: {b['ride_time']} • 
                            Fare: ₹{b['price']} • Status: {b['status']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No bookings yet!")
    
    else:
        # Driver Dashboard
        driver_tab1, driver_tab2, driver_tab3, driver_tab4 = st.tabs(
            ["📋 Ride Requests", "🚗 Offer Ride", "📝 My Rides", "📄 Verify Profile"]
        )
        
        with driver_tab1:
            st.markdown("### Passenger Ride Requests")
            reqs = db.get_all_ride_requests()
            col_f, col_t = st.columns(2)
            with col_f:
                f_city = st.selectbox("From City", ["Any"] + INDIAN_CITIES, key="d_req_from")
            with col_t:
                t_city = st.selectbox("To City", ["Any"] + INDIAN_CITIES, key="d_req_to")
            
            if len(reqs) > 0:
                for req in reqs:
                    if (f_city == "Any" or req['from_city'] == f_city) and (t_city == "Any" or req['to_city'] == t_city):
                        st.markdown(f"""
                        <div class="ride-card">
                            <h4 style="margin: 0 0 0.5rem 0; color: #1e293b; font-weight: 700;">
                                👤 {req['rider_name']} • {req['from_city']} → {req['to_city']}
                            </h4>
                            <p style="color: #64748b; margin: 0;">
                                📅 {req['date']} • ⏰ {req['time']} • {req['passengers']} Passengers • Budget: ₹{req['budget']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"Accept Request", key=f"accept_{req['id']}"):
                            st.success("✅ Request Accepted!")
            else:
                st.info("No requests yet!")
        
        with driver_tab2:
            st.markdown("### Offer Your Ride")
            col_c, col_d = st.columns(2)
            with col_c:
                d_vehicle, d_icon = st.selectbox("Vehicle Type", VEHICLE_TYPES, format_func=lambda x: f"{x[1]} {x[0]}")
                d_from = st.selectbox("From", INDIAN_CITIES, key="d_from")
                d_vehicle_num = st.text_input("Vehicle Number", placeholder="e.g., UP16AB1234")
            with col_d:
                d_to = st.selectbox("To", INDIAN_CITIES, key="d_to")
                d_date = st.date_input("Date", key="d_date")
                d_time = st.time_input("Time", key="d_time")
                d_seats = st.number_input("Seats", 1, 50, 3)
                d_price = st.number_input("Price/Seat (₹)", 20, 5000, 200)
            if st.button("Publish Ride", type="primary", use_container_width=True):
                if d_vehicle_num:
                    db.add_ride(user['id'], user['name'], d_vehicle, d_icon,
                              d_from, d_to, d_date.strftime("%d %B %Y"),
                              d_time.strftime("%H:%M"), d_seats, d_price, d_vehicle_num)
                    st.balloons()
                    st.success("✅ Ride Published!")
                else:
                    st.error("Please enter vehicle number!")
        
        with driver_tab3:
            st.markdown("### My Offered Rides")
            my_rides = [r for r in db.get_all_rides() if r['driver_id'] == user['id']]
            if len(my_rides) > 0:
                for ride in my_rides:
                    card_class = get_vehicle_class(ride['ride_type'])
                    st.markdown(f"""
                    <div class="ride-card {card_class}">
                        <h4 style="margin: 0 0 0.5rem 0; color: #1e293b; font-weight: 700;">
                            {ride['vehicle_icon']} {ride['ride_type']} • {ride['from_city']} → {ride['to_city']}
                        </h4>
                        <p style="color: #64748b; margin: 0;">
                            📅 {ride['date']} • ⏰ {ride['time']} • 💺 {ride['seats']} seats • ₹{ride['price']}/seat
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No rides offered yet!")
        
        with driver_tab4:
            st.markdown("### Driver Verification (KYC)")
            st.info("Submit your documents for verification to build trust with riders!")
            col_e, col_f = st.columns(2)
            with col_e:
                kyc_aadhar = st.text_input("Aadhar Number", placeholder="Enter your Aadhar number")
                kyc_license = st.text_input("Driving License", placeholder="Enter your license number")
            with col_f:
                kyc_rc = st.text_input("Vehicle RC Number", placeholder="Enter RC number")
                kyc_pan = st.text_input("PAN Number (Optional)", placeholder="Enter PAN number")
            if st.button("Submit for Verification", type="primary"):
                db.submit_driver_verification(user['id'], kyc_aadhar, kyc_license, kyc_rc, kyc_pan)
                st.success("✅ Verification Documents Submitted! We will verify soon.")

# Footer
st.markdown("""
<div style="text-align: center; padding: 3rem 2rem; margin-top: 4rem; background: #1e1b4b; border-radius: 2rem 2rem 0 0;">
    <h3 style="margin-bottom: 1rem; font-size: 1.5rem; color: white !important;">🚌 Margshree</h3>
    <p style="color: rgba(255, 255, 255, 0.9) !important; margin-bottom: 0.5rem;">India's Most Trusted Ride Sharing Platform</p>
    <p style="color: rgba(255, 255, 255, 0.7) !important; font-size: 0.875rem;">Made with ❤️ in India • © 2026 Margshree</p>
</div>
""", unsafe_allow_html=True)
