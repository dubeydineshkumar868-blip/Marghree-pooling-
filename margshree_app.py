import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Margshree - Desi Ride Sharing",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern, Professional UI
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Hide Streamlit Defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero Section */
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
    
    /* Search Container */
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 1.5rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        max-width: 1000px;
        margin: 0 auto;
    }
    
    /* Cards */
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
    
    /* Buttons */
    .btn-primary {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.875rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.5);
    }
    
    .btn-secondary {
        background: white;
        color: #4f46e5;
        border: 2px solid #4f46e5;
        border-radius: 0.75rem;
        padding: 0.875rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-secondary:hover {
        background: #f8fafc;
    }
    
    /* Price Tag */
    .price-tag {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1.25rem;
        border-radius: 0.5rem;
        font-weight: 700;
        font-size: 1.5rem;
        display: inline-block;
    }
    
    /* Labels */
    .label {
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    
    /* Info Text */
    .info-text {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.125rem;
    }
    
    /* Role Selection */
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
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    /* Navigation Tabs */
    .nav-tab {
        background: white;
        padding: 1rem 2rem;
        border-radius: 1rem;
        text-align: center;
        cursor: pointer;
        font-weight: 600;
        color: #64748b;
        transition: all 0.3s ease;
    }
    
    .nav-tab.active {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
    }
    
    /* Vehicle Icons */
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
    "Siliguri", "Guwahati", "Dibrugarh", "Jorhat"
]

# Vehicle Types
VEHICLE_TYPES = [
    ("Car", "🚗"),
    ("Bus", "🚌"),
    ("Battery Rickshaw", "🛺"),
    ("Bike", "🏍️"),
    ("SUV", "🚙")
]

# Initialize Session State
if 'rides' not in st.session_state:
    # Generate Sample Rides
    sample_rides = []
    cities = INDIAN_CITIES
    vehicle_info = VEHICLE_TYPES
    driver_names = ["Rajesh Kumar", "Suresh Singh", "Amit Sharma", "Priya Patel", 
                    "Rahul Verma", "Anita Gupta", "Vikram Singh", "Neha Reddy"]
    
    for i in range(12):
        ride_type, icon = random.choice(vehicle_info)
        from_city = random.choice(cities)
        to_city = random.choice([c for c in cities if c != from_city])
        date = datetime.now() + timedelta(days=random.randint(0, 7))
        time = f"{random.randint(6, 22):02d}:{random.choice(['00', '15', '30', '45'])}"
        
        if ride_type == "Car":
            seats = random.randint(3, 4)
            price = random.randint(300, 2500)
        elif ride_type == "Bus":
            seats = random.randint(10, 45)
            price = random.randint(100, 800)
        elif ride_type == "Battery Rickshaw":
            seats = random.randint(2, 3)
            price = random.randint(30, 300)
        elif ride_type == "Bike":
            seats = 1
            price = random.randint(50, 500)
        else:  # SUV
            seats = random.randint(5, 7)
            price = random.randint(500, 4000)
        
        sample_rides.append({
            "id": i + 1,
            "driver": driver_names[i % len(driver_names)],
            "ride_type": ride_type,
            "vehicle_icon": icon,
            "from": from_city,
            "to": to_city,
            "date": date.strftime("%d %B %Y"),
            "time": time,
            "seats": seats,
            "price": price,
            "rating": round(random.uniform(4.0, 5.0), 1),
            "vehicle_number": f"UP{random.randint(10, 99)}{random.choice(['ABC', 'XYZ', 'DEF', 'GHI'])}{random.randint(1000, 9999)}"
        })
    st.session_state.rides = pd.DataFrame(sample_rides)

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'user_role' not in st.session_state:
    st.session_state.user_role = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

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
        if st.button("Find Rides", key="find_rides_btn", use_container_width=True, type="primary"):
            st.session_state.current_page = "rider_dashboard"
            st.session_state.user_role = "rider"
            st.session_state.current_user = "Guest Rider"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">🚗</div>
            <h3 style="color: #1e293b; font-size: 1.5rem; margin-bottom: 0.5rem;">Offer a Ride</h3>
            <p style="color: #64748b; margin-bottom: 1.5rem;">Share your journey and earn money</p>
        """, unsafe_allow_html=True)
        if st.button("Offer a Ride", key="offer_ride_btn", use_container_width=True):
            st.session_state.current_page = "driver_dashboard"
            st.session_state.user_role = "driver"
            st.session_state.current_user = "Guest Driver"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display Search Results
    filtered_rides = st.session_state.rides.copy()
    if from_city != "Any City":
        filtered_rides = filtered_rides[filtered_rides["from"] == from_city]
    if to_city != "Any City":
        filtered_rides = filtered_rides[filtered_rides["to"] == to_city]
    if vehicle_filter != "All":
        filtered_rides = filtered_rides[filtered_rides["ride_type"] == vehicle_filter]
    
    st.markdown("<div style='margin-top: 3rem;'>", unsafe_allow_html=True)
    if len(filtered_rides) > 0:
        st.markdown(f"<h3 style='color: #1e293b; margin-bottom: 1.5rem; font-weight: 700;'>✨ {len(filtered_rides)} Rides Found</h3>", unsafe_allow_html=True)
        
        for idx, ride in filtered_rides.iterrows():
            card_class = get_vehicle_class(ride['ride_type'])
            st.markdown(f"""
            <div class="ride-card {card_class}">
                <div style='display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 1rem;'>
                    <div style='flex: 1; min-width: 250px;'>
                        <div style='display: flex; align-items: center; margin-bottom: 0.75rem;'>
                            <span class='vehicle-icon'>{ride['vehicle_icon']}</span>
                            <h3 style='margin: 0; color: #1e293b; font-size: 1.5rem; font-weight: 700;'>
                                {ride['ride_type']} • {ride['from']} → {ride['to']}
                            </h3>
                        </div>
                        <p style='color: #64748b; margin: 0.25rem 0;'>
                            <strong>Driver:</strong> {ride['driver']} • ⭐ {ride['rating']} • {ride['vehicle_number']}
                        </p>
                        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 1rem;'>
                            <div>
                                <div class='label'>Date</div>
                                <div class='info-text'>📅 {ride['date']}</div>
                            </div>
                            <div>
                                <div class='label'>Time</div>
                                <div class='info-text'>🕐 {ride['time']}</div>
                            </div>
                            <div>
                                <div class='label'>Seats Available</div>
                                <div class='info-text'>💺 {ride['seats']}</div>
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
    st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;'>
        <h2 style='color: #1e293b; margin: 0; font-size: 2rem; font-weight: 700;'>
            🧑‍💼 Rider Dashboard
        </h2>
    """, unsafe_allow_html=True)
    if st.button("← Back to Home", key="rider_back"):
        st.session_state.current_page = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Rider Navigation
    rider_tab1, rider_tab2, rider_tab3 = st.columns(3)
    with rider_tab1:
        if st.button("🔍 Search Rides", key="tab_search", use_container_width=True, type="primary"):
            st.session_state.rider_active_tab = "search"
            if 'rider_active_tab' not in st.session_state:
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
        
        filtered_rides = st.session_state.rides.copy()
        if from_city != "Any":
            filtered_rides = filtered_rides[filtered_rides["from"] == from_city]
        if to_city != "Any":
            filtered_rides = filtered_rides[filtered_rides["to"] == to_city]
        filtered_rides = filtered_rides[filtered_rides["price"] <= max_price]
        
        if len(filtered_rides) > 0:
            for idx, ride in filtered_rides.iterrows():
                card_class = get_vehicle_class(ride['ride_type'])
                st.markdown(f"""
                <div class="ride-card {card_class}">
                    <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;'>
                        <div style='flex: 1;'>
                            <h4 style='margin: 0 0 0.5rem 0; color: #1e293b; font-size: 1.25rem; font-weight: 700;'>
                                {ride['vehicle_icon']} {ride['ride_type']} • {ride['from']} → {ride['to']}
                            </h4>
                            <p style='color: #64748b; margin: 0;'>📅 {ride['date']} at {ride['time']} • 💺 {ride['seats']} seats</p>
                        </div>
                        <div style='display: flex; align-items: center; gap: 1rem;'>
                            <div class='price-tag'>₹{ride['price']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Book Now - {ride['driver']}", key=f"book_rider_{idx}", type="primary"):
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
            name = st.text_input("Your Name")
            from_city = st.selectbox("From City", INDIAN_CITIES)
            to_city = st.selectbox("To City", INDIAN_CITIES)
            passengers = st.number_input("Passengers", 1, 10, 1)
        with col2:
            date = st.date_input("Date", datetime.now())
            time = st.time_input("Time")
            budget = st.number_input("Your Budget (₹)", 50, 5000, 500)
        
        if st.button("Submit Request", type="primary"):
            if name:
                st.balloons()
                st.markdown("""
                <div class="success-message">
                    ✅ Your ride request has been submitted! Drivers will see your request soon.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Please enter your name!")
    
    else:  # Bookings
        st.markdown("<h3 style='color: #1e293b; margin-top: 2rem; margin-bottom: 1.5rem; font-weight: 700;'>My Bookings</h3>", unsafe_allow_html=True)
        st.info("Your booked rides will appear here. This is a demo version.")


# --- Driver Dashboard ---
elif st.session_state.current_page == "driver_dashboard":
    st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;'>
        <h2 style='color: #1e293b; margin: 0; font-size: 2rem; font-weight: 700;'>
            🚗 Driver Dashboard
        </h2>
    """, unsafe_allow_html=True)
    if st.button("← Back to Home", key="driver_back"):
        st.session_state.current_page = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Driver Navigation
    driver_tab1, driver_tab2, driver_tab3 = st.columns(3)
    with driver_tab1:
        if st.button("📋 Ride Requests", key="d_tab_requests", use_container_width=True, type="primary"):
            st.session_state.driver_active_tab = "requests"
            if 'driver_active_tab' not in st.session_state:
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
            from_city_filter = st.selectbox("From City", ["Any"] + INDIAN_CITIES)
        with col2:
            to_city_filter = st.selectbox("To City", ["Any"] + INDIAN_CITIES)
        
        st.markdown("""
        <div class="ride-card">
            <div style='display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 1rem;'>
                <div>
                    <h4 style='margin: 0 0 0.5rem 0; color: #1e293b; font-weight: 700;'>
                        👤 Arjun Mehta • Noida → Mainpuri
                    </h4>
                    <p style='color: #64748b; margin: 0;'>📅 Tomorrow at 08:30 AM • 2 Passengers</p>
                </div>
                <div style='display: flex; gap: 0.75rem;'>
                    <div class='price-tag'>₹800</div>
                </div>
            </div>
        </div>
        <div class="ride-card">
            <div style='display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap; gap: 1rem;'>
                <div>
                    <h4 style='margin: 0 0 0.5rem 0; color: #1e293b; font-weight: 700;'>
                        👤 Riya Kapoor • Delhi → Agra
                    </h4>
                    <p style='color: #64748b; margin: 0;'>📅 Day After at 10:00 AM • 1 Passenger</p>
                </div>
                <div style='display: flex; gap: 0.75rem;'>
                    <div class='price-tag'>₹450</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Accept Request - Arjun Mehta", type="primary"):
            st.balloons()
            st.success("Request accepted! Passenger will be notified.")
    
    elif st.session_state.driver_active_tab == "offer":
        st.markdown("<h3 style='color: #1e293b; margin-top: 2rem; margin-bottom: 1.5rem; font-weight: 700;'>Offer Your Ride</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            driver_name = st.text_input("Your Name")
            vehicle_type = st.selectbox("Vehicle Type", [vt[0] for vt in VEHICLE_TYPES])
            from_city = st.selectbox("From City", INDIAN_CITIES)
            to_city = st.selectbox("To City", INDIAN_CITIES)
            vehicle_number = st.text_input("Vehicle Number")
        with col2:
            date = st.date_input("Date of Journey", datetime.now())
            time = st.time_input("Departure Time")
            seats = st.number_input("Seats Available", 1, 50, 3)
            price_per_seat = st.number_input("Price per Seat (₹)", 20, 5000, 200)
        
        if st.button("Publish Ride", type="primary", use_container_width=True):
            if driver_name and vehicle_number:
                # Add new ride
                vehicle_icon = [vt[1] for vt in VEHICLE_TYPES if vt[0] == vehicle_type][0]
                new_ride = {
                    "id": len(st.session_state.rides) + 1,
                    "driver": driver_name,
                    "ride_type": vehicle_type,
                    "vehicle_icon": vehicle_icon,
                    "from": from_city,
                    "to": to_city,
                    "date": date.strftime("%d %B %Y"),
                    "time": time.strftime("%H:%M"),
                    "seats": seats,
                    "price": price_per_seat,
                    "rating": 5.0,
                    "vehicle_number": vehicle_number
                }
                st.session_state.rides = pd.concat([pd.DataFrame([new_ride]), st.session_state.rides], ignore_index=True)
                
                st.balloons()
                st.markdown("""
                <div class="success-message">
                    ✅ Your ride has been published successfully! Passengers can now book your ride.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Please fill in all required fields!")
    
    else:  # My Rides
        st.markdown("<h3 style='color: #1e293b; margin-top: 2rem; margin-bottom: 1.5rem; font-weight: 700;'>My Offered Rides</h3>", unsafe_allow_html=True)
        my_rides = st.session_state.rides.head(3)
        
        for idx, ride in my_rides.iterrows():
            card_class = get_vehicle_class(ride['ride_type'])
            st.markdown(f"""
            <div class="ride-card {card_class}">
                <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;'>
                    <div style='flex: 1;'>
                        <h4 style='margin: 0 0 0.5rem 0; color: #1e293b; font-weight: 700;'>
                            {ride['vehicle_icon']} {ride['ride_type']} • {ride['from']} → {ride['to']}
                        </h4>
                        <p style='color: #64748b; margin: 0;'>📅 {ride['date']} • {ride['time']} • 💺 {ride['seats']} seats</p>
                    </div>
                    <div class='price-tag'>₹{ride['price']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# Footer
st.markdown("""
<div style='text-align: center; padding: 3rem 2rem; margin-top: 4rem; background: #1e1b4b; color: white; border-radius: 2rem 2rem 0 0;'>
    <h3 style='margin-bottom: 1rem; font-size: 1.5rem;'>🚌 Margshree</h3>
    <p style='opacity: 0.8; margin-bottom: 0.5rem;'>India's Most Trusted Ride Sharing Platform</p>
    <p style='opacity: 0.6; font-size: 0.875rem;'>Made with ❤️ in India • © 2026 Margshree</p>
</div>
""", unsafe_allow_html=True)

