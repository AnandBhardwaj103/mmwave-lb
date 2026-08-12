import streamlit as st
import streamlit.components.v1 as components
import math

st.set_page_config(page_title="26 GHz Link Budget Tool", layout="wide")

st.title("📡 26 GHz Link Budget & Far-End RSSI Calculator")

# Input Configuration Section
with st.container():
    st.subheader("Hardware & Link Configuration")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        dist = st.number_input("Distance (meters)", value=3000, step=100)
        tx_pwr = st.number_input("Tx Power (dBm)", value=22.0, step=1.0)
        
    with col2:
        tx_gain = st.number_input("Tx Antenna Gain (dBi)", value=31.0, step=1.0)
        rx_gain = st.number_input("Rx Antenna Gain (dBi)", value=31.0, step=1.0)
        
    with col3:
        mcs_str = st.selectbox("MCS Index", ["MCS 9 (256-QAM)", "MCS 7 (64-QAM)"])
        mcs = 9 if "9" in mcs_str else 7
        region_str = st.selectbox("Region", ["Southern India", "Northern India"])
        region = "N" if "Northern" in region_str else "S"
        
    with col4:
        rain_pct = st.number_input("Rain Impact %", value=0, min_value=0, max_value=100, step=5)

# Calculations
freq = 26e9
pi = 22 / 7
c = 3e8

fspl = 20 * math.log10(dist) + 20 * math.log10(freq) + 20 * math.log10((4 * pi) / c)
eirp = tx_pwr + tx_gain
snr = 33 if mcs == 9 else 23
sens = -174 + 10 * math.log10(320e6) + 5.2 + snr
sens_with_margin = sens + 5

rates = [2.0, 6.9, 16.3] if region == "N" else [5.8, 15.5, 29.2]
avails = ["99.9%", "99.99%", "99.999%"]

table_rows = ""
for i in range(3):
    rain_loss = rates[i] * (rain_pct / 100.0) * (dist / 1000.0)
    mapl = fspl + rain_loss
    rssi = eirp + rx_gain - mapl
    margin = rssi - sens_with_margin
    ok = margin >= 0
    
    status_class = "ok" if ok else "bad"
    status_text = "OK" if ok else "BAD"

    table_rows += f"""<tr>
        <td>{avails[i]}</td>
        <td>{mapl:.2f}</td>
        <td><strong>{rssi:.2f}</strong></td>
        <td>{sens_with_margin:.2f}</td>
        <td>{margin:.2f}</td>
        <td class="{status_class}">{status_text}</td>
    </tr>"""

# Pure HTML/CSS rendered safely via components.html
html_component = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        margin: 0;
        padding: 0;
        background-color: transparent;
    }}
    .card {{
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        border: 1px solid #e1e4e8;
    }}
    .custom-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }}
    .custom-table th, .custom-table td {{
        padding: 12px;
        border: 1px solid #ddd;
        text-align: center;
        font-size: 14px;
    }}
    .custom-table th {{
        background-color: #007bff;
        color: white;
        font-weight: 600;
    }}
    .ok {{
        color: #28a745;
        font-weight: bold;
    }}
    .bad {{
        color: #dc3545;
        font-weight: bold;
    }}
</style>
</head>
<body>
<div class="card">
    <h3 style="margin-top:0; font-size: 18px; color: #333;">Far-End Receive Signal & Link Feasibility</h3>
    <table class="custom-table">
        <thead>
            <tr>
                <th>Availability</th>
                <th>Total Path Loss (dB)</th>
                <th>Far-End RSSI (dBm)</th>
                <th>Sensitivity w/ Margin (dBm)</th>
                <th>Link Margin (dB)</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</div>
</body>
</html>
"""

# Render HTML component directly
components.html(html_component, height=280, scrolling=False)
