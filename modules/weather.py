import requests
from .base import Module

class Weather(Module):
    def exec(self):
        city_id = 524901
        appid = "267758e07b3f07db17976b089302c1a1"
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            description = str(data['weather'][0]['description'])
            temp = str(data['main']['temp'])
            return f"Сегодня {description} и температура {temp} градусов по цельсию"
        except:
            return "Ошибка поиска"