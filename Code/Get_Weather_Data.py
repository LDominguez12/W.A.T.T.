import pandas as pd
import requests
from datetime import datetime
from time import sleep

# Function that initialized the API request but with retries now
def fetch_weather(lat, lon, date, retries = 3):
     # This is the API im getting data from
    url = 'https://power.larc.nasa.gov/api/temporal/daily/point'

    # Parameters for the API request
    params = {
        'start': date,
        'end': date,
        'latitude': lat,
        'longitude': lon,
        'community': 're',
        'parameters': 'T2M,WS2M,RH2M,WS10M',
        'format': 'csv',
        'user': 'Luis12',
        'header': 'false'
    }

    # Getting the data but this time with retries
    for attempt in range(retries):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.text.strip().splitlines()[1:]
        else:
            sleep(2)
    
    print(f"Failed to fetch data for ({lat}, {lon}) on {date}. Status code: {response.status_code}")
    return None


# Function to get weather data from the NASA Power API
def get_weather_data(lat, lon, date):    
    # Initialize a list to hold all the data
    all_data = []

    for i in range(len(date)):
        data = fetch_weather(lat[i], lon[i], date[i])
        all_data.extend(data)
    
    return all_data

def main():
    # Importing the Fire Entry Data
    dataset = pd.read_csv('Final_Data.csv')
    # Extracting the required columns
    lat = dataset.iloc[100:149,1].values
    lon = dataset.iloc[100:149,2].values
    date = dataset.iloc[100:149,9].values

    # Converting the Date format to YYYYMMDD
    date = [datetime.strptime(str(date), '%m/%d/%Y').strftime('%Y%m%d') for date in date]

    # Getting the weather data
    all_weather_data = get_weather_data(lat, lon, date)

    # Saving the data to a CSV file
    with open('Test_Weather_Data2.csv', 'w') as f:
        f.write('YEAR,MO,DY,T2m,WS2M,RH2M,WS10M\n')
        for row in all_weather_data:
            f.write(row + '\n')

if __name__ == "__main__":
    main()