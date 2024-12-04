import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate Example Data with Date and Time as Separate Columns
def generate_example_data():
    categories = ["Bandages", "Syringes", "Gloves", "Masks", "IV Fluids"]
    current_time = datetime.now()
    data = {
        "Category of Supply": np.random.choice(categories, 50),
        "Expiration Date": [current_time + timedelta(days=np.random.randint(30, 365)) for _ in range(50)],
        "Entry Date": [current_time.date() - timedelta(days=np.random.randint(0, 10)) for _ in range(50)],
        "Entry Time": [
            (current_time - timedelta(hours=np.random.randint(0, 3), minutes=np.random.randint(0, 60))).time()
            for _ in range(50)
        ],
        "Quantity": np.random.randint(10, 100, 50),
        "Pallet Number": np.random.randint(1, 20, 50),
        "Box number": np.random.randint(1, 50, 50),
    }
    return pd.DataFrame(data)

# Load or Create Data
df = generate_example_data()

# Save Data to Excel for Demo
df.to_excel("example_data.xlsx", index=False)

# Streamlit App
st.title("Medical Supply KPI Dashboard")

# Upload Excel File
uploaded_file = st.file_uploader("Upload Excel File", type="xlsx")
if uploaded_file:
    df = pd.read_excel(uploaded_file)

# Display DataFrame
st.dataframe(df)

# KPI: Supply Levels by Category
supply_levels = df.groupby("Category of Supply")["Quantity"].sum()
st.subheader("Supply Levels by Category")
st.bar_chart(supply_levels)

# KPI: Expiration Rates
expired_items = df[df["Expiration Date"] < datetime.now()]
expiration_rate = len(expired_items) / len(df) * 100
st.subheader("Expiration Rate")
st.metric("Expired Items", f"{len(expired_items)}", f"{expiration_rate:.2f}%")

# Combine Date and Time Columns to Calculate Average Inventory Event Time
df["Date of entry"] = pd.to_datetime(df["Entry Date"].astype(str) + " " + df["Entry Time"].astype(str))
df = df.sort_values(by="Date of entry")  # Ensure chronological order
inventory_event_times = df["Date of entry"].diff().dropna().dt.total_seconds() / 3600  # Convert to hours
average_event_time = inventory_event_times.mean()

st.subheader("Average Inventory Event Time")
st.metric("Average Time Between Entries", f"{average_event_time:.2f} hours")
