import pickle
import telebot

bot = telebot.TeleBot('5535308530:AAGnO-vB4095ZIJvfb_d9--qpGPX29S0WOo')

with open('saved_users.pkl', 'rb') as f: #Подгружаем базу пользователей
    users_d = pickle.load(f)