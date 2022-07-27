import pickle

import requests
import telebot
from geopy import geocoders

with open('saved_users.pkl', 'rb') as f: #Подгружаем базу пользователей
    users_d = pickle.load(f)
#
# print(users_d)
#
# bot = telebot.TeleBot('5535308530:AAGnO-vB4095ZIJvfb_d9--qpGPX29S0WOo')
# bot.send_message(1024424598,"Хей, теперь ты можешь редактировать инфрмацию о себе, и больше не жить в Ямало-ненецком АО")
