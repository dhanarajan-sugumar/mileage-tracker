import streamlit as st
import pandas as pd
from mileage_service import save_log, fetch_log

# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Hyryder Mileage Tracker", page_icon="🚘")
st.title("🚘 Toyota Hyryder Mileage Tracker")
# ──────────────────────────────────────────────────────────────

with st.form("mileage", clear_on_submit=True):
    col1, col2 = st.columns(2)
    odo_start = col1.number_input(
        "Start Odometer (km)", min_value=0.0, value=0.0, step=1.0
    )
    odo_end = col2.number_input(
        "End Odometer (km)", min_value=0.0, value=0.0, step=1.0
    )

    col3, col4 = st.columns(2)
    litres = col3.number_input(
        "Fuel Filled (L)", min_value=0.0, value=0.0, step=0.1
    )
    price = col4.number_input(
        "Price per Litre (₹)", min_value=0.0, value=0.0, step=0.1
    )

    submitted = st.form_submit_button("Compute & Save")

# ── validation + business logic ───────────────────────────────
if submitted:
    errors = []

    # rule‑set
    if odo_end <= odo_start:
        errors.append("End odometer must be **greater** than start odometer.")
    if litres <= 0:
        errors.append("Fuel filled (L) must be **greater than 0**.")
    if price <= 0:
        errors.append("Price per litre must be **greater than 0**.")

    if errors:
        for e in errors:
            st.error(e)
        st.stop()  # halt execution; nothing saved
    else:
        # all good – persist entry
        dist, mil, tot_cost, cost_km = save_log(
            odo_start, odo_end, litres, price
        )
        st.success(f"Distance : **{dist} km**")
        st.success(f"Mileage  : **{mil} km/L**")
        st.success(f"₹ per km : **₹{cost_km}**")

# ── historical log (read‑only) ────────────────────────────────
records = fetch_log()
if records:
    df = pd.DataFrame([dict(r) for r in records]).rename(
        columns={
            "id": "ID",
            "ts": "Timestamp",
            "odo_start": "Start",
            "odo_end": "End",
            "litres": "Litres",
            "distance": "Distance",
            "mileage": "km/L",
            "cost_per_litre": "₹/L",
            "total_cost": "Total ₹",
            "cost_per_km": "₹/km",
        }
    )
    st.subheader("📊 Mileage Log")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No records yet. Add one via the form above.")
