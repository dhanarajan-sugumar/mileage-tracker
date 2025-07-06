import pandas as pd
import streamlit as st
from mileage_service import save_log, fetch_log

st.set_page_config(page_title="Hyryder Mileage Tracker", page_icon="🚘")
st.title("🚘 Toyota Hyryder Mileage Tracker")

with st.form("mileage"):
    col1, col2 = st.columns(2)
    odo_start = col1.number_input("Start Odometer (km)", min_value=0.0, value=7322.0, step=1.0)
    odo_end   = col2.number_input("End Odometer (km)",   min_value=0.0, value=8006.0, step=1.0)

    col3, col4 = st.columns(2)
    litres = col3.number_input("Fuel Filled (L)", min_value=0.1, value=35.0, step=0.1)
    price  = col4.number_input("Price per Litre (₹)", min_value=0.1, value=101.0, step=0.1)

    submitted = st.form_submit_button("Compute & Save")

if submitted:
    dist, mil, tot_cost, cost_km = save_log(odo_start, odo_end, litres, price)
    st.success(f"Distance: **{dist} km**")
    st.success(f"Mileage: **{mil} km/L**")
    st.success(f"₹ per km: **₹{cost_km}**")

# ―― Historical dashboard ―――――――――――――――――――――――――――――――――
records = fetch_log()
if records:
    df = pd.DataFrame(records)
    df = df.rename(columns={
        "ts": "Timestamp", "odo_start": "Start", "odo_end": "End",
        "litres": "Litres", "distance": "Distance",
        "mileage": "Mileage (km/L)", "cost_per_litre": "₹/L",
        "total_cost": "Total ₹", "cost_per_km": "₹ per km",
    })
    st.subheader("📊 Mileage Log")
    st.dataframe(df)
else:
    st.info("No records yet. Add one via the form above.")
