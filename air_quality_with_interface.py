import requests, sys
import streamlit as st
import folium
import os
from streamlit_folium import st_folium
with st.container():
    st.markdown("<h1 style='text-align: center;'>Aplicație meteo</h1>", unsafe_allow_html=True)
st.markdown("""
    <style>
        .stTextInput>div>div>input {
            text-align: center;
            align-items: center;
        }
        .stButton>div>div {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        .center-text {
        text-align: center;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown('<div class=".stTextInput">', unsafe_allow_html=True)
oras = st.text_input("Introduceți un oraș:")
st.markdown('<div>', unsafe_allow_html=True)
API_key = os.getenv("OpenWeather_API")
col1, col2 = st.columns([115, 200])
col3, col4 = st.columns(2)
with col2:
    if st.button("Afișează datele meteo"):
        if oras:   
            city = requests.get("http://api.openweathermap.org/geo/1.0/direct?q=%s&appid=%s" % (oras, API_key))
            if(city.status_code == 200):
                datac = city.json()
                if not datac:
                    st.write("Oraș inexistent")
                else:
                    lat = datac[0]['lat']
                    lon = datac[0]['lon']
                    pollution = requests.get("http://api.openweathermap.org/data/2.5/air_pollution?lat=%f&lon=%f&appid=%s" % (lat, lon, API_key))
                    weather = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=%f&lon=%f&appid=%s" % (lat, lon, API_key))
                    data_pollution = pollution.json()
                    data_weather = weather.json()
                    st.markdown('<div>', unsafe_allow_html=True)
                    try:
                        temperature = data_weather['main']['temp']
                        temperature -= 273.15
                        humidity = data_weather['main']['humidity']
                        pressure = data_weather['main']['pressure']
                        pm2_5 = data_pollution['list'][0]['components']['pm2_5']
                        pm10 = data_pollution['list'][0]['components']['pm10']
                        airq = data_pollution['list'][0]['main']['aqi']
                        with col3:
                            st.markdown(f"<h5 style='text-align: center;'>Temperatură: {temperature:.2f} °C</h5>", unsafe_allow_html=True)
                            st.markdown(f"<h5 style='text-align: center;'>Umiditate: {humidity}%</h5>", unsafe_allow_html=True)
                            if(airq==1):
                                st.markdown(f"<h5 style='text-align: center;'>Caliatea aerului: {airq} <p> Aer curat 🌿 </h5>", unsafe_allow_html=True)
                            elif(airq==2):
                                st.markdown(f"<h5 style='text-align: center;'>Caliatea aerului: {airq} <p> Sigur pentru majoritatea oamenilor! 😊 </h5>", unsafe_allow_html=True)
                            elif(airq==3):
                                st.markdown(f"<h5 style='text-align: center;'>Caliatea aerului: {airq} <p> Acceptabilă, dar persoanele sensibile pot fi afectate 😷 </h5>", unsafe_allow_html=True)
                            elif(airq==4):
                                st.markdown(f"<h5 style='text-align: center;'>Caliatea aerului: {airq} <p> Evitați expunerea prelungită 🚷 </h5>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<h5 style='text-align: center;'>Caliatea aerului: {airq} <p> Risc major pentru sănătate! ❌ </h5>", unsafe_allow_html=True)
                        with col4:
                            st.markdown(f"<h5 style='text-align: center;'>Presiune: {pressure:.2f} mb</h5>", unsafe_allow_html=True)
                            st.markdown(f"<h5 style='text-align: center;'>PM2.5: {pm2_5:.2f} µg/m³</h5>", unsafe_allow_html=True)
                            st.markdown(f"<h5 style='text-align: center;'>PM10: {pm10:.2f} µg/m³</h5>", unsafe_allow_html=True)
                    except KeyError:
                        st.write("Datele de poluare nu sunt disponibile")
            else:
                st.write("Eroare la accesarea API")
            with col3:
                st.markdown(f"<h5 style='text-align: center;'>Hartă termică:</h5>", unsafe_allow_html=True)
                harta = folium.Map(location=[lat, lon], zoom_start=12)
                folium.Marker([lat, lon], popup=oras).add_to(harta)
                folium.TileLayer(
                    tiles="https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=" + API_key,
                    attr="OpenWeatherMap",
                    name="Temperatura",
                    overlay=True
                ).add_to(harta)
                harta_path = "harta_temp.html"
                harta.save(harta_path)
                with open(harta_path, "r", encoding="utf-8") as f:
                    st.components.v1.html(f.read(), width=700, height=500)
                os.remove(harta_path)
        else:
            st.write("Introduceți un oraș!")