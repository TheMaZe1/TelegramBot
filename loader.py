import pickle
import telebot

bot = telebot.TeleBot('5535308530:AAGnO-vB4095ZIJvfb_d9--qpGPX29S0WOo')
weather_key_AW = "VgbA35G6eTNSr4I2CmPcglLMyqv5oXGq"
weather_key_OW = "c96a5e005acac84c24bf91f094f9c5c1"

with open('saved_users.pkl', 'rb') as f: #Подгружаем базу пользователей
    users_d = pickle.load(f)


# for u in users_d:
#     users_d[u]["notes"] ={}
# update_users(users_d)