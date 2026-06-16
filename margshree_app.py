import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# Try to import Faker, if not available use fallback
try:
    from faker import Faker
    fake = Faker('en_IN')
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False

# Set page configuration
st.set_page_config(
    page_title="Margshree - Desi Ride Sharing",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fdf4ff 0%, #f0e7ff 50%, #ede9fe 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 50%, #2563eb 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(124, 58, 237, 0.4);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.4rem;
        opacity: 0.95;
        margin: 0;
        font-weight: 500;
    }
    
    .ride-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border-left: 6px solid #7c3aed;
        transition: all 0.3s ease;
    }
    
    .ride-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(124, 58, 237, 0.2);
    }
    
    .ride-type-car {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left-color: #3b82f6;
    }
    
    .ride-type-bus {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left-color: #10b981;
    }
    
    .ride-type-rickshaw {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left-color: #f59e0b;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
        color: white;
        border-radius: 50px;
        border: none;
        padding: 0.8rem 2.5rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(79, 70, 229, 0.4);
    }
    
    .sidebar [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%);
    }
    
    .sidebar-title {
        color: white;
        font-weight: 800;
        font-size: 1.8rem;
    }
    
    .price-tag {
        font-size: 1.8rem;
        font-weight: 900;
        color: #059669;
    }
    
    .footer {
        text-align: center;
        padding: 3rem;
        color: #64748b;
        margin-top: 3rem;
    }
    
    .role-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .role-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(124, 58, 237, 0.2);
    }
    
    .role-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Generate fake ride data
def generate_fake_rides():
    ride_types = ["Car", "Bus", "Battery Rickshaw"]
    cities = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Noida", "Mainpuri"]
    # Fallback driver names if Faker is not available
    driver_names = ["Rajesh Kumar", "Suresh Singh", "Amit Sharma", "Priya Patel", 
                    "Rahul Verma", "Anita Gupta", "Vikram Singh", "Neha Reddy"]
    
    rides = []
    for i in range(12):
        ride_type = random.choice(ride_types)
        from_city = random.choice(cities)
        to_city = random.choice([c for c in cities if c != from_city])
        date = datetime.now() + timedelta(days=random.randint(0, 7))
        time = f"{random.randint(6, 22):02d}:{random.choice(['00', '15', '30', '45'])}"
        
        if ride_type == "Car":
            seats = random.randint(3, 4)
            price = random.randint(300, 1500)
        elif ride_type == "Bus":
            seats = random.randint(10, 40)
            price = random.randint(100, 600)
        else:
            seats = random.randint(2, 3)
            price = random.randint(50, 200)
        
        # Get driver name
        if FAKER_AVAILABLE:
            driver_name = fake.name()
        else:
            driver_name = driver_names[i % len(driver_names)]
        
        rides.append({
            "driver": driver_name,
            "ride_type": ride_type,
            "from": from_city,
            "to": to_city,
            "date": date.strftime("%d %B %Y"),
            "time": time,
            "seats": seats,
            "price": price,
            "rating": round(random.uniform(4.0, 5.0), 1)
        })
    
    return pd.DataFrame(rides)

# Generate fake ride requests (for drivers)
def generate_fake_ride_requests():
    cities = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Noida", "Mainpuri"]
    # Fallback rider names if Faker is not available
    rider_names = ["Arjun Mehta", "Riya Kapoor", "Karan Joshi", "Ananya Iyer",
                   "Siddharth Rao", "Pooja Desai", "Rohit Nair", "Ishita Saxena"]
    
    requests = []
    for i in range(8):
        from_city = random.choice(cities)
        to_city = random.choice([c for c in cities if c != from_city])
        date = datetime.now() + timedelta(days=random.randint(0, 7))
        time = f"{random.randint(6, 22):02d}:{random.choice(['00', '15', '30', '45'])}"
        
        # Get rider name
        if FAKER_AVAILABLE:
            rider_name = fake.name()
        else:
            rider_name = rider_names[i % len(rider_names)]
        
        requests.append({
            "rider": rider_name,
            "from": from_city,
            "to": to_city,
            "date": date.strftime("%d %B %Y"),
            "time": time,
            "passengers": random.randint(1, 4),
            "budget": random.randint(100, 2000)
        })
    
    return pd.DataFrame(requests)

# Initialize session state
if 'rides' not in st.session_state:
    st.session_state.rides = generate_fake_rides()

if 'ride_requests' not in st.session_state:
    st.session_state.ride_requests = generate_fake_ride_requests()

if 'drivers' not in st.session_state:
    st.session_state.drivers = pd.DataFrame(columns=["name", "phone", "vehicle_type", "vehicle_number", "city"])

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# Main header
st.markdown("""
<div class="main-header">
    <h1>🚌 Margshree</h1>
    <p>Desi Ride Sharing - Cars, Buses & Battery Rickshaws</p>
</div>
""", unsafe_allow_html=True)

