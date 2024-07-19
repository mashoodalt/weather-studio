import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

import plotly.express as px
import plotly.graph_objects as go


locations = {
    "Athara": {"lat": "31.1", "lon": "72.0"},
    "Bhowana": {"lat": "31.5", "lon": "72.6"},
    "Chund Bharwana": {"lat": "31.4", "lon": "72.2"},
    "Garh Maharaja": {"lat": "30.8", "lon": "71.9"},
    "Lallian": {"lat": "31.8", "lon": "72.7"},
    "Hafizabad": {"lat": "32.0", "lon": "73.6"},
    "Toba Tek Singh": {"lat": "30.9", "lon": "72.4"}
}


weatherbit_key = st.secrets["WEATHERBIT_API_KEY"]

# Function to get historical weather data from Weatherbit API
def get_weather_data(lat, lon):
    api_key = weatherbit_key  # Replace YOUR_API_KEY with your actual Weatherbit API key
    # Fetching data from the last 7 days
    end_date = pd.to_datetime('today').strftime('%Y-%m-%d')  # today's date as the end date
    start_date = (pd.to_datetime('today') - pd.Timedelta(days=7)).strftime('%Y-%m-%d')  # 7 days ago as the start date
    url = f"https://api.weatherbit.io/v2.0/history/hourly?key={api_key}&start_date={start_date}&end_date={end_date}&lat={lat}&lon={lon}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the API")
        return None

# def calculate_disease_severity(weather_data, disease_criteria):
#     # Initialize a dictionary to hold the severity, hours count for consecutive and total hours met for each disease
#     disease_severity = {disease: {'hours_met': 0, 'total_hours_met': 0, 'severity': 0} for disease in disease_criteria}

#     # Process each hourly record in the weather data
#     for hour in weather_data:
#         for disease, criteria in disease_criteria.items():
#             # Check if the conditions for this disease are met
#             if (criteria['min_temp'] <= hour['temp'] <= criteria['max_temp'] and
#                 criteria['min_humidity'] <= hour['rh'] <= criteria['max_humidity']):
#                 # Increment the hour count for this disease
#                 disease_severity[disease]['hours_met'] += 1
#                 disease_severity[disease]['total_hours_met'] += 1
#             else:
#                 # Calculate and update severity if conditions were not met and reset hours count
#                 if disease_severity[disease]['hours_met'] > 0:
#                     disease_severity[disease]['severity'] = calculate_severity(disease_severity[disease]['hours_met'])
#                 disease_severity[disease]['hours_met'] = 0

#     # Final update for severity after the last hour
#     for disease in disease_criteria:
#         if disease_severity[disease]['hours_met'] > 0:
#             disease_severity[disease]['severity'] = calculate_severity(disease_severity[disease]['hours_met'])

#     return disease_severity

# Some Open AI magic

# api_key = "sk-proj-6D1i4318S0sF56wfR9tsT3BlbkFJS3TfFZdpvl9j5mPJG9D7"
api_key = st.secrets["OPENAI_API_KEY"]

# The endpoint for the OpenAI API (specify if you are using a particular model or feature)
url = 'https://api.openai.com/v1/chat/completions'





def calculate_disease_severity(weather_data, disease_criteria):
    # Initialize a dictionary to hold the severity, hours count for consecutive and total hours met for each disease
    disease_severity = {disease: {'hours_met': 0, 'total_hours_met': 0, 'severity': 0} for disease in disease_criteria}

    # Process each hourly record in the weather data
    for hour in weather_data:
        for disease, criteria in disease_criteria.items():
            # Check if the conditions for this disease are met
            if (criteria['min_temp'] <= hour['temp'] <= criteria['max_temp'] and
                criteria['min_humidity'] <= hour['rh'] <= criteria['max_humidity']):
                # Increment the hour count for this disease
                disease_severity[disease]['hours_met'] += 1
                disease_severity[disease]['total_hours_met'] += 1
            else:
                # Update severity if conditions were not met and reset hours count
                if disease_severity[disease]['hours_met'] > 0:
                    current_severity = calculate_severity(disease_severity[disease]['hours_met'])
                    # disease_severity[disease]['total_severity'] = max(disease_severity[disease]['severity'], current_severity)
                    disease_severity[disease]['hours_met'] = 0

    # Final update for severity after the last hour
    for disease in disease_criteria:
        if disease_severity[disease]['hours_met'] > 0:
            current_severity = calculate_severity(disease_severity[disease]['hours_met'])
            disease_severity[disease]['severity'] = max(disease_severity[disease]['severity'], current_severity)

    return disease_severity


def calculate_severity(hours_met):
    if hours_met > 3:
        return int(hours_met) * 2
    else:
        return 0
    # if hours_met >= 48:
    #     return 100
    # elif hours_met >= 36:
    #     return 75
    # elif hours_met >= 24:
    #     return 50
    # elif hours_met >= 12:
    #     return 25
    # else:
    #     return 0
    
    
