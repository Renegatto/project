from typing import Callable
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from flask import Flask
from function import movies, All_courses, get_weather
from datetime import timedelta, datetime


weather = get_weather()["instant forecast"]
get_movies = movies()
get_currencies = All_courses()
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

def is_message_lowercase_an( whichMessage ): #а можно еще и попробовать внедрять ФП. Псевдо-каррирование, например
    def equal_to( toTest ):                  #здесь для примера, но будь кода больше - могло бы быть полезно
        return message.text.lower() == equalTo
def answer_to_message( message ):
    def answer_is( answer, parse_mode=None ):
        if parse_mode :
            return bot.send_message(message.chat.id, answer, parse_mode=parse_mode)
        return bot.send_message(message.chat.id, answer)

@bot.message_handler(content_types=['text'])
def send_message(message):

    is_message_a : Callable[[str],bool] = is_message_lowercase_an(message)
    answer       : Callable[[str],None] = answer_to_message(message)

    if is_message_a('movies 🎥'):
        answer('\n'.join(get_movies))
    elif is_message_a('cours 💰'):
        answer("*Курс на сегодня:*", parse_mode='Markdown')

        currency_rate_messages = []
        for currency_name, currency_rate in get_currencies.items():
            currency_rate_messages.append( f'{currency_name} - {currency_rate}' )

        answer('\n'.join(currency_rate_messages))

    elif is_message_a('weather 🌡️'):      
        answer(f'Погода в Минске - температура : {weather["temperature C"]}°C, влажность : {weather["humidity"]}%')
        
        if weather["temperature C"] <= 0:
           answer( 'Холодно,нужен шарф(')
        else:
           answer('Норм, можно без носков)')
    
#bot.polling()