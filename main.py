import streamlit as st

import pandas as pd

import matplotlib.pyplot as plt

import requests

from datetime import datetime


# Define the API endpoint and parameters
def get_weather_data(lat, lon):
    url = "https://www.meteosource.com/api/v1/free/point"
    params = {
        "lat": lat, #"28.4N"
        "lon": lon, #"70.2E"
        "sections": "current,daily",
        "timezone": "Asia/Karachi",
        "units": "metric"
    }

    # Define the headers, including the API key
    headers = {
        "x-api-key": "ipor2try9nkb5e3yvr6nqfpwnv61e1qpz4pzwfjg"
    }

    # Send the GET request to the API
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # print(data)
        return data
    else:
        print(f"Request failed with status code {response.status_code}")
        return None

locations = {
    "Athara": {"lat": "31.1N", "lon": "72.0E"},
    "Bhowana": {"lat": "31.5N", "lon": "72.6E"},
    "Chund Bharwana": {"lat": "31.4N", "lon": "72.2E"},
    "Garh Maharaja": {"lat": "30.8N", "lon": "71.9E"},
    "Lallian": {"lat": "31.8N", "lon": "72.7E"},
    "Hafizabad": {"lat": "32.0N", "lon": "73.6E"},
    "Toba Tek Singh": {"lat": "30.9N", "lon": "72.4E"}
}

# Add buttons for each location
with st.sidebar:
    # User Inputs for Demand Multipliers
    with open("logo.svg", "r") as file:
        svg = file.read()

    # Display SVG
    st.sidebar.markdown(svg, unsafe_allow_html=True)
    
    st.markdown("# Weather Studio")
    st.markdown("### Main Locations")
    selected_location = None
    for location in locations.keys():
        if st.button(location):
            selected_location = location


# Function to predict potential crop issues
def predict_crop_issues(weather_data):
    issues = []
    current = weather_data.get('current', {})
    print(current)
    temp = current.get('temperature', 0)
    humidity = 12
    # humidity = current["humidity"]  # Default to None if not found
    leaf_wetness_duration = current.get('leaf_wetness_duration', 0)
    conducive_days = current.get('conducive_days', 0)
    
    print(temp, humidity, leaf_wetness_duration, conducive_days)
    
    if temp is None or humidity is None:
        st.error("Temperature or humidity data is missing.")
        return issues
    
    # Brown Spot
    if 16 <= temp <= 36 and 85 <= humidity <= 100 and 10 <= leaf_wetness_duration <= 36 and conducive_days >= 3:
        issues.append("Brown Spot")
        
    # Sheath Rot
    if 20 <= temp <= 32 and 85 <= humidity <= 100 and conducive_days >= 3:
        issues.append("Sheath Rot")
        
    # Sheath Blight
    if 17 <= temp <= 36 and 85 <= humidity <= 100 and conducive_days >= 3:
        issues.append("Sheath Blight")
        
    # False Smut
    if 25 <= temp <= 35 and 90 <= humidity <= 100 and conducive_days >= 3:
        issues.append("False Smut")
        
    # Rice Blast
    if 19 <= temp <= 32 and 90 <= humidity <= 100 and 10 <= leaf_wetness_duration <= 36 and conducive_days >= 4:
        issues.append("Rice Blast")
        
    # Bacterial Leaf Blight
    if 21 <= temp <= 36 and 70 <= humidity <= 100 and conducive_days >= 3:
        issues.append("Bacterial Leaf Blight")
        
    # Bakanae
    if 20 <= temp <= 35 and 90 <= humidity <= 100 and conducive_days >= 3:
        issues.append("Bakanae")
        
    # Bacterial Panicle Blight
    if 25 <= temp <= 40 and 85 <= humidity <= 100 and conducive_days >= 3:
        issues.append("Bacterial Panicle Blight")
        
    return issues



