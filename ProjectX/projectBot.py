import telebot
import requests
from bs4 import BeautifulSoup
from flask import Flask
from function import movies
from function import All_courses



get_movies = movies()
get_courses = All_courses()
Token = '' #убрал


keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Movies' , 'Cours','Weather')
bot = telebot.TeleBot(Token)
@bot.message_handler(commands=['start'])

def start_message(message):
    bot.send_message(message.chat.id,'Что хотите узнать?', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.text.lower() == 'movies':
        bot.send_message(message.chat.id,'\n'.join(get_movies))
    elif message.text.lower() == 'cours':
        cur2 = []
        for k, v in get_courses.items():
            cur = (k+' '+'-'+' '+v)
            cur2.append(cur)
        bot.send_message(message.chat.id,'\n'.join(cur2))
    
bot.polling()