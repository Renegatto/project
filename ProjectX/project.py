import requests
from datetime import timedelta,datetime

from bs4 import BeautifulSoup
from flask import Flask, render_template,request
import pyowm
from pyowm import timeutils


#частично дублирует function.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template ('index.html')


@app.route('/movies')
def movies():
    url = "https://afisha.tut.by/day/2019/10/24"  
    req = requests.get(url)
    page = req.text
    soup = BeautifulSoup(page,"lxml")
    catalog = []
    ivents = soup.findAll('div', attrs= {'class' : 'm-b-border tab-pane active'})
    for films in ivents:
        films = films.findAll('a', attrs= {'class' : 'name'})
        for film in films:
            film = film.text
            catalog.append(film)
    catalog = tuple(catalog)
    return render_template ('movies.html' , mov = catalog)

@app.route('/courses')
def valyta():
    url = "http://www.nbrb.by/API/ExRates/Rates?Periodicity=0"
    all_courses = requests.get(url).json()
    courses = []
    for k in all_courses:
        n = k["Cur_Name"],k["Cur_OfficialRate"]
        courses.append(n)
    courses = dict(courses)
    return render_template('courses.html', sps =courses)
   

@app.route('/weather', methods=['post', 'get'])
def Get_weather():
    owm = pyowm.OWM('872dd8157b4dbabef93b11324b5ecabc')
    city = 'Minsk'
    if request.method == 'POST':
        city = request.form.get('city') 
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    temp = w.get_temperature('celsius')['temp']
    humidity = w.get_humidity()
    
    forecaster = owm.three_hours_forecast(city)
    times = []
    temps = []
    for i in (range(1, 5)):
        time = datetime.now() + timedelta(days=0, hours=i)
        weather = forecaster.get_weather_at(time)
        temperature = weather.get_temperature('celsius')['temp']
        time_s = time.strftime('%H:%M')
        temp_3h = temperature
        times.append(time_s)
        temps.append(temp_3h)
    info = dict(zip(times,temps)) #баг с идентацией как и в function.py
    return render_template('weather.html',t = temp, m = city, h = humidity, info = info)


if __name__ == '__main__':
    #app.debug = True
    app.run('127.0.0.1')