# Initialize latitude and longitude fields
lat = st.text_input("Enter Latitude", locations[selected_location]["lat"] if selected_location else "28.4N")
lon = st.text_input("Enter Longitude", locations[selected_location]["lon"] if selected_location else "70.2E")


# Button to fetch data
if st.button("Get Weather Data"):
    
    weather_data = get_weather_data(lat, lon)
    issues = predict_crop_issues(weather_data)
    
    # Predict crop issues

    # Show predicted issues
    st.header("Predicted Crop Issues")
    if issues:
        for issue in issues:
            st.write(issue)
    else:
        st.write("No issues predicted based on current weather data.")
    
    if weather_data:
        # Display current weather
        st.header("Current Weather")
        current = weather_data.get('current', {})
        st.write(f"Summary: {current.get('summary', 'N/A')}")
        st.write(f"Temperature: {current.get('temperature', 'N/A')} °C")
        wind = current.get('wind', {})
        st.write(f"Wind: {wind.get('speed', 'N/A')} km/h, {wind.get('dir', 'N/A')}")
        st.write(f"Cloud Cover: {current.get('cloud_cover', 'N/A')}%")
        precipitation = current.get('precipitation', {})
        st.write(f"Precipitation: {precipitation.get('total', 'N/A')} mm")

        # Prepare daily data for visualization
        daily_data = weather_data.get('daily', {}).get('data', [])
        df_daily = pd.DataFrame(daily_data)

        # Extract all_day information for easier access
        if not df_daily.empty:
            df_daily = df_daily.join(pd.json_normalize(df_daily.pop('all_day')), rsuffix='_all_day')

            # Convert 'day' to datetime and format
            df_daily['day'] = pd.to_datetime(df_daily['day'])
            df_daily['formatted_day'] = df_daily['day'].dt.strftime('%a, %d %b')

            # Display daily weather data
            st.header("Daily Weather Forecast")
            st.dataframe(df_daily[['formatted_day', 'summary', 'temperature', 'temperature_min', 'temperature_max', 'wind.speed', 'wind.dir', 'cloud_cover.total', 'precipitation.total']])

            # Plot temperature trend
            st.subheader("Daily Temperature Trend")
            plt.figure(figsize=(10, 5))
            plt.plot(df_daily['formatted_day'], df_daily['temperature_max'], marker='o', label='Max Temperature')
            plt.plot(df_daily['formatted_day'], df_daily['temperature_min'], marker='o', label='Min Temperature')
            plt.title("Daily Temperature")
            plt.xlabel("Date")
            plt.ylabel("Temperature (°C)")
            plt.legend()
            plt.grid(True)
            st.pyplot(plt)

            # Plot cloud cover trend
            st.subheader("Daily Cloud Cover Trend")
            plt.figure(figsize=(10, 5))
            plt.plot(df_daily['formatted_day'], df_daily['cloud_cover.total'], marker='o', color='orange')
            plt.title("Daily Cloud Cover")
            plt.xlabel("Date")
            plt.ylabel("Cloud Cover (%)")
            plt.grid(True)
            st.pyplot(plt)

            # Plot wind speed trend
            st.subheader("Daily Wind Speed Trend")
            plt.figure(figsize=(10, 5))
            plt.plot(df_daily['formatted_day'], df_daily['wind.speed'], marker='o', color='green')
            plt.title("Daily Wind Speed")
            plt.xlabel("Date")
            plt.ylabel("Wind Speed (km/h)")
            plt.grid(True)
            st.pyplot(plt)

            # Plot precipitation trend
            st.subheader("Daily Precipitation Trend")
            plt.figure(figsize=(10, 5))
            plt.plot(df_daily['formatted_day'], df_daily['precipitation.total'], marker='o', color='blue')
            plt.title("Daily Precipitation")
            plt.xlabel("Date")
            plt.ylabel("Precipitation (mm)")
            plt.grid(True)
            st.pyplot(plt)