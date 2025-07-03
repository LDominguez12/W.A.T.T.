import requests

url = 'https://power.larc.nasa.gov/api/temporal/daily/point'

params = {
    'start': 20040623,
    'end': 20040624,
    'latitude': 35.08,
    'longitude': -106.65,
    'community': 're',
    'parameters': 'T2M,WS2M,RH2M,WS10M',
    'format': 'csv',
    'user': 'Luis12',
    'header': 'false'
}

response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.text
    print(data)
else:
    print(f"Error: {response.status_code}")
    
