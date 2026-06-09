import streamlit as st
import requests 


st.title("Flight Delay Predictor")

# Input
month = st.number_input("Enter month ", min_value=1, max_value=12)

day_of_month = st.number_input("Enter day_of_month ", min_value=1, max_value=31)

day_of_week=st.number_input("Enter day_of_week ", min_value=1, max_value=7)


airports = [
    "ATL", "LAX", "ORD", "DFW", "DEN", "JFK", "SFO", "SEA", "LAS", "MCO",
    "EWR", "CLT", "PHX", "MIA", "IAH", "BOS", "MSP", "FLL", "DTW", "PHL"
]
airline = st.selectbox("Choose from below airlines ",["AA", "DL", "UA", "WN", "B6", "AS", "NK", "F9", "G4", "HA"])
origin = st.selectbox("Origin Airport", airports)
dest = st.selectbox("Destination Airport", airports)



dep_hour = st.number_input("Enter departure hour ", min_value=0, max_value=23)

crs_elapsed_time = st.number_input("Flight Duration (minutes)", min_value=30, max_value=800)
distance = st.number_input("Distance (miles)", min_value=50, max_value=5000)



if st.button('Predict'):
    payload={"month": int(month),
        "day_of_month": int(day_of_month),
        "day_of_week": int(day_of_week),
        "airline": airline,
        "origin": origin,
        "dest": dest,
        "dep_hour": int(dep_hour),
        "crs_elapsed_time": float(crs_elapsed_time),
        "distance": float(distance)
    }
    response=requests.post("http://localhost:8000/predict",json=payload)
    result=response.json()["prediction"]

    if "Delayed" in result:
            st.error(f"✈️ Flight is likely: {result}")
    else:
        st.success(f"✈️ Flight is likely: {result}")