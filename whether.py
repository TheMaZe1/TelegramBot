import requests
from geopy import geocoders
from loader import weather_key_AW,weather_key_OW

dict_weather = {
    "1":"\U00002600",
    "2":"\U00002600",
    "3":"\U0001F324",
    "4":"\U0001F324",
    "5":"\U0001F325",
    "6":"\U0001F325",
    "7":"\U00002601",
    "8":"\U00002601",
    "11":"\U00002601",
    "12":"\U0001F327",
    "13":"\U0001F327",
    "14":"\U0001F326",
    "15":"\U0001F329",
    "16":"\U0001F329",
    "17":"\U0001F329",
    "18":"\U0001F329",
    "19":"\U0001F328",
    "20":"\U0001F328",
    "21":"\U0001F328",
    "22":"\U0001F328",
    "23":"\U0001F328",
    "24":"\U0001F328",
    "25":"\U0001F328",
    "26":"\U0001F328",
    "29":"\U0001F328",
    "30":"\U00002600",
    "31":"\U00002744",
    "32":"\U0001F32C",
    "33":"\U0001F311",
    "34":"\U0001F311",
    "35":"\U0001F311",
    "36":"\U0001F311",
    "37":"\U0001F325",
    "38":"\U0001F325",
    "39":"\U0001F327",
    "40":"\U0001F327",
    "41":"\U0001F329",
    "42":"\U0001F329",
    "43":"\U0001F328",
    "44":"\U0001F328"
}

dict_weather_2 = {
    "01d":"\U00002600",
    "02d":"\U000026C5",
    "03d":"\U00002601",
    "04d":"\U00002601",
    "09d":"\U0001F327",
    "10d":"\U0001F326",
    "11d":"\U0001F329",
    "13d":"\U00002744",
    "50d":"\U0001F32B"
}
#Определение геопозиции человека по его городу
def geo_pos(city: str):
    try:
        geolocator = geocoders.Nominatim(user_agent="telebot")
        latitude = str(geolocator.geocode(city).latitude)
        longitude = str(geolocator.geocode(city).longitude)
        return latitude,longitude
    except Exception as ex:
        return None

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
            (f"🌡 За окном: {round(data[0]['Temperature']['Value'])} C°\n"
             f"{dict_weather[str(data[0]['WeatherIcon'])]} {data[0]['IconPhrase']}\n"
             f"💧 Влажность воздуха: {data[0]['RelativeHumidity']} %\n"
             f"🌧 Вероятность дождя: {data[0]['RainProbability']} %\n"
             f"🌬 Ветер: {data[0]['Wind']['Direction']['Localized']}, скорость {data[0]['Wind']['Speed']['Value']} км/ч")
        return response

#Определение погоды через серви AccuWeather
def get_weather_OW(lat,lon, token):
     r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token}&units=metric&lang=ru")
     data = r.json()
     response = \
         (f"🌡 Температура за окном: {round(data['main']['temp'])} C°\n"
          f"{dict_weather_2[str(data['weather'][0]['icon'])]} {str(data['weather'][0]['main']).title()}\n"
          f"💧 Влажность воздуха: {data['main']['humidity']} %\n"
          f"🌬 Ветер: {data['wind']['deg']}°, {data['wind']['speed']} м/c")
     return response


def check_weather_one_hour(city: str):
    ll = geo_pos(city)
    if ll == None:
        return "Вашего города не существует, измените его в настройках"
    else:
        try:
            return get_wether_AW(ll[0],ll[1],weather_key_AW)
        except Exception:
            try:
                return get_weather_OW(ll[0],ll[1],weather_key_OW)
            except Exception:
                return "Что то пошло не так. Я не могу определить погоду😥"
