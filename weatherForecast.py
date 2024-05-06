import requests
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime




# Your OpenWeatherMap API key
api_key = 'enter api key here'

user_input = input("Enter city: ")

response= requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")

# Fetch weather data from the API
#response = requests.get(url)

from flask import Flask, render_template
from io import BytesIO
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)


if response.status_code == 200:
    # Parse JSON response
    weather_data = response.json()

    # Extract relevant weather information
    weather_description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    temperature = round((temperature - 32)/1.8,1);
    real_feel = weather_data['main']['feels_like']
    real_feel = round((real_feel - 32)/1.8,1);

    # Display weather information on the terminal
    print(f'Weather in {user_input}:')
    print(f'Description: {weather_description}')
    print(f'Temperature: {temperature}°C')
    print(f'Feels like: {real_feel}°C')
    print(f'Humidity: {humidity}%')
    
else:
    print('Failed to fetch weather data. Please check your API key or city name.')
    
    
# OpenWeatherMap API endpoint for weather forecast
forecast_url = "http://api.openweathermap.org/data/2.5/forecast"

# Parameters for the API request
params = {
    'q': user_input,
    'units': 'metric',
    'appid': api_key
}

response = requests.get(forecast_url, params=params)
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse JSON response
    forecast_data = response.json()

    # Extract relevant forecast information
    forecasts = forecast_data['list']

    # Print forecast information
    print(f"5-day weather forecast for {user_input}:")
    for forecast in forecasts:
        date_time = forecast['dt_txt']
        temperature = forecast['main']['temp']
        description = forecast['weather'][0]['description']
        print(f"{date_time}: {description}, Temperature: {temperature}°C")
else:
    print("Failed to fetch weather forecast. Check your API key or city name.")
    


# Extract temperature and date-time data from the forecast
dates = [forecast['dt_txt'] for forecast in forecasts]
temperatures = [forecast['main']['temp'] for forecast in forecasts]

# Convert date-time strings to datetime objects
dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in dates]

# # Plot the temperature data
# plt.figure(figsize=(10, 6))
# plt.plot(dates, temperatures, marker='o', color='b')
# plt.title(f"5-day Temperature Forecast for {user_input}")
# plt.xlabel("Date")
# plt.ylabel("Temperature (°C)")
# plt.grid(True)
# plt.xticks(rotation=45)

# # Display the plot
# plt.tight_layout()
# plt.show()

# # Extract humidity data from the forecast
humidities = [forecast['main']['humidity'] for forecast in forecasts]
feels_like = [forecast['main']['feels_like'] for forecast in forecasts]

# # Plot the humidity data
# plt.figure(figsize=(10, 6))
# plt.bar(dates, humidities, color='g')
# plt.title(f"5-day Humidity Forecast for {user_input}")
# plt.xlabel("Date")
# plt.ylabel("Humidity (%)")
# plt.grid(True)
# plt.xticks(rotation=45)
# # Display the plot
# plt.tight_layout()
# plt.show()

# from collections import defaultdict
# from flask import Flask, render_template

# daily_temperatures = defaultdict(list)

# # Group temperature data by date
# current_date = dates[0].date()
# for date, temperature in zip(dates, temperatures):
#     if date.date() == current_date:
#         daily_temperatures[current_date].append(temperature)
#     else:
#         current_date = date.date()
#         daily_temperatures[current_date].append(temperature)

# for date, temps in daily_temperatures.items():
#     print(f"{date}: {temps}")
    
    
# # Calculate the average temperature for each day
# average_temperatures = {date: sum(temps) / len(temps) for date, temps in daily_temperatures.items()}
# print("Average temperatures:")

# plt.figure(figsize=(10, 6))
# plt.boxplot(list(daily_temperatures.values()), labels=list(daily_temperatures.keys()))
# plt.title("5-day Temperature Forecast Boxplot")
# plt.xlabel("Date")
# plt.ylabel("Temperature (°C)")
# plt.grid(True)
# plt.show()


            
# rainy_days = [forecast['dt_txt'] for forecast in forecasts if 'rain' in forecast['weather'][0]['description'].lower()]

# print("Rainy days:")
# for day in rainy_days:
#     print(day)



from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
from collections import defaultdict

# Sample forecast data (replace with actual data)
#dates = [...]  # List of date-time strings
#temperatures = [...]  # List of temperatures
#humidities = [...]  # List of humidities

# Create Flask app
app = Flask(__name__)

# Function to generate base64 encoded plot
def generate_plot(dates, data, ylabel, title):
    plt.figure(figsize=(10, 6))
    plt.plot(dates, data, marker='o', color='b')
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.xticks(rotation=45)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode()

def generate_barplot(dates, data, ylabel, title):
    plt.figure(figsize=(10, 6))
    plt.bar(dates, data, color='g')
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.xticks(rotation=45)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode()

# Function to generate boxplot for daily temperatures
def generate_boxplot(daily_temperatures):
    plt.figure(figsize=(10, 6))
    plt.boxplot(list(daily_temperatures.values()), labels=list(daily_temperatures.keys()))
    plt.title("5-day Temperature Forecast Boxplot")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode()

# Route to display forecast information
@app.route('/')
def forecast():
    # Convert date-time strings to datetime objects
    #dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in dates]

    # Generate plots
    temperature_plot = generate_plot(dates, temperatures, "Temperature (°C)", f"5-day Temperature Forecast")
    humidity_plot = generate_barplot(dates, humidities, "Humidity (%)", f"5-day Humidity Forecast")
    feels_like_plot = generate_plot(dates, feels_like, "Feels Like (°C)", f"5-day Feels Like Forecast") 

    # Group temperature data by date
    daily_temperatures = defaultdict(list)
    current_date = dates[0].date()
    for date, temperature in zip(dates, temperatures):
        if date.date() == current_date:
            daily_temperatures[current_date].append(temperature)
        else:
            current_date = date.date()
            daily_temperatures[current_date].append(temperature)

    # Generate boxplot for daily temperatures
    boxplot_data = generate_boxplot(daily_temperatures)

    # Identify rainy days
    rainy_days = [date for date, forecast in zip(dates, forecasts) if 'rain' in forecast['weather'][0]['description'].lower()]

    # Render template with forecast information
    return render_template('forecast.html', city = user_input, temperature_plot=temperature_plot, humidity_plot=humidity_plot, boxplot_data=boxplot_data, feels_like_plot = feels_like_plot, rainy_days=rainy_days)

if __name__ == '__main__':
    app.run(debug=True)

