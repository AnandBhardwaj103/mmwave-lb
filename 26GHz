import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="26 GHz Link Budget Tool", layout="wide")

st.title("📡 26 GHz mmWave Wi-Fi Link Budget & RSSI Tool")

st.sidebar.header("🔧 Link Parameters")
model_type = st.sidebar.radio("Select Model", ["Standard 802.11ax Model", "Nokia EIRP Model"])

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌐 Distance & Rain")
    distance_m = st.number_input("Distance (meters)", min_value=100, max_value=50000, value=3000, step=100)
    region = st.selectbox("Region", ["Southern India (S)", "Northern India (N)"])
    rain_impact_pct = st.slider("Rain Impact (% of Link)", 0, 100, 0, step=10)

with col2:
    st.subheader("📻 Transceiver & Antennas")
    bandwidth_mhz = st.selectbox("Bandwidth (MHz)", [320, 160])
    mcs = st.selectbox("MCS Index", [9, 7])
    tx_conducted_dbm = st.number_input("Tx Conducted Power (dBm)", value=22)
    tx_gain_dbi = st.number_input("Tx Antenna Gain (dBi)", value=31)
    rx_gain_dbi = st.number_input("Rx Antenna Gain (dBi)", value=31)
    tx_loss_db = st.number_input("Tx Cable/Chain Loss (dB)", value=0)
    rx_loss_db = st.number_input("Rx Cable/Chain Loss (dB)", value=0)

with col3:
    st.subheader("📊 System Margins & Traffic")
    dl_duty_pct = st.slider("Downlink Duty Cycle (%)", 0, 100, 70)
    noise_figure_db = st.number_input("Noise Figure (dB)", value=5.2)

# Calculations
frequency_hz = 26e9
pi_approx = 22 / 7
c = 3e8

if model_type == "Standard 802.11ax Model":
    path_loss = 20*math.log10(distance_m) + 20*math.log10(frequency_hz) + 20*math.log10((4*pi_approx)/c)
    snr_req = 33 if mcs == 9 else 23
    bits_per_carrier = 8 if mcs == 9 else 6
    subcarriers = 3920 if bandwidth_mhz == 320 else 1960
    phy_100 = (subcarriers * bits_per_carrier * 2 * (5/6)) / 13.6
    sens_margin = 5
    eirp = tx_conducted_dbm + tx_gain_dbi - tx_loss_db
else:
    path_loss = 10*2.1*math.log10(distance_m) + 20*math.log10(frequency_hz) + 6 + 20*math.log10((4*pi_approx)/c)
    snr_req = 25 if mcs == 7 else 33
    phy_100 = 2017.4 if bandwidth_mhz == 320 else 1008.7
    sens_margin = 3
    eirp = tx_conducted_dbm + tx_gain_dbi - tx_loss_db

sensitivity = -174 + 10*math.log10(bandwidth_mhz * 1e6) + noise_figure_db + snr_req
sens_with_margin = sensitivity + sens_margin

reg_code = 'N' if "Northern" in region else 'S'
rain_rates = {99.9: 2.0, 99.99: 6.9, 99.999: 16.3} if reg_code == 'N' else {99.9: 5.8, 99.99: 15.5, 99.999: 29.2}

results = []
for avail, rate in rain_rates.items():
    r_loss = rate * (rain_impact_pct / 100.0) * (distance_m / 1000.0)
    mapl = path_loss + r_loss
    rssi = eirp + rx_gain_dbi - rx_loss_db - mapl
    margin = rssi - sens_with_margin
    status = "✅ OK" if margin >= 0 else "❌ BAD"
    
    results.append({
        "Availability (%)": f"{avail}%",
        "Total Path Loss (dB)": round(mapl, 2),
        "Far-End RSSI (dBm)": round(rssi, 2),
        "Link Margin (dB)": round(margin, 2),
        "Status": status
    })

st.divider()

res_col1, res_col2 = st.columns([2, 1])

with res_col1:
    st.subheader("📋 Far-End Signal & Availability Matrix")
    st.table(pd.DataFrame(results))

with res_col2:
    st.subheader("🚀 Receiver & Throughput Stats")
    dl_phy = (dl_duty_pct / 100.0) * phy_100
    ul_phy = ((100 - dl_duty_pct) / 100.0) * phy_100
    st.metric("Far-End Clear-Sky RSSI", f"{round(eirp + rx_gain_dbi - rx_loss_db - path_loss, 2)} dBm")
    st.metric("Receiver Sensitivity (w/ Margin)", f"{round(sens_with_margin, 2)} dBm")
    st.metric("DL Practical Throughput", f"{round(dl_phy * 0.75, 1)} Mbps")
    st.metric("UL Practical Throughput", f"{round(ul_phy * 0.75, 1)} Mbps")
