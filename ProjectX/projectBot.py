import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from flask import Flask
from function import movies
from function import All_courses
from function import Get_weather
from datetime import timedelta,datetime


weather = Get_weather()
get_movies = movies()
get_courses = All_courses()
Token = '871811425:AAHX5QPWtd3OvAfmPHbU1qbWyyhy62Nftr4' 
bot = telebot.TeleBot(Token)




keyboard = types.ReplyKeyboardMarkup(True,True)
button_mov = types.KeyboardButton(text = "movies 🎥")
button_geo = types.KeyboardButton(text="Location 🎯", request_location=True)
button_Crs = types.KeyboardButton(text='cours 💰')
button_whr = types.KeyboardButton(text="weather 🌡️")
keyboard.add(button_geo,button_mov,button_whr,button_Crs)


@bot.message_handler(commands=['start'])

def start_message(message):
    bot.send_message(message.chat.id,'Что хотите узнать? 😉', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.text.lower() == 'movies 🎥':
        bot.send_message(message.chat.id,'\n'.join(get_movies))
    elif message.text.lower() == 'cours 💰':
        bot.send_message(message.chat.id,"*Курс на сегодня:*",parse_mode= 'Markdown')
        cur = []
        cur2 = []
        for k, v in get_courses.items():
            cur = (k+' '+'-'+' '+str(v))
            cur2.append(cur)
        bot.send_message(message.chat.id,'\n'.join(cur2))
    elif message.text.lower() == 'weather 🌡️':      
        bot.send_message(message.chat.id, f'Погода в Минске - температура : {weather[0]}°C, влажность : {weather[1]}%')
        if weather[0] <= 0:
           bot.send_message(message.chat.id, 'Холодно,нужен шарф(')
        else:
            bot.send_message(message.chat.id,'Норм, можно без носков)')
    
bot.polling()