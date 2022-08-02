import datetime

from telebot.types import CallbackQuery

import telegramcalendar
from whether import check_weather_one_hour
from keyboards import *
from loader import *
import telegramcalendar
import calendar


# Проверка зарегистрирован ли пользователь
def check_user(user_id):
    if user_id not in users_d:
        return False
    else:
        return True


# Отправка приветствия пользователю
def hello_user(message, user_id):
    bot.send_message(user_id, "Здравсвтуйте <b>" + users_d[user_id][1] + "</b>\nЯ скучал\nЧем займемся?",
                     parse_mode="html", reply_markup=markup_menu)


def create_profile(message, users_d, user_id):
    mes = message.text.split()
    if(len(mes) != 3):
        bot.send_message(message.from_user.id, "Криворукий, формат для дибилов, да?",reply_markup=markup_main)
    else:
        for i in mes:
            if(i.isdigit()):
                bot.send_message(message.from_user.id, "Криворукий, формат для дибилов, да?", reply_markup=markup_main)
                break
            else:
                users_d[user_id] = message.text.split()
                with open('saved_users.pkl', 'wb') as f:
                    pickle.dump(users_d, f)
                    bot.send_message(message.chat.id, "Рад познакомится <b>" + users_d[user_id][1] + "</b>",
                                     parse_mode="html", reply_markup=markup_main)
                break

def create_note(message, date):

    pass


# Функция начал взаисодействия с ботом
# Проверяет есть ли пользователь в базе
# Если нет знакомится, иначе приветсвует
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if (not (check_user(user_id))):
        bot.send_message(message.chat.id,
                         "Здраствуйте, я Дима, бот помощник, мы свами еще не знакомы, давайте заполним информацию")
        mess = bot.send_message(message.chat.id, "Введите ваше ФИ и город\nФормата: \'Ф И Г\' ")
        bot.register_next_step_handler(mess, create_profile, users_d, user_id)
    else:
        hello_user(message, user_id)

#menu_callback.filter(button_name = "weather")
@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == "menu" )
def menu(call: CallbackQuery):
    callback_data = call.data.split(':')
    if (callback_data[1] == "weather"):
        bot.edit_message_reply_markup(call.from_user.id,call.message.id)
        bot.send_message(call.from_user.id, "Коротоко о погоде:")
        bot.send_message(call.from_user.id, check_weather_one_hour(users_d[call.from_user.id][2]))
    elif (callback_data[1] == "settings"):
        bot.edit_message_reply_markup(call.from_user.id,call.message.id)
        bot.send_message(call.from_user.id, "Настройки:", reply_markup=markup_settings)
    elif (callback_data[1] == "notebook"):
        bot.edit_message_reply_markup(call.from_user.id,call.message.id)
        bot.send_message(call.from_user.id, "Выберите дату:", reply_markup=telegramcalendar.create_calendar())


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == "settings" )
def settings(call: CallbackQuery):
    callback_data = call.data.split(':')
    if (callback_data[1] == "edit_profile"):
        bot.edit_message_reply_markup(call.from_user.id,call.message.id)
        mess = bot.send_message(call.from_user.id, "Введите ваше ФИ и город\nФормата: \'Ф И Г\' ")
        bot.register_next_step_handler(mess, create_profile, users_d, call.from_user.id)

# @bot.callback_query_handler(func=lambda call: True)
# def test(call: CallbackQuery):
#     print(call.data.split(':')[0])

#Обработчик календаря
@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == "CALENDAR")
def note_date(call: CallbackQuery):
    selected,date = telegramcalendar.process_calendar_selection(call, bot)
    date = datetime.datetime(date.day, date.month, date.year, hour = 12, )
    print(selected,date)
    # if(selected):
    #     mess = "Введите время в 24-ом формате HH:MM"
    #     bot.register_next_step_handler(mess, create_profile, users_d, call.from_user.id)




@bot.message_handler(content_types=['text'])
def any_text(message):
    if (message.text == "Привет, Дима"):
        if (message.from_user.id not in users_d):
            bot.send_message(message.from_user.id, "Нажмите старт", reply_markup=markup_start)
        else:
            hello_user(message, message.from_user.id)
    else:
        bot.send_message(message.chat.id, "Возможно вы написали что то умное, или отличную шутку\n"
                                        "Но я ограничен технологиями своего времени чтобы понять вас\n"
                                        "Список доступных команд:  /help")


bot.polling(none_stop=True)
