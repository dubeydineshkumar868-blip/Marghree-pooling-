import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import database as db  # Hamara database helper import karein

# Initialize database (agar pehle se na ho to ban jayega)
db.init_db()

# Page Configuration
st.set_page_config(
    page_title="Margshree - India's Ride Sharing",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Modern, Professional UI
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
        padding: 4rem 2rem;
        border-radius: 0 0 3rem 3rem;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 20px 60px rgba(79, 70, 229, 0.3);
    }
    
    .hero-title {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-align: center;
        text-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.3rem;
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
        margin: 0 auto;
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
    
    .ride-card-car {
        border-left: 5px solid #3b82f6;
    }
    
    .ride-card-bus {
        border-left: 5px solid #10b981;
    }
    
    .ride-card-rickshaw {
        border-left: 5px solid #f59e0b;
    }
    
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
    
    .role-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
    }
    
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    .vehicle-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Comprehensive Indian Cities List
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

# Vehicle Types
VEHICLE_TYPES = [
    ("Car", "🚗"),
    ("Bus", "🚌"),
    ("Battery Rickshaw", "🛺"),
    ("Bike", "🏍️"),
    ("SUV", "🚙")
]

# --- Helper Functions ---
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
    """Demo ke liye sample data add karein (agar pehle na ho)"""
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
            db.add_ride(1, driver_names[i], ride_type, icon, from_city, to_city, date, time, seats, price, vehicle_num)
        print("✅ Sample data added!")

# Add sample data if needed
add_sample_data()

# --- Session State Initialize ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'current_user_id' not in st.session_state:
    st.session_state.current_user_id = None
if 'current_user_name' not in st.session_state:
    st.session_state.current_user_name = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# --- Main Application ---

