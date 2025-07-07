import pandas as pd
import requests
import numpy as np
from datetime import datetime

# Function to get weather data from the NASA Power API
def get_weather_data(Latitude, Longitude, Date):    
    # This is the API im getting data from
    url = 'https://power.larc.nasa.gov/api/temporal/daily/point'
    # Initialize a list to hold all the data
    all_data = []

    for i in range(len(Date)):
        # Parameters for the API request
        params = {
            'start': Date[i],
            'end': Date[i],
            'latitude': Latitude[i],
            'longitude': Longitude[i],
            'community': 're',
            'parameters': 'T2M,WS2M,RH2M,WS10M',
            'format': 'csv',
            'user': 'Luis12',
            'header': 'false'
        }

        # Gets the data and makes sure it works
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            lines = response.text.strip().splitlines()
            data_only = lines[1:]  # Skip the header line
            all_data.extend(data_only)
        else:
            print(f"Failed for index {i}, status code: {response.status_code}")
    
    return all_data

def main():
    # Importing the Fire Entry Data
    dataset = pd.read_csv('Final_Data.csv')
    # Extracting the required columns
    Latitude = dataset.iloc[0:99,1].values
    Longitude = dataset.iloc[0:99,2].values
    Date = dataset.iloc[0:99,9].values

    # Converting the Date format to YYYYMMDD
    Date = [datetime.strptime(str(date), '%m/%d/%Y').strftime('%Y%m%d') for date in Date]

    # Getting the weather data
    all_weather_data = get_weather_data(Latitude, Longitude, Date)

    # Saving the data to a CSV file
    with open('Test_Weather_Data.csv', 'w') as f:
        f.write('YEAR,MO,DY,T2m,WS2M,RH2M,WS10M\n')
        for row in all_weather_data:
            f.write(row + '\n')

if __name__ == "__main__":
    main()