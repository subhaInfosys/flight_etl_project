import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from datetime import date, timedelta

# Load environment variables
load_dotenv(override=True)

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
dbname = os.getenv('DB_NAME')
port = os.getenv('DB_PORT', '5432')

# Connect to database
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")
df = pd.read_sql("SELECT * FROM flights", engine)

st.title("✈️ Flight Delay Dashboard")

# Sidebar Filters
st.sidebar.header("🔎 Filters")

# Airline filter
airlines = st.sidebar.multiselect("Select Airline(s):", options=df['airline'].unique(), default=df['airline'].unique())

# Airport filter
departure_airports = st.sidebar.multiselect("Select Departure Airport(s):", options=df['departure_airport'].unique(), default=df['departure_airport'].unique())
arrival_airports = st.sidebar.multiselect("Select Arrival Airport(s):", options=df['arrival_airport'].unique(), default=df['arrival_airport'].unique())

# Date Range filter
today = date.today()
last_week = today - timedelta(days=7)
date_range = st.sidebar.date_input("Departure Date Range", [last_week, today])

# Apply filters
filtered_df = df.copy()
if airlines:
    filtered_df = filtered_df[filtered_df['airline'].isin(airlines)]

if departure_airports:
    filtered_df = filtered_df[filtered_df['departure_airport'].isin(departure_airports)]

if arrival_airports:
    filtered_df = filtered_df[filtered_df['arrival_airport'].isin(arrival_airports)]

if len(date_range) == 2 and all(date_range):
    filtered_df = filtered_df[
        (filtered_df['departure_time'].dt.date >= date_range[0]) &
        (filtered_df['departure_time'].dt.date <= date_range[1])
    ]

# Show filtered data
st.subheader("📊 Filtered Flight Data")
st.write(filtered_df.head())

# Plot 1: Status Distribution
st.subheader("📌 Flight Status Distribution")
fig1, ax1 = plt.subplots()
filtered_df['status'].value_counts().plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_ylabel("Number of Flights")
ax1.set_title("Status Count")
st.pyplot(fig1)

# Plot 2: Flights per Airline
st.subheader("✈️ Flights per Airline")
fig2, ax2 = plt.subplots()
filtered_df['airline'].value_counts().plot(kind='bar', ax=ax2, color='lightgreen')
ax2.set_ylabel("Number of Flights")
ax2.set_title("Flights per Airline")
st.pyplot(fig2)

# Plot 3: Top 10 Flight Routes
st.subheader("🛫 Top 10 Flight Routes")

# Create a route column (departure → arrival)
filtered_df['route'] = filtered_df['departure_airport'] + " → " + filtered_df['arrival_airport']

top_routes = filtered_df['route'].value_counts().nlargest(10)

fig3, ax3 = plt.subplots(figsize=(10, 6))
top_routes.plot(kind='barh', ax=ax3, color='coral')
ax3.invert_yaxis()
ax3.set_xlabel("Number of Flights")
ax3.set_title("Top 10 Flight Routes")
st.pyplot(fig3)