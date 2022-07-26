import pickle
import telebot
with open('saved_users.pkl', 'rb') as f: #Подгружаем базу пользователей
    users_d = pickle.load(f)

print(users_d)

bot = telebot.TeleBot('5535308530:AAGnO-vB4095ZIJvfb_d9--qpGPX29S0WOo')
st = "Аня Токсик"
photo = open('АняТоксик.jpg', 'rb')

print(st)
for i in range(10):
    bot.send_message(1024424598, st)
    bot.send_photo(1024424598, photo)
    photo = open('АняТоксик.jpg', 'rb')