disease_criteria = {
    'Brown Spot': {'min_temp': 16, 'max_temp': 36, 'min_humidity': 85, 'max_humidity': 100},
    'Sheath Rot': {'min_temp': 20, 'max_temp': 32, 'min_humidity': 85, 'max_humidity': 100},
    'Sheath Blight': {'min_temp': 17, 'max_temp': 36, 'min_humidity': 85, 'max_humidity': 100},
    'False Smut': {'min_temp': 25, 'max_temp': 35, 'min_humidity': 90, 'max_humidity': 100},
    'Rice Blast': {'min_temp': 19, 'max_temp': 32, 'min_humidity': 90, 'max_humidity': 100},
    'Bacterial Leaf Blight': {'min_temp': 21, 'max_temp': 36, 'min_humidity': 70, 'max_humidity': 100},
    'Bakanae': {'min_temp': 20, 'max_temp': 35, 'min_humidity': 90, 'max_humidity': 100},
    'Bacterial Panicle Blight': {'min_temp': 25, 'max_temp': 40, 'min_humidity': 85, 'max_humidity': 100}
}
    
def plot_weather_data(weather_data):
    # Convert list of dictionaries (hourly data) into a DataFrame
    df = pd.DataFrame(weather_data)

    # Convert timestamps to datetime objects for better plotting
    df['datetime'] = pd.to_datetime(df['timestamp_local'])

    # Create a Plotly graph object
    fig = go.Figure()

    # Add temperature trace
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['temp'],
                             mode='lines+markers',
                             name='Temperature (°C)',
                             line=dict(color='firebrick', width=2)))

    # Add humidity trace
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['rh'],
                             mode='lines+markers',
                             name='Relative Humidity (%)',
                             line=dict(color='royalblue', width=2)))

    # Add precipitation trace
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['precip'],
                             mode='lines+markers',
                             name='Precipitation (mm)',
                             line=dict(color='green', width=2)))

    # Update plot layout
    fig.update_layout(title='Weather Data Over Time',
                      xaxis_title='Time',
                      yaxis_title='Value',
                      legend_title='Variable',
                      template='plotly_dark')

    return fig
    
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
            

# Initialize latitude and longitude fields
lat = st.text_input("Enter Latitude", locations[st.session_state['selected_location']]["lat"] if st.session_state['selected_location'] else "31.5")
lon = st.text_input("Enter Longitude", locations[st.session_state['selected_location']]["lon"] if st.session_state['selected_location'] else "72.6")
crop = st.selectbox('Select Crop', ["Rice"], 0, disabled=True)

# Button to fetch data
if st.button("Get Weather Data", type="primary"):
    weather_data = get_weather_data(lat, lon)
    if weather_data:
        # Display the city name
        city_name = weather_data.get('city_name', 'Unknown City')
        st.header(f"Weather Forecast for {city_name}")
    severity = calculate_disease_severity(weather_data["data"], disease_criteria)
    # st.write(severity)
    def create_disease_plot(disease_data):
        diseases = list(disease_data.keys())
        total_hours = [data['total_hours_met'] for data in disease_data.values()]
        consecutive_hours = [data['hours_met'] for data in disease_data.values()]
        severities = [data['severity'] for data in disease_data.values()]
        # total_severities = [data['total_severity'] for data in disease_data.values()]

        # Creating bar chart for total hours met
        fig = go.Figure(data=[
            go.Bar(name='Total Hours Met', x=diseases, y=total_hours, marker_color='blue'),
            go.Bar(name='Consecutive Hours (current)', x=diseases, y=consecutive_hours, marker_color='yellow'),
            go.Bar(name='Severity', x=diseases, y=severities, marker_color='red'),
            # go.Bar(name='Total Severity', x=diseases, y=total_severities, marker_color='purple')
        ])

        # Change the bar mode
        fig.update_layout(barmode='group', title='Disease Conditions and Severity',
                        xaxis_title='Disease', yaxis_title='Value')
        return fig

    # Plotting in Streamlit
    st.title('Disease Analysis')
    fig = create_disease_plot(severity)
    st.plotly_chart(fig)
    fig2 = plot_weather_data(weather_data["data"])
    st.plotly_chart(fig2)
    
    # print(weather_data["data"])
    # print(disease_criteria)
    #  'precip': entry['precip'],
    simplified_data = [{'temp': entry['temp'], 'humidity': entry['rh'], 'datetime': entry['datetime']} for entry in weather_data["data"]]

    
    gptdata = {
    "model": "gpt-4o",
    "temperature": 0.2,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "messages": [
      {
        "role": "system",
        "content": "You will be provided with hourly weather data and disease criteria for various agricultural diseases. Your task is to analyze the likelihood of these diseases based on the given weather conditions. Use the temperature and humidity data to determine if the conditions meet the thresholds for any diseases. Provide an assessment of which diseases are likely to occur. If weather conditions are within disease range for 12 hours consecutively, the likelihood of disease is growing. If it consecutively in range for over 24 hours, the likelihood of disease is extremely high. Lower than these ranges, the likelihood of disease is low. Also include the average temperature and humidity in your analysis, and mention the worst day from the last week in terms of disease severity and the best day. I also want you to write the longest time when disease condition was met for every disease during the period."
      },
      {
        "role": "user",
        "content": f"The disease criteria is the following: {disease_criteria}"
      },
      {
        "role": "user",
        "content": f'Weather Data: {simplified_data}'
      }

    ]
  }


    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Make the POST request
    response = requests.post(url, json=gptdata, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        st.header("AI Analysis")
        st.write(content)
        print(response.json())
    # st.write(weather_data["data"])
    # st.write(severity)
    
    print(response.json)
    
    
