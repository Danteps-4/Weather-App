import requests
from decouple import config
from timezonefinder import TimezoneFinder
import pytz
import datetime

tf = TimezoneFinder()

def get_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config('API_KEY')}"
    response = requests.get(url)
    if response:
        data = response.json()

        temp_kelvin = data["main"]["temp"]
        country = data["sys"]["country"]
        icon = data["weather"][0]["icon"]
        weather = data["weather"][0]["main"]
        city = data["name"]
        lon = data["coord"]["lon"]
        lat = data["coord"]["lat"]
        max_temp = data["main"]["temp_max"]
        min_temp = data["main"]["temp_min"]

        # Datetime
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        timezone_str = str(timezone_str)
        dt = datetime.datetime.now(pytz.timezone(timezone_str))

        final = (city, country, temp_kelvin, icon, weather, dt, min_temp, max_temp)
        return final
    else:
        return None