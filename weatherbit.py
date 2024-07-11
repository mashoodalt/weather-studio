import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

import plotly.express as px
import plotly.graph_objects as go

# Function to get weather data from Weatherbit API
def get_weather_data(lat, lon):
    api_key = '762ee9f4f0ef4e7ebb8862f9b1427476'
    url = f"https://api.weatherbit.io/v2.0/forecast/daily?key={api_key}&days=7&lat={lat}&lon={lon}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the API")
        return None

# Function to predict potential crop issues
def predict_crop_issues(weather_data):
    issues = []
    for day in weather_data['data']:
        temp = day['temp']
        humidity = day['rh']
        cloud_cover = day['clouds']
        leaf_wetness_duration = day.get('leaf_wetness_duration', 0)
        conducive_days = day.get('conducive_days', 0)
        
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

# Streamlit application
# st.title("Rice Crop Disease Prediction")

# Mapping of locations to their latitude and longitude

# Function to check if conditions are conducive for diseases
def check_disease_conditions(row, diseases):
    conditions = []
    for disease in diseases:
        cond = diseases[disease]
        if (cond['min_temp'] <= row['temp'] <= cond['max_temp'] and
            cond['min_humidity'] <= row['rh'] <= cond['max_humidity']):
            conditions.append(disease)
    return conditions

# Disease conducive parameters
diseases = {
    'Brown Spot': {'min_temp': 16, 'max_temp': 36, 'min_humidity': 85, 'max_humidity': 100},
    'Sheath Rot': {'min_temp': 20, 'max_temp': 32, 'min_humidity': 85, 'max_humidity': 100},
    'Sheath Blight': {'min_temp': 17, 'max_temp': 36, 'min_humidity': 85, 'max_humidity': 100},
    'False Smut': {'min_temp': 25, 'max_temp': 35, 'min_humidity': 90, 'max_humidity': 100},
    'Rice Blast': {'min_temp': 19, 'max_temp': 32, 'min_humidity': 90, 'max_humidity': 100},
    'Bacterial Leaf Blight': {'min_temp': 21, 'max_temp': 36, 'min_humidity': 70, 'max_humidity': 100},
    'Bakanae': {'min_temp': 20, 'max_temp': 35, 'min_humidity': 90, 'max_humidity': 100},
    'Bacterial Panicle Blight': {'min_temp': 25, 'max_temp': 40, 'min_humidity': 85, 'max_humidity': 100}
}

disease_df = df = pd.DataFrame(diseases).T



locations = {
    "Athara": {"lat": "31.1", "lon": "72.0"},
    "Bhowana": {"lat": "31.5", "lon": "72.6"},
    "Chund Bharwana": {"lat": "31.4", "lon": "72.2"},
    "Garh Maharaja": {"lat": "30.8", "lon": "71.9"},
    "Lallian": {"lat": "31.8", "lon": "72.7"},
    "Hafizabad": {"lat": "32.0", "lon": "73.6"},
    "Toba Tek Singh": {"lat": "30.9", "lon": "72.4"}
}

# Add buttons for each location
with st.sidebar:
    # User Inputs for Demand Multipliers
    with open("logo.svg", "r") as file:
        svg = file.read()

    # Display SVG
    st.sidebar.markdown(svg, unsafe_allow_html=True)
    st.title("Weather Studio")
    # st.markdown("# Weather Studio")
    st.markdown("### Main Locations")

    if 'selected_location' not in st.session_state:
        st.session_state['selected_location'] = None

    # st.session_state.selected_location = None
    
    for location in locations.keys():
        if st.button(location, help=f'{locations[location]["lat"]}N - {locations[location]["lon"]}E'):
            st.session_state['selected_location'] = location

    # st.write(f'{st.session_state.selected_location}')


# Initialize latitude and longitude fields
lat = st.text_input("Enter Latitude", locations[st.session_state['selected_location']]["lat"] if st.session_state['selected_location'] else "31.5")
lon = st.text_input("Enter Longitude", locations[st.session_state['selected_location']]["lon"] if st.session_state['selected_location'] else "72.6")
crop = st.selectbox('Select Crop', ["Rice"], 0, disabled=True)

