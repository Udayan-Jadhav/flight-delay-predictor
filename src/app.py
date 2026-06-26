import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Wheels Up", page_icon="✈️", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #0a1628 0%, #050a14 100%);
    }
    .hero {
        text-align: center;
        padding: 3rem 1rem 2rem 1rem;
    }
    .hero-title {
        font-size: 6rem !important;;
        font-weight: 900;
        color: #ffffff;
        margin: 0;
        letter-spacing: -2px;
        line-height: 1;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #6b8cae;
        margin-top: 0.6rem;
    }
    div[data-testid="stForm"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        height: 3.2rem;
        font-weight: 700;
        font-size: 1.1rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5253 100%);
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ee5253 0%, #d63838 100%);
    }
    .result-card {
        text-align: center;
        padding: 2.5rem;
        border-radius: 20px;
        margin-top: 1.5rem;
    }
    .result-delayed {
        background: rgba(255,107,107,0.12);
        border: 1px solid rgba(255,107,107,0.3);
    }
    .result-ontime {
        background: rgba(46,213,115,0.12);
        border: 1px solid rgba(46,213,115,0.3);
    }
    .result-emoji { font-size: 3rem; }
    .result-text { font-size: 1.6rem; font-weight: 700; color: white; margin-top: 0.5rem; }
    .result-route { color: #888; margin-top: 0.3rem; }
    footer, [data-testid="stToolbar"] { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- Hero ---
st.markdown("""
    <div class="hero">
        <p class="hero-title">✈️ Wheels Up</p>
        <p class="hero-subtitle">Will your flight be on time?</p>
    </div>
""", unsafe_allow_html=True)

AIRPORTS = [
    "ATL", "LAX", "ORD", "DFW", "DEN", "JFK", "SFO", "SEA", "LAS", "MCO",
    "EWR", "CLT", "PHX", "MIA", "IAH", "BOS", "MSP", "FLL", "DTW", "PHL"
]
AIRLINES = {
    "AA": "American Airlines", "DL": "Delta", "UA": "United",
    "WN": "Southwest", "B6": "JetBlue", "AS": "Alaska",
    "NK": "Spirit", "F9": "Frontier", "G4": "Allegiant", "HA": "Hawaiian"
}

with st.form("flight_form"):
    flight_date = st.date_input("Date", datetime.today())

    col1, col2 = st.columns(2)
    with col1:
        airline_label = st.selectbox("Airline", list(AIRLINES.values()))
    with col2:
        dep_hour = st.slider("Departure hour", 0, 23, 12)

    col3, col4 = st.columns(2)
    with col3:
        origin = st.selectbox("From", AIRPORTS, index=AIRPORTS.index("JFK"))
    with col4:
        dest = st.selectbox("To", [a for a in AIRPORTS if a != origin])

    col5, col6 = st.columns(2)
    with col5:
        crs_elapsed_time = st.number_input("Duration (min)", min_value=30, max_value=800, value=180)
    with col6:
        distance = st.number_input("Distance (mi)", min_value=50, max_value=5000, value=1000)

    submitted = st.form_submit_button("Predict")

if submitted:
    airline = [k for k, v in AIRLINES.items() if v == airline_label][0]
    payload = {
        "month": flight_date.month,
        "day_of_month": flight_date.day,
        "day_of_week": flight_date.isoweekday(),
        "airline": airline,
        "origin": origin,
        "dest": dest,
        "dep_hour": int(dep_hour),
        "crs_elapsed_time": float(crs_elapsed_time),
        "distance": float(distance)
    }

    with st.spinner("Checking flight history..."):
        try:
            response = requests.post(
                "https://wheels-up-api.onrender.com/predict",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()["prediction"]
        except Exception as e:
            st.error(f"Couldn't reach the prediction service: {e}")
            st.stop()

    is_delayed = "Delayed" in result
    card_class = "result-delayed" if is_delayed else "result-ontime"
    emoji = "🔴" if is_delayed else "🟢"
    text = "Likely Delayed" if is_delayed else "Likely On Time"

    st.markdown(f"""
        <div class="result-card {card_class}">
            <div class="result-emoji">{emoji}</div>
            <div class="result-text">{text}</div>
            <div class="result-route">{airline_label} · {origin} → {dest} · {flight_date.strftime('%b %d, %Y')}</div>
        </div>
    """, unsafe_allow_html=True)