# Login/Signup page if no user is logged in
if st.session_state.current_user is None:
    st.markdown("## 👋 Welcome to Margshree!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="role-card" onclick="st.button('Rider')">
            <div class="role-icon">🧑‍💼</div>
            <h3 style="color: #1e1b4b;">Rider</h3>
            <p style="color: #64748b;">Book rides and travel safely</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Continue as Rider", key="rider_btn"):
            st.session_state.user_role = "Rider"
            st.session_state.current_user = "Guest Rider"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="role-card">
            <div class="role-icon">🚗</div>
            <h3 style="color: #1e1b4b;">Driver</h3>
            <p style="color: #64748b;">Offer rides and earn money</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Continue as Driver", key="driver_btn"):
            st.session_state.user_role = "Driver"
            st.rerun()

else:
    # Sidebar
    st.sidebar.markdown(f'<p class="sidebar-title">🚗 {st.session_state.user_role} Dashboard</p>', unsafe_allow_html=True)
    st.sidebar.write(f"Logged in as: **{st.session_state.current_user}**")
    
    if st.sidebar.button("Logout"):
        st.session_state.current_user = None
        st.session_state.user_role = None
        st.rerun()
    
    # Rider Interface
    if st.session_state.user_role == "Rider":
        rider_page = st.sidebar.radio(
            "Menu",
            ["Find Rides", "My Bookings", "Request a Ride"]
        )
        
        # Find Rides
        if rider_page == "Find Rides":
            st.markdown("## 🔍 Find Your Perfect Ride")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                ride_type_filter = st.selectbox("Vehicle Type", ["All", "Car", "Bus", "Battery Rickshaw"])
            with col2:
                from_city = st.selectbox("From City", ["Any", "Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Noida", "Mainpuri"])
            with col3:
                to_city = st.selectbox("To City", ["Any", "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Mainpuri", "Noida"])
            with col4:
                max_price = st.slider("Max Price (₹)", 50, 5000, 1000)
            
            filtered_rides = st.session_state.rides.copy()
            
            if ride_type_filter != "All":
                filtered_rides = filtered_rides[filtered_rides["ride_type"] == ride_type_filter]
            
            if from_city != "Any":
                filtered_rides = filtered_rides[filtered_rides["from"] == from_city]
            
            if to_city != "Any":
                filtered_rides = filtered_rides[filtered_rides["to"] == to_city]
            
            filtered_rides = filtered_rides[filtered_rides["price"] <= max_price]
            
            if len(filtered_rides) == 0:
                st.warning("⚠️ No rides found! Try adjusting your filters.")
            else:
                st.success(f"✅ Found {len(filtered_rides)} rides!")
                
                for idx, ride in filtered_rides.iterrows():
                    card_class = "ride-card"
                    if ride["ride_type"] == "Car":
                        card_class += " ride-type-car"
                    elif ride["ride_type"] == "Bus":
                        card_class += " ride-type-bus"
                    else:
                        card_class += " ride-type-rickshaw"
                    
                    st.markdown(f"""
                    <div class="{card_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                            <div>
                                <h3 style="margin: 0; color: #1e1b4b;">{ride['ride_type']} Ride</h3>
                                <p style="margin: 0.3rem 0; color: #475569;">by {ride['driver']} ⭐ {ride['rating']}</p>
                            </div>
                            <div class="price-tag">₹{ride['price']}</div>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1rem;">
                            <div>
                                <p style="margin: 0; font-weight: 600; color: #7c3aed;">From</p>
                                <p style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #1e1b4b;">{ride['from']}</p>
                            </div>
                            <div>
                                <p style="margin: 0; font-weight: 600; color: #7c3aed;">To</p>
                                <p style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #1e1b4b;">{ride['to']}</p>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                            <div>
                                <p style="margin: 0; font-weight: 600; color: #475569;">Date</p>
                                <p style="margin: 0; font-weight: 700; color: #1e1b4b;">{ride['date']}</p>
                            </div>
                            <div>
                                <p style="margin: 0; font-weight: 600; color: #475569;">Time</p>
                                <p style="margin: 0; font-weight: 700; color: #1e1b4b;">{ride['time']}</p>
                            </div>
                            <div>
                                <p style="margin: 0; font-weight: 600; color: #475569;">Seats</p>
                                <p style="margin: 0; font-weight: 700; color: #1e1b4b;">{ride['seats']} Available</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Book This {ride['ride_type']}", key=f"book_{idx}"):
                        st.balloons()
                        st.success(f"✅ You have successfully booked the {ride['ride_type']} ride with {ride['driver']}!")
        
        # Request a Ride
        elif rider_page == "Request a Ride":
            st.markdown("## 📋 Request a Custom Ride")
            
            col1, col2 = st.columns(2)
            with col1:
                rider_name = st.text_input("Your Name", value=st.session_state.current_user if st.session_state.current_user != "Guest Rider" else "")
                from_city = st.selectbox("From City", ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Noida", "Mainpuri"])
                to_city = st.selectbox("To City", ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Mainpuri", "Noida"])
            
            with col2:
                date = st.date_input("Date of Journey", datetime.now())
                time = st.time_input("Time of Journey")
                passengers = st.number_input("Number of Passengers", min_value=1, max_value=10, value=1)
                budget = st.number_input("Your Budget (₹)", min_value=50, max_value=5000, value=500)
            
            if st.button("Submit Ride Request"):
                if rider_name:
                    new_request = {
                        "rider": rider_name,
                        "from": from_city,
                        "to": to_city,
                        "date": date.strftime("%d %B %Y"),
                        "time": time.strftime("%H:%M"),
                        "passengers": passengers,
                        "budget": budget
                    }
                    st.session_state.ride_requests = pd.concat([pd.DataFrame([new_request]), st.session_state.ride_requests], ignore_index=True)
                    st.balloons()
                    st.success("✅ Your ride request has been submitted! Drivers will see your request soon.")
                else:
                    st.error("Please enter your name!")
        
        # My Bookings
        elif rider_page == "My Bookings":
            st.markdown("## 📝 My Bookings")
            st.info("Your booked rides will appear here! For now, this is a demo.")
    
    # Driver Interface
    elif st.session_state.user_role == "Driver":
        # Check if driver is registered
        if len(st.session_state.drivers) == 0 or st.session_state.current_user == "Guest Driver":
            st.markdown("## 🚗 Driver Registration")
            
            col1, col2 = st.columns(2)
            with col1:
                driver_name = st.text_input("Your Full Name")
                phone = st.text_input("Phone Number")
                vehicle_type = st.selectbox("Vehicle Type", ["Car", "Bus", "Battery Rickshaw"])
            
            with col2:
                vehicle_number = st.text_input("Vehicle Number")
                city = st.selectbox("Your City", ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Noida", "Mainpuri"])
            
            if st.button("Register as Driver"):
                if driver_name and phone and vehicle_number:
                    new_driver = {
                        "name": driver_name,
                        "phone": phone,
                        "vehicle_type": vehicle_type,
                        "vehicle_number": vehicle_number,
                        "city": city
                    }
                    st.session_state.drivers = pd.concat([pd.DataFrame([new_driver]), st.session_state.drivers], ignore_index=True)
                    st.session_state.current_user = driver_name
                    st.balloons()
                    st.success("✅ You have successfully registered as a driver!")
                    st.rerun()
                else:
                    st.error("Please fill all the fields!")
        
        else:
            driver_page = st.sidebar.radio(
                "Menu",
                ["Find Ride Requests", "Offer a Ride", "My Rides"]
            )
            
            # Find Ride Requests
            if driver_page == "Find Ride Requests":
                st.markdown("## 🔍 Find Ride Requests")
                
                col1, col2 = st.columns(2)
                with col1:
                    from_city_filter = st.selectbox("From City", ["Any", "Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Noida", "Mainpuri"])
                with col2:
                    to_city_filter = st.selectbox("To City", ["Any", "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Mainpuri", "Noida"])
                
                filtered_requests = st.session_state.ride_requests.copy()
                
                if from_city_filter != "Any":
                    filtered_requests = filtered_requests[filtered_requests["from"] == from_city_filter]
                
                if to_city_filter != "Any":
                    filtered_requests = filtered_requests[filtered_requests["to"] == to_city_filter]
                
                if len(filtered_requests) == 0:
                    st.warning("⚠️ No ride requests found!")
                else:
                    st.success(f"✅ Found {len(filtered_requests)} ride requests!")
                    
                    for idx, request in filtered_requests.iterrows():
                        st.markdown(f"""
                        <div class="ride-card">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                                <div>
                                    <h3 style="margin: 0; color: #1e1b4b;">Ride Request from {request['rider']}</h3>
                                </div>
                                <div class="price-tag">Budget: ₹{request['budget']}</div>
                            </div>
                            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1rem;">
                                <div>
                                    <p style="margin: 0; font-weight: 600; color: #7c3aed;">From</p>
                                    <p style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #1e1b4b;">{request['from']}</p>
                                </div>
                                <div>
                                    <p style="margin: 0; font-weight: 600; color: #7c3aed;">To</p>
                                    <p style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #1e1b4b;">{request['to']}</p>
                                </div>
                            </div>
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                                <div>
                                    <p style="margin: 0; font-weight: 600; color: #475569;">Date</p>
                                    <p style="margin: 0; font-weight: 700; color: #1e1b4b;">{request['date']}</p>
                                </div>
                                <div>
                                    <p style="margin: 0; font-weight: 600; color: #475569;">Time</p>
                                    <p style="margin: 0; font-weight: 700; color: #1e1b4b;">{request['time']}</p>
                                </div>
                                <div>
                                    <p style="margin: 0; font-weight: 600; color: #475569;">Passengers</p>
                                    <p style="margin: 0; font-weight: 700; color: #1e1b4b;">{request['passengers']}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"Accept Request from {request['rider']}", key=f"accept_{idx}"):
                            st.balloons()
                            st.success(f"✅ You have accepted the ride request from {request['rider']}!")
            
            # Offer a Ride
            elif driver_page == "Offer a Ride":
                st.markdown("## 🚘 Offer a Ride to Others")
                
                col1, col2 = st.columns(2)
                with col1:
                    ride_type = st.selectbox("Vehicle Type", ["Car", "Bus", "Battery Rickshaw"])
                    from_city = st.selectbox("From City", ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Noida", "Mainpuri"])
                    to_city = st.selectbox("To City", ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Mainpuri", "Noida"])
                
                with col2:
                    date = st.date_input("Date of Journey", datetime.now())
                    time = st.time_input("Time of Journey")
                    seats = st.number_input("Number of Seats Available", min_value=1, max_value=50, value=3)
                    price = st.number_input("Price per Seat (₹)", min_value=20, max_value=5000, value=200)
                
                if st.button("Publish Your Ride"):
                    new_ride = {
                        "driver": st.session_state.current_user,
                        "ride_type": ride_type,
                        "from": from_city,
                        "to": to_city,
                        "date": date.strftime("%d %B %Y"),
                        "time": time.strftime("%H:%M"),
                        "seats": seats,
                        "price": price,
                        "rating": 5.0
                    }
                    
                    st.session_state.rides = pd.concat([pd.DataFrame([new_ride]), st.session_state.rides], ignore_index=True)
                    st.balloons()
                    st.success(f"✅ Your {ride_type} ride has been published!")
            
            # My Rides
            elif driver_page == "My Rides":
                st.markdown("## 📝 My Offered Rides")
                my_rides = st.session_state.rides[st.session_state.rides["driver"] == st.session_state.current_user]
                
                if len(my_rides) == 0:
                    st.info("You haven't offered any rides yet!")
                else:
                    for idx, ride in my_rides.iterrows():
                        card_class = "ride-card"
                        if ride["ride_type"] == "Car":
                            card_class += " ride-type-car"
                        elif ride["ride_type"] == "Bus":
                            card_class += " ride-type-bus"
                        else:
                            card_class += " ride-type-rickshaw"
                        
                        st.markdown(f"""
                        <div class="{card_class}">
                            <h3 style="margin: 0 0 1rem 0; color: #1e1b4b;">{ride['ride_type']} - {ride['from']} → {ride['to']}</h3>
                            <p style="margin: 0.5rem 0;">📅 {ride['date']} at {ride['time']}</p>
                            <p style="margin: 0.5rem 0;">💺 {ride['seats']} seats available | 💰 ₹{ride['price']} per seat</p>
                        </div>
                        """, unsafe_allow_html=True)

# About page link (in sidebar if not logged in)
if st.session_state.current_user is None:
    if st.sidebar.button("About Margshree"):
        st.markdown("## 🌟 About Margshree")
        st.markdown("""
        <div style="background: white; padding: 3rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);">
            <h3 style="color: #7c3aed; font-size: 2rem;">Our Mission</h3>
            <p style="font-size: 1.2rem; color: #1e1b4b; line-height: 1.8;">
                Margshree is India's first ride-sharing platform that brings together <strong>Cars, Buses, and Battery Rickshaws</strong> all in one place!
            </p>
            
            <h3 style="color: #7c3aed; font-size: 1.8rem; margin-top: 2rem;">Why Choose Margshree?</h3>
            <ul style="font-size: 1.2rem; color: #1e1b4b; line-height: 2;">
                <li>🚗 <strong>Car Pooling</strong> - Comfortable rides for long distances</li>
                <li>🚌 <strong>Bus Sharing</strong> - Affordable rides for groups and daily commuters</li>
                <li>🛺 <strong>Battery Rickshaw</strong> - Eco-friendly last-mile connectivity</li>
                <li>💰 <strong>Affordable Prices</strong> - Save money while traveling</li>
                <li>🌱 <strong>Environment Friendly</strong> - Reduce carbon footprint</li>
                <li>👥 <strong>Community Focused</strong> - Connect with fellow travelers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Made with ❤️ in India | Margshree © 2026</p>
</div>
""", unsafe_allow_html=True)