# Hero Section (Home Page)
if st.session_state.current_page == "home":
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🚌 Margshree</h1>
        <p class="hero-subtitle">India's Most Trusted Ride Sharing Platform • Car • Bus • Auto • Bike</p>
        
        <div class="search-container">
            <h3 style="text-align: center; color: #1e293b; margin-bottom: 1.5rem; font-size: 1.75rem; font-weight: 700;">Find Your Perfect Ride</h3>
    """, unsafe_allow_html=True)
    
    # Search Form
    col1, col2, col3, col4 = st.columns([2, 2, 1.5, 1.5])
    with col1:
        from_city = st.selectbox("From City", ["Any City"] + INDIAN_CITIES, key="home_from")
    with col2:
        to_city = st.selectbox("To City", ["Any City"] + INDIAN_CITIES, key="home_to")
    with col3:
        date_input = st.date_input("Date", datetime.now(), key="home_date")
    with col4:
        vehicle_filter = st.selectbox("Vehicle", ["All"] + [vt[0] for vt in VEHICLE_TYPES], key="home_vehicle")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Role Selection
    st.markdown("<div style='margin-top: 3rem;'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">🧑‍💼</div>
            <h3 style="color: #1e293b; font-size: 1.5rem; margin-bottom: 0.5rem;">Book a Ride</h3>
            <p style="color: #64748b; margin-bottom: 1.5rem;">Find rides going your way and book instantly</p>
        """, unsafe_allow_html=True)
        rider_name = st.text_input("Apna Naam", placeholder="Enter your name", key="rider_name_home")
        if st.button("Continue as Rider", key="find_rides_btn", use_container_width=True, type="primary"):
            if rider_name:
                user_id = db.add_user(rider_name, "rider")
                st.session_state.current_user_id = user_id
                st.session_state.current_user_name = rider_name
                st.session_state.user_role = "rider"
                st.session_state.current_page = "rider_dashboard"
                st.rerun()
            else:
                st.error("Please enter your name!")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">🚗</div>
            <h3 style="color: #1e293b; font-size: 1.5rem; margin-bottom: 0.5rem;">Offer a Ride</h3>
            <p style="color: #64748b; margin-bottom: 1.5rem;">Share your journey and earn money</p>
        """, unsafe_allow_html=True)
        driver_name = st.text_input("Apna Naam", placeholder="Enter your name", key="driver_name_home")
        if st.button("Continue as Driver", key="offer_ride_btn", use_container_width=True):
            if driver_name:
                user_id = db.add_user(driver_name, "driver")
                st.session_state.current_user_id = user_id
                st.session_state.current_user_name = driver_name
                st.session_state.user_role = "driver"
                st.session_state.current_page = "driver_dashboard"
                st.rerun()
            else:
                st.error("Please enter your name!")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display Search Results
    filtered_rides = db.get_rides_by_filters(from_city, to_city, vehicle_filter)
    
    st.markdown("<div style='margin-top: 3rem;'>", unsafe_allow_html=True)
    if len(filtered_rides) > 0:
        st.markdown(f"<h3 style='color: #1e293b; margin-bottom: 1.5rem; font-weight: 700;'>✨ {len(filtered_rides)} Rides Found</h3>", unsafe_allow_html=True)
        
        for ride in filtered_rides:
            card_class = get_vehicle_class(ride['ride_type'])
            st.markdown(f"""
            <div class="ride-card {card_class}">
                <div style='display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 1rem;'>
                    <div style='flex: 1; min-width: 250px;'>
                        <div style='display: flex; align-items: center; margin-bottom: 0.75rem;'>
                            <span class='vehicle-icon'>{ride['vehicle_icon']}</span>
                            <h3 style='margin: 0; color: #1e293b; font-size: 1.5rem; font-weight: 700;'>
                                {ride['ride_type']} • {ride['from_city']} → {ride['to_city']}
                            </h3>
                        </div>
                        <p style='color: #64748b; margin: 0.25rem 0;'>
                            <strong>Driver:</strong> {ride['driver_name']} • ⭐ {ride['rating']} • {ride['vehicle_number']}
                        </p>
                        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 1rem;'>
                            <div>
                                <p style='color: #64748b; margin: 0; font-weight: 600;'>Date</p>
                                <p style='color: #1e293b; margin: 0; font-weight: 600;'>📅 {ride['date']}</p>
                            </div>
                            <div>
                                <p style='color: #64748b; margin: 0; font-weight: 600;'>Time</p>
                                <p style='color: #1e293b; margin: 0; font-weight: 600;'>🕐 {ride['time']}</p>
                            </div>
                            <div>
                                <p style='color: #64748b; margin: 0; font-weight: 600;'>Seats Available</p>
                                <p style='color: #1e293b; margin: 0; font-weight: 600;'>💺 {ride['seats']}</p>
                            </div>
                        </div>
                    </div>
                    <div style='text-align: center;'>
                        <div class='price-tag'>₹{ride['price']}</div>
                        <p style='color: #64748b; margin-top: 0.5rem; font-size: 0.875rem;'>per seat</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div style='text-align: center; padding: 4rem 2rem; background: white; border-radius: 1.5rem;'>
            <div style='font-size: 5rem; margin-bottom: 1rem;'>🔍</div>
            <h3 style='color: #1e293b; margin-bottom: 0.5rem;'>No rides found</h3>
            <p style='color: #64748b;'>Try adjusting your search filters or request a ride</p>
        </div>
        """, unsafe_allow_html=True)


# --- Rider Dashboard ---
elif st.session_state.current_page == "rider_dashboard":
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;'>
        <h2 style='color: #1e293b; margin: 0; font-size: 2rem; font-weight: 700;'>
            🧑‍💼 Welcome {st.session_state.current_user_name}!
        </h2>
    """, unsafe_allow_html=True)
    if st.button("← Back to Home", key="rider_back"):
        st.session_state.current_page = "home"
        st.session_state.current_user_id = None
        st.session_state.current_user_name = None
        st.session_state.user_role = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Rider Navigation
    rider_tab1, rider_tab2, rider_tab3 = st.columns(3)
    with rider_tab1:
        if st.button("🔍 Search Rides", key="tab_search", use_container_width=True, type="primary"):
            st.session_state.rider_active_tab = "search"
    with rider_tab2:
        if st.button("📋 Request Ride", key="tab_request", use_container_width=True):
            st.session_state.rider_active_tab = "request"
    with rider_tab3:
        if st.button("📝 My Bookings", key="tab_bookings", use_container_width=True):
            st.session_state.rider_active_tab = "bookings"
    
    if 'rider_active_tab' not in st.session_state:
        st.session_state.rider_active_tab = "search"
    
    # Tab Content
    if st.session_state.rider_active_tab == "search":
        st.markdown("<h3 style='color: #1e293b; margin-top: 2rem; margin-bottom: 1.5rem; font-weight: 700;'>Find Your Ride</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            from_city = st.selectbox("From", ["Any"] + INDIAN_CITIES, key="rider_from")
        with col2:
            to_city = st.selectbox("To", ["Any"] + INDIAN_CITIES, key="rider_to")
        with col3:
            max_price = st.slider("Max Price (₹)", 50, 5000, 1500, key="rider_price")
        
        filtered_rides = db.get_rides_by_filters(from_city, to_city, max_price=max_price)
        
        if len(filtered_rides) > 0:
            for ride in filtered_rides:
                card_class = get_vehicle_class(ride['ride_type'])
                st.markdown(f"""
                <div class="ride-card {card_class}">
                    <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;'>
                        <div style='flex: 1;'>
                            <h4 style='margin: 0 0 0.5rem 0; color: #1e293b; font-size: 1.25rem; font-weight: 700;'>
                                {ride['vehicle_icon']} {ride['ride_type']} • {ride['from_city']} → {ride['to_city']}
                            </h4>
                            <p style='color: #64748b; margin: 0;'>📅 {ride['date']} at {ride['time']} • 💺 {ride['seats']} seats</p>
                        </div>
                        <div style='display: flex; align-items: center; gap: 1rem;'>
                            <div class='price-tag'>₹{ride['price']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Book Now - {ride['driver_name']}", key=f"book_rider_{ride['id']}", type="primary"):
                    db.add_booking(ride['id'], st.session_state.current_user_id, st.session_state.current_user_name)
                    st.balloons()
                    st.markdown("""
                    <div class="success-message">
                        ✅ Ride Booked Successfully! Driver will contact you soon.
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No rides found. Try adjusting your filters or request a ride!")
    
    elif st.session_state.rider_active_tab == "request":
        st.markdown("<h3 style='color: #1e293b; margin-top: 2rem; margin-bottom: 1.5rem; font-weight: 700;'>Request a Custom Ride</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            from_city = st.selectbox("From City", INDIAN_CITIES)
            to_city = st.selectbox("To City", INDIAN_CITIES)
            passengers = st.number_input("Passengers", 1, 10, 1)
        with col2:
            date = st.date_input("Date", datetime.now())
            time = st.time_input("Time")
            budget = st.number_input("Your Budget (₹)", 50, 5000, 500)
        
        if st.button("Submit Request", type="primary"):
            db.add_ride_request(
                st.session_state.current_user_id,
                st.session_state.current_user_name,
                from_city,
                to_city,
                date.strftime("%d %B %Y"),
                time.strftime("%H:%M"),
                passengers,
                budget
            )
            st.balloons()
            st.markdown("""
            <div class="success-message">
                ✅ Your ride request has been submitted! Drivers will see your request soon.
            </div>
            """, unsafe_allow_html=True)
    
    else:  # Bookings
        st.markdown("<h3 style='color: #1e293b; margin-top: 2rem; margin-bottom: 1.5rem; font-weight: 700;'>My Bookings</h3>", unsafe_allow_html=True)
        bookings = db.get_user_bookings(st.session_state.current_user_id)
        if len(bookings) > 0:
            for booking in bookings:
                st.markdown(f"""
                <div class="ride-card">
                    <h4 style='margin: 0 0 0.5rem 0; color: #1e293b; font-weight: 700;'>
                        {booking['from_city']} → {booking['to_city']}
                    </h4>
                    <p style='color: #64748b; margin: 0.25rem 0;'>
                        <strong>Driver:</strong> {booking['driver_name']} • <strong>Date:</strong> {booking['ride_date']} • <strong>Time:</strong> {booking['ride_time']}
                    </p>
                    <p style='color: #64748b; margin: 0.25rem 0;'>
                        <strong>Price:</strong> ₹{booking['price']} • <strong>Passengers:</strong> {booking['passengers']} • <strong>Status:</strong> {booking['status']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("You haven't booked any rides yet!")


# --- Driver Dashboard ---
elif st.session_state.current_page == "driver_dashboard":
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;'>
        <h2 style='color: #1e293b; margin: 0; font-size: 2rem; font-weight: 700;'>
            🚗 Welcome {st.session_state.current_user_name}!
        </h2>
    """, unsafe_allow_html=True)
    if st.button("← Back to Home", key="driver_back"):
        st.session_state.current_page = "home"
        st.session_state.current_user_id = None
        st.session_state.current_user_name = None
        st.session_state.user_role = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Driver Navigation
    driver_tab1, driver_tab2, driver_tab3 = st.columns(3)
    with driver_tab1:
        if st.button("📋 Ride Requests", key="d_tab_requests", use_container_width=True, type="primary"):
            st.session_state.driver_active_tab = "requests"
    with driver_tab2:
        if st.button("🚘 Offer Ride", key="d_tab_offer", use_container_width=True):
            st.session_state.driver_active_tab = "offer"
    with driver_tab3:
        if st.button("📝 My Rides", key="d_tab_myrides", use_container_width=True):
            st.session_state.driver_active_tab = "myrides"
    
    if 'driver_active_tab' not in st.session_state:
        st.session_state.driver_active_tab = "requests"
    
    # Tab Content
    if st.session_state.driver_active_tab == "requests":
        st.markdown("<h3 style='color: #1e293b; margin-top: 2rem; margin-bottom: 1.5rem; font-weight: 700;'>Passenger Ride Requests</h3>", unsafe_allow_html=True)
        
        # Sample Requests
        col1, col2 = st.columns(2)
        with col1:
            from_city_filter = st.selectbox("From City", ["Any"] + INDIAN_CITIES, key="req_from")
        with col2:
            to_city_filter = st.selectbox("To City", ["Any"] + INDIAN_CITIES, key="req_to")
        
        requests = db.get_all_ride_requests()
        
        if len(requests) > 0:
            for req in requests:
                if (from_city_filter == "Any" or req['from_city'] == from_city_filter) and (to_city_filter == "Any" or req['to_city'] == to_city_filter):
                    st.markdown(f"""
                    <div class="ride-card">
                        <div style='display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 1rem;'>
                            <div>
                                <h4 style='margin: 0 0 0.5rem 0; color: #1e293b; font-weight: 700;'>
                                    👤 {req['rider_name']} • {req['from_city']} → {req['to_city']}
                                </h4>
                                <p style='color: #64748b; margin: 0;'>📅 {req['date']} at {req['time']} • {req['passengers']} Passengers</p>
                            </div>
                            <div style='display: flex; gap: 0.75rem;'>
                                <div class='price-tag'>₹{req['budget']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Accept Request - {req['rider_name']}", key=f"accept_req_{req['id']}", type="primary"):
                        st.balloons()
                        st.success("Request accepted! Passenger will be notified.")
        else:
            st.info("No ride requests yet!")
    
    elif st.session_state.driver_active_tab == "offer":
        st.markdown("<h3 style='color: #1e293b; margin-top: 2rem; margin-bottom: 1.5rem; font-weight: 700;'>Offer Your Ride</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            vehicle_type, vehicle_icon = st.selectbox("Vehicle Type", VEHICLE_TYPES, format_func=lambda x: f"{x[1]} {x[0]}")
            from_city = st.selectbox("From City", INDIAN_CITIES)
            to_city = st.selectbox("To City", INDIAN_CITIES)
            vehicle_number = st.text_input("Vehicle Number", placeholder="e.g., UP16AB1234")
        with col2:
            date = st.date_input("Date of Journey", datetime.now())
            time = st.time_input("Departure Time")
            seats = st.number_input("Seats Available", 1, 50, 3)
            price_per_seat = st.number_input("Price per Seat (₹)", 20, 5000, 200)
        
        if st.button("Publish Ride", type="primary", use_container_width=True):
            if vehicle_number:
                db.add_ride(
                    st.session_state.current_user_id,
                    st.session_state.current_user_name,
                    vehicle_type,
                    vehicle_icon,
                    from_city,
                    to_city,
                    date.strftime("%d %B %Y"),
                    time.strftime("%H:%M"),
                    seats,
                    price_per_seat,
                    vehicle_number
                )
                st.balloons()
                st.markdown("""
                <div class="success-message">
                    ✅ Your ride has been published successfully! Passengers can now book your ride.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Please enter vehicle number!")
    
    else:  # My Rides
        st.markdown("<h3 style='color: #1e293b; margin-top: 2rem; margin-bottom: 1.5rem; font-weight: 700;'>My Offered Rides</h3>", unsafe_allow_html=True)
        all_rides = db.get_all_rides()
        my_rides = [r for r in all_rides if r['driver_id'] == st.session_state.current_user_id]
        
        if len(my_rides) > 0:
            for ride in my_rides:
                card_class = get_vehicle_class(ride['ride_type'])
                st.markdown(f"""
                <div class="ride-card {card_class}">
                    <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;'>
                        <div style='flex: 1;'>
                            <h4 style='margin: 0 0 0.5rem 0; color: #1e293b; font-weight: 700;'>
                                {ride['vehicle_icon']} {ride['ride_type']} • {ride['from_city']} → {ride['to_city']}
                            </h4>
                            <p style='color: #64748b; margin: 0;'>📅 {ride['date']} • {ride['time']} • 💺 {ride['seats']} seats</p>
                        </div>
                        <div class='price-tag'>₹{ride['price']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("You haven't offered any rides yet!")


# Footer
st.markdown("""
<div style='text-align: center; padding: 3rem 2rem; margin-top: 4rem; background: #1e1b4b; color: white; border-radius: 2rem 2rem 0 0;'>
    <h3 style='margin-bottom: 1rem; font-size: 1.5rem;'>🚌 Margshree</h3>
    <p style='opacity: 0.8; margin-bottom: 0.5rem;'>India's Most Trusted Ride Sharing Platform</p>
    <p style='opacity: 0.6; font-size: 0.875rem;'>Made with ❤️ in India • © 2026 Margshree</p>
</div>
""", unsafe_allow_html=True)