# Button to fetch data
if st.button("Get Weather Data", type="primary"):
    weather_data = get_weather_data(lat, lon)
    # '''
    # if weather_data:
    #     # Display weather data
    #     # st.header("Weather Forecast Data")
    #     # Display the city name
    #     city_name = weather_data.get('city_name', 'Unknown City')
    #     st.header(f"Weather Forecast for {city_name}")
    #     # Extract relevant data
    #     df = pd.DataFrame(weather_data['data'])
    
    #     # Convert date to datetime format
    #     df['datetime'] = pd.to_datetime(df['valid_date'])

    #     # Plot the data
    #     fig = px.line(df, x='datetime', y=['temp', 'rh', 'precip', 'wind_spd'], 
    #                 labels={'value': 'Values', 'variable': 'Metrics'},
    #                 title='7-Day Weather Forecast')
    #     fig.update_layout(
    #         xaxis_title='Date',
    #         yaxis_title='Values',
    #         legend_title_text='Metrics'
    #     )
        
    #     # Show the plot in Streamlit
    #     st.plotly_chart(fig)
    # '''
    # if weather_data:
    #     # Display the city name
    #     city_name = weather_data.get('city_name', 'Unknown City')
    #     st.header(f"Weather Forecast for {city_name}")

    #     # Extract relevant data
    #     df = pd.DataFrame(weather_data['data'])
        
    #     # Convert date to datetime format
    #     df['datetime'] = pd.to_datetime(df['valid_date'])

    #     # Check disease conditions
    #     df['conditions'] = df.apply(lambda row: check_disease_conditions(row, diseases), axis=1)
        
    #     # Plot the data
    #     fig = go.Figure()

    #     fig.add_trace(go.Scatter(x=df['datetime'], y=df['temp'], mode='lines+markers', name='Temperature (°C)'))
    #     fig.add_trace(go.Scatter(x=df['datetime'], y=df['rh'], mode='lines+markers', name='Humidity (%)'))
    #     fig.add_trace(go.Scatter(x=df['datetime'], y=df['precip'], mode='lines+markers', name='Precipitation (mm)'))
    #     fig.add_trace(go.Scatter(x=df['datetime'], y=df['wind_spd'], mode='lines+markers', name='Wind Speed (m/s)'))
        
    #     # Highlight danger areas
    #     for disease in diseases.keys():
    #         mask = df['conditions'].apply(lambda x: disease in x)
    #         fig.add_trace(go.Scatter(x=df['datetime'][mask], y=df['temp'][mask], mode='markers', 
    #                                 name=f'{disease} Risk', 
    #                                 marker=dict(size=12, color=px.colors.qualitative.Set1[diseases.keys().index(disease)])))

    #     fig.update_layout(
    #         title='7-Day Weather Forecast with Disease Risk Areas',
    #         xaxis_title='Date',
    #         yaxis_title='Values',
    #         legend_title_text='Metrics and Disease Risks'
    #     )

    #     # Show the plot in Streamlit
    #     st.plotly_chart(fig)
        
    if weather_data:
        # Display the city name
        city_name = weather_data.get('city_name', 'Unknown City')
        st.header(f"Weather Forecast for {city_name}")

        # Extract relevant data
        df = pd.DataFrame(weather_data['data'])
        
        # Convert date to datetime format
        df['datetime'] = pd.to_datetime(df['valid_date'])

        # Check disease conditions
        df['conditions'] = df.apply(lambda row: check_disease_conditions(row, diseases), axis=1)
        
        # st.write(df['conditions'])
        
        # Plot the data
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=df['datetime'], y=df['temp'], mode='lines+markers', name='Temperature (°C)'))
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['rh'], mode='lines+markers', name='Humidity (%)'))
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['precip'], mode='lines+markers', name='Precipitation (mm)'))
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['wind_spd'], mode='lines+markers', name='Wind Speed (m/s)'))
        
        # Highlight danger areas
        disease_list = list(diseases.keys())
        for disease in disease_list:
            mask = df['conditions'].apply(lambda x: disease in x)
            fig.add_trace(go.Scatter(x=df['datetime'][mask], y=df['temp'][mask], mode='markers', 
                                    name=f'{disease} Risk', 
                                    marker=dict(size=12, color=px.colors.qualitative.Set1[disease_list.index(disease)])))

        fig.update_layout(
            title='7-Day Weather Forecast with Disease Risk Areas',
            xaxis_title='Date',
            yaxis_title='Values',
            legend_title_text='Metrics and Disease Risks'
        )

        # Show the plot in Streamlit
        st.plotly_chart(fig)
        
        
    st.write("### Disease Conditions")
    st.dataframe(disease_df)

    # Display the plot
    
    st.button("Send Emails")