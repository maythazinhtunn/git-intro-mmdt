import pandas as pd
import requests

# OpenWeatherMap API Key (Replace with your actual API key)
API_KEY = "e29ec1a1acfdf93a96f642e14cc78777"

# List of cities
CITIES = ["London", "New York", "Tokyo", "Delhi", "Paris"]

# Base API URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# List to store weather data
weather_data = []

# Loop through each city and fetch weather data
for city in CITIES:
    url = f"{BASE_URL}?q={city}&appid={API_KEY}"
    response = requests.get(url, verify=False)
    
    if response.status_code == 200:  # Check if request was successful
        data = response.json()
        # print(data)
        weather_info = {
            "City": city,
            "Temperature (°C)": data["main"]["temp"],
            "Humidity (%)": data["main"]["humidity"],
            "Weather": data["weather"][0]["description"],
            "Wind Speed (m/s)": data["wind"]["speed"],
        }
        weather_data.append(weather_info)
    else:
        print(f"Failed to fetch data for {city}: {response.status_code}")

# Create DataFrame
df = pd.DataFrame(weather_data)

# Print DataFrame
print(df)

# Optional: Save to CSV
df.to_csv("weather_data.csv", index=False)
