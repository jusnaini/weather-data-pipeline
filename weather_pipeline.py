# %%
# weather_pipeline.py
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# %% Functions for fetching, transforming, and saving weather data
def get_weather_data(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    r = requests.get(BASE_URL, params=params)
    return r.json()

def transform_data(raw_data):
    return {
        "city": raw_data.get("name"),
        "temperature": raw_data.get("main", {}).get("temp"),
        "humidity": raw_data.get("main", {}).get("humidity"),
        "weather": raw_data.get("weather", [{}])[0].get("description"),
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)
    print(f"Saved to {filename}")

def main():
    cities = ["Kuala Lumpur", "Jakarta", "Bangkok", "Singapore", "Manila"]
    results = []

    for city in cities:
        raw_data = get_weather_data(city)
        transformed_data = transform_data(raw_data)
        results.append(transformed_data)

    df = pd.DataFrame(results)
    print(df)

    output_file = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    save_to_csv(df, output_file)

if __name__ == "__main__":
    main()
