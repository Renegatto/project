import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import pyowm
from pyowm import timeutils
from datetime import timedelta, datetime

app = Flask(__name__)


def movies():
    parsing_page_url = "https://afisha.tut.by/day/2019/10/24"  #хардкод. желательно вынести в отдельный файл
    req = requests.get(parsing_page_url)
    parsing_page = req.text
    soup = BeautifulSoup(parsing_page, "lxml")
    films_catalog = []  #каталог чего?
    events = soup.findAll('div', attrs={'class': 'm-b-border tab-pane active'})
    for event in events:  #когда мы итерируемся по events, каждый элемент будет event, не film
        #переопределять элемент, не используя его значения в цикле - из области хаков. Лучше не прибегать к хакам.
        films = event.findAll('a', attrs={'class': 'name'})     # это можно было бы впихнуть в качестве итератора во  
                                                                # вложенный цикл, но лучше указать явно, что это - films
        for film in films:
            films_catalog.append(film.text) #это достаточно простой код, легко читается. Нет необходимости в доп переменной, тем более с именем film, а не film_name
    films_catalog = tuple(films_catalog)    #почему именно tuple? К list тоже можно обращаться по индексам. Проверить
    return films_catalog 

@app.route('/courses')
def All_courses():  #courses или currency rates? По PEP8 - названия функций и методов должны быть snake_case
    currency_rates_url = "http://www.nbrb.by/API/ExRates/Rates?Periodicity=0"  # "это какой-то url"
    currencies = requests.get(currency_rates_url).json()  #url-ы и прочие магические значения стоит выносить в отдельные файлы чтобы
                                                          #при необходимости изменения не искать их по всем сорцам
    currency_rates = {}
    for currency in currencies:  #имя переменной n - не говорящее. Если это не по принятому в коллективе соглашению - не использовать такие имена.
        currency_rates[currency["Cur_Name"]] = currency["Cur_OfficialRate"]

    #явное - лучше неявного. Генерировать дикт желательно явно, а не преобразованием списка кортежей

    return currency_rates


# @app.route('/weather', methods=['post', 'get'])
def get_weather(city="Minsk", hours=9):

    owm = pyowm.OWM('872dd8157b4dbabef93b11324b5ecabc')
    # if request.method == 'POST':
    #     city = request.form.get('city')
    observation = owm.weather_at_place(city)
    weather = observation.get_weather()  #w - плохое имя переменной

    instant_forecast = {
                "temp": weather.get_temperature('celsius')['temp'],
            "humidity": weather.get_humidity()
            }

    forecaster = owm.three_hours_forecast(city) #внимательно читаем документацию и видим, что эта функция - прогноз на КАЖДЫЕ 3 часа.
    forecast_on_several_hours = []              #например, с 7:00 до 10:00 будет в среднем -3 C, с 11:00 до 14:00 будет -1 С и так далее

    for three_hours in range(0, hours, 3 ):

        time = datetime.now() + timedelta(days=0, hours=three_hours)  
        weather = forecaster.get_weather_at(time)           

        forecast_on_current_3_hours = {
            "time"          : time.strftime('%H:%M'),
            "temperature_C" : weather.get_temperature('celsius')['temp'],
            "humidity"      : weather.get_humidity()
            }

        forecast_on_several_hours.append(forecast_on_current_3_hours)
    return {"instant forecast": instant_forecast ,"several hours forecast": forecast_on_several_hours}

if __name__ == '__main__':
    #app.debug = True
    app.run()
