import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

import plotly.express as px
import plotly.graph_objects as go

# Function to get weather data from Weatherbit API
def get_weather_data(lat, lon):
    api_key = '762ee9f4f0ef4e7ebb8862f9b1427476'
    url = f"https://api.weatherbit.io/v2.0/forecast/agweather?key={api_key}&days=7&lat={lat}&lon={lon}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the API")
        return None


with st.sidebar:
    # User Inputs for Demand Multipliers
    with open("logo.svg", "r") as file:
        svg = file.read()

    # Display SVG
    st.sidebar.markdown(svg, unsafe_allow_html=True)
    st.title("Weather Studio")

lat = st.text_input("Enter Latitude")
lon = st.text_input("Enter Longitude")

if st.button("Get Agricultral Data", type="primary"):
    df = pd.DataFrame(get_weather_data(lat, lon)["data"])
    
    # Streamlit interface
    st.title('Agricultural Dashboard')
    st.write('This dashboard provides an overview of agricultural data important for farming decisions.')

    # Displaying data as a table
    st.subheader('Raw Data')
    st.write(df)

    # Plotting using Plotly
    st.subheader('Temperature and Soil Moisture Overview')

    # Temperature plot
    temp_fig = px.line(df, x='valid_date', y=['skin_temp_avg', 'temp_2m_avg'], labels={
                    'value': 'Temperature (C)', 'variable': 'Variable'}, title='Average Temperatures')
    st.plotly_chart(temp_fig)

    # Soil Moisture plot
    moisture_fig = px.line(df, x='valid_date', y=['soilm_0_10cm', 'soilm_10_40cm'], labels={
                        'value': 'Moisture (mm)', 'variable': 'Soil Depth'}, title='Soil Moisture by Depth')
    st.plotly_chart(moisture_fig)

    