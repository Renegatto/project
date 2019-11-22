import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template,url_for


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
    url = "http://www.nbrb.by/statistics/rates/ratesdaily.asp"

    req2 = requests.get(url)
    page2 = req2.text
    soup2 = BeautifulSoup(page2,"lxml")
    val = []
    nam = []
    courses = soup2.findAll('td', attrs= {'class' : 'curCours'})
    for cours in courses:
        cours = cours.text
        val.append(cours.lstrip())
    names = soup2.findAll('span', attrs= {'class' : 'text'})
    for name in names:
        name = name.text
        nam.append(name)
    val_nam =dict(zip(nam,val))
    
    return render_template('courses.html', sps =val_nam)
   
@app.route('/data/2.5/weather')
def gen_url():
    pass

api = 'http://api.openweathermap.org'
key = '872dd8157b4dbabef93b11324b5ecabc'
city = input('Введите город латинскими буквами:')

with  app.test_request_context():   
    url_w = (url_for('gen_url', q=city, appid=key))
    url_y = api + url_w

@app.route('/weather')
def Get_weather():

    req = requests.get(url_y)
    main = req.json()
    temp = main["main"]
    Kelvin = temp["temp"]
    Celc = Kelvin - 273
    Celc2 = round(Celc,1)
    return render_template('weather.html',t = Celc2, m = city)

if __name__ == '__main__':
    app.debug = True
    app.run()