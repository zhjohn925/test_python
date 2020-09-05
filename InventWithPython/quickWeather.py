#! python3
# quickWeather.py - Prints the current weather for a location from the command line.

import json, requests, sys

API_KEY="211c8f8388f56112f2b670d94d784c6f"

# Compute location from command line arguments.
if len(sys.argv) < 2:
    print('Usage: quickWeather.py location')
    sys.exit()
location = ' '.join(sys.argv[1:])

#r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=San&Jose&APPID=211c8f8388f56112f2b670d94d784c6f')

# Download the JSON data from OpenWeatherMap.org's API
url ='http://api.openweathermap.org/data/2.5/forecast/daily?q=%s&cnt=3&APPID=211c8f8388f56112f2b670d94d784c6f' % (location)
response = requests.get(url)
response.raise_for_status()

# Load JSON data into a Python variable.
weatherData = json.loads(response.text)

# Print weather descriptions.
w = weatherData['list']
print('Current weather in %s:' % (location))
print(w[0]['weather'][0]['main'], '-', w[0]['weather'][0]['description'])
print()
print('Tomorrow:')
print(w[1]['weather'][0]['main'], '-', w[1]['weather'][0]['description'])
print()
print('Day after tomorrow:')
print(w[2]['weather'][0]['main'], '-', w[2]['weather'][0]['description'])
