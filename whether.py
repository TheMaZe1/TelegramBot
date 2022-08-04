import requests
import json
from pprint import pprint
from geopy import geocoders
from loader import weather_key_AW,weather_key_OW

#Определение геолпозиции человека по его городу
def geo_pos(city: str):
        geolocator = geocoders.Nominatim(user_agent="telebot")
        latitude = str(geolocator.geocode(city).latitude)
        longitude = str(geolocator.geocode(city).longitude)
        return latitude,longitude

#Определение погоды через серви AccuWeather
def get_wether_AW(latitude,longitude, token):
        #определение Location key
        code = requests.get(
            f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={token}&q={latitude},{longitude}&language=ru")
        code_json = code.json()
        location_code = code_json["Key"]
        #определение погоды в соответствии с Location key
        r = requests.get(
            f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{location_code}?apikey={token}&language=ru&metric=True&details=true')
        data = r.json()
        #оформление готового вывода информации о погоде
        response = \
            (f"""За окном: {data[0]['Temperature']['Value']} C, {data[0]['IconPhrase']}
            Влажность воздуха: {data[0]['RelativeHumidity']}, Вероятность дождя: {data[0]['RainProbability']}
            Ветер: {data[0]['Wind']['Direction']['Localized']} {data[0]['Wind']['Speed']['Value']} км/ч""")
        return response

#Определение погоды через серви AccuWeather
def get_weather_OW(lat,lon, token):
     r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token}&units=metric")
     data = r.json()
     response = (f"""За окном: {data['main']['temp']} C, {data['weather'][0]['description']}
     Влажность воздуха: {data['main']['humidity']}
     Ветер: {data['wind']['deg']} {data['wind']['speed']} м/c""")
     return response


# def get_weather(location_code, token):
#      return(response)


def check_weather_one_hour(city: str):
    ll = geo_pos(city)
    try:
        return get_wether_AW(ll[0],ll[1],weather_key_AW)
    except Exception as ex:
        print(ex)
        try:
            return get_weather_OW(ll[0],ll[1],weather_key_OW)
        except Exception as ex:
            print(ex)
            return "Датчики умерли, не возможно определить погоду"
