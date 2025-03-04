import requests, sys
from tkinter import *
oras = input("Introduceti un oras: ")
print("Vei afla informatii despre poluarea din %s:" % oras)
API_key = "6525089e4bb0be97e7a64adc9e9b1081"
city = requests.get("http://api.openweathermap.org/geo/1.0/direct?q=%s&appid=%s" % (oras, API_key))
if(city.status_code == 200):
    datac = city.json()
    if not datac:
        print("Oras inexistent")
        sys.exit(0)
    lat = datac[0]['lat']
    lon = datac[0]['lon']
r = requests.get("http://api.openweathermap.org/data/2.5/air_pollution?lat=%f&lon=%f&appid=%s" % (lat, lon, API_key))
weather = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=%f&lon=%f&appid=%s" % (lat, lon, API_key))
data_pollution = r.json()
data_weather = weather.json()
try:
    temperature = data_weather['main']['temp']
    temperature -= 273.15
    humidity = data_weather['main']['humidity']
    pm2_5 = data_pollution['list'][0]['components']['pm2_5']
    pm10 = data_pollution['list'][0]['components']['pm10']
    airq = data_pollution['list'][0]['main']['aqi']
except KeyError:
    print("Datele nu sunt disponibile")
print("Temp: %.2f °C" % temperature)
print("Humidity: %d" % humidity + str.format("%"))
print("Indicele de caliate al aerului este: %d" % airq)
print("PM2.5: %.2f µg/m³" % pm2_5)
print("PM10: %.2f µg/m³" % pm10)