import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os
import time

# Dashboard Title
st.title("Real-Time Crypto Dashboard")

# Filter
crypto = st.selectbox(
    "Select Cryptocurrency",
    ["bitcoin", "ethereum", "dogecoin"]
)

# Fetch Live Data
url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    if crypto in data:
        price = float(data[crypto]["usd"])
    else:
        st.error("No data received from API.")
        st.write(data)
        st.stop()
else:
    st.error("Failed to fetch data from API.")
    st.stop()

# Extract Fields
timestamp = datetime.now()

# Display Data
st.metric(
    label=f"{crypto.capitalize()} Price",
    value=f"${price}"
)

st.write("Timestamp:", timestamp)

# Alert
threshold = st.number_input(
    "Enter Alert Price",
    min_value=0.0,
    value=70000.0
)

if price > threshold:
    st.success(
        f"Alert! {crypto.capitalize()} crossed ${threshold}"
    )

# Save Historical Data
filename = "crypto_data.csv"

new_row = pd.DataFrame({
    "Time": [timestamp],
    "Crypto": [crypto],
    "Price": [price]
})

if os.path.exists(filename):
    df = pd.read_csv(filename)
    df = pd.concat([df, new_row], ignore_index=True)
else:
    df = new_row

df.to_csv(filename, index=False)

# Filter Data
filtered_df = df[df["Crypto"] == crypto]

# Chart
st.subheader("Price Trend")

if len(filtered_df) > 1:
    st.line_chart(filtered_df["Price"])
else:
    st.write("Collecting data... Please wait for a few refreshes.")

# Recent Records
st.subheader("Recent Records")
st.dataframe(filtered_df.tail(10))

# Auto Refresh Every 60 Seconds
time.sleep(60)
st.rerun()