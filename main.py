import telebot
from telebot import types
import pickle
from whether import check_weather_one_hour

bot = telebot.TeleBot('5535308530:AAGnO-vB4095ZIJvfb_d9--qpGPX29S0WOo')

with open('saved_users.pkl', 'rb') as f: #Подгружаем базу пользователей
    users_d = pickle.load(f)

#основная клавиатура
markup_main = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
itembtn = types.KeyboardButton('Привет, Дима')
markup_main.add(itembtn)

#Проверка зарегистрирован ли пользователь
def check_user(user_id):
    if user_id not in users_d:
        return False
    else:
        return True

#Отправка приветствия пользователю
def hello_user(message, user_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    itembtn1 = types.InlineKeyboardButton('Че по погоде', callback_data="weather")
    itembtn2 = types.InlineKeyboardButton('Настройки', callback_data="settings")
    markup.add(itembtn1)
    bot.send_message(user_id, "Здравсвтуйте <b>" + users_d[user_id][1] + "</b>\nЯ скучал\nЧем займемся?",
                     parse_mode="html", reply_markup=markup)

    # bot.send_message(user_id, "Коротоко о погоде:")
    # bot.send_message(user_id, check_weather_one_hour(users_d[user_id][2]))


#Функция начал взаисодействия с ботом
#Проверяет есть ли пользователь в базе
#Если нет знакомится, иначе приветсвует
@bot.message_handler(commands = ['start'])
def start(message):
    user_id = message.from_user.id
    if(not(check_user(user_id))):
        bot.send_message(message.chat.id, "Здраствуйте, я Дима, бот помощник, мы свами еще не знакомы, давайте заполним информацию")
        mess = bot.send_message(message.chat.id,"Введите ваше ФИ и город\nФормата: \'Ф И Г\' ")
        bot.register_next_step_handler(mess, create_profile,users_d,user_id)
    else:
        hello_user(message, user_id)


def create_profile(message,users_d,user_id):
    users_d[user_id] = message.text.split()
    with open('saved_users.pkl', 'wb') as f:
        pickle.dump(users_d, f)
        bot.send_message(message.chat.id, "Здравсвтуйте <b>" + users_d[user_id][1] + "</b>\nЯ скучал", parse_mode="html")

# @bot.message_handler(commands = ['hello'])
# def hello_dima(message):
#     bot.send_message(message.chat.id, "Здравсвтуйте <b>" + users_d[user_id][1] + "</b>\nЯ скучал", parse_mode="html")
# @bot.message_handler(commands = ['menu'])
# def menu(message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton("Создать ваш профиль", callback_data="create_profile"))
#     bot.send_message(message.chat.id, "Давайте заполним информацию о вас", reply_markup=markup)

# @bot.message_handler(commands = ['help'])
# def start(message):
#     bot.send_message(message.chat.id,"Вот что я могу делать:")

@bot.message_handler(content_types=['text'])
def any_text(message):
    if(message.text == "Привет, Дима"):
        hello_user(message, message.from_user.id)
    else:
        bot.send_message(message.chat.id, "Возможно вы написали что то умное, или отличную шутку\nНо я ограничен технологиями своего времени чтобы понять вас\nСписок доступных команд:  /help")

@bot.callback_query_handler(func=lambda call: call.data == "weather")
def show_weather(call):
    bot.send_message(call.from_user.id, "Коротоко о погоде:")
    bot.send_message(call.from_user.id, check_weather_one_hour(users_d[call.from_user.id][2]), reply_markup=markup_main)

@bot.callback_query_handler(func=lambda call: call.data == "settings")
def show_weather(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    itembtn1 = types.InlineKeyboardButton('Редактировать профиль', callback_data="weather")
    bot.send_message(call.from_user.id, "Коротоко о погоде:")
    bot.send_message(call.from_user.id, check_weather_one_hour(users_d[call.from_user.id][2]), reply_markup=markup_main)

bot.polling(none_stop = True)