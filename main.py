from telebot.types import CallbackQuery
import telegramcalendar
from games import coinflip
from users import *
from threading import *
from scheduler_handler import *
from bot_messanges import *
from wiki import get_info

# Функция начала взаимодействия с ботом
# Проверяет есть ли пользователь в базе
# Если нет знакомится, иначе приветствует
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if (not (check_user(user_id))):
        bot.register_next_step_handler(begin_message(user_id), create_profile, users_d, user_id)
    else:
        hello_user(user_id)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == "menu")
def menu(call: CallbackQuery):
    callback_data = call.data.split(':')
    if (callback_data[1] == "weather"):
        bot.edit_message_reply_markup(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, f"Коротоко о погоде в {users_d[call.from_user.id]['city']}е:")
        bot.send_message(call.from_user.id, check_weather_one_hour(users_d[call.from_user.id]["city"]))
    elif (callback_data[1] == "settings"):
        bot.edit_message_reply_markup(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, "Настройки:", reply_markup=markup_settings)
    elif (callback_data[1] == "notebook"):
        bot.edit_message_reply_markup(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, "Ежедневник:", reply_markup=markup_notebook)
    elif (callback_data[1] == "wiki"):
        bot.edit_message_reply_markup(call.from_user.id, call.message.id)
        mess = bot.send_message(call.from_user.id, "Введите то, о чем вы хотите узнать: ")
        bot.register_next_step_handler(mess, get_info)
    elif (callback_data[1] == "games"):
        bot.edit_message_reply_markup(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, "Давай поиграем:", reply_markup=markup_games)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == "settings")
def settings(call: CallbackQuery):
    callback_data = call.data.split(':')
    if (callback_data[1] == "edit_profile"):
        bot.edit_message_reply_markup(call.from_user.id, call.message.id)
        mess = bot.send_message(call.from_user.id, "Введите ваши Фамилию, Имя и город\nФормат для ввода: \'Ф И Г\'")
        bot.register_next_step_handler(mess, create_profile, users_d, call.from_user.id)

#обработчик заметок
@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == "notes")
def notes(call: CallbackQuery):
    callback_data = call.data.split(':')
    if (callback_data[1] == "create_note"):
        bot.edit_message_reply_markup(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id,"Выберите дату:",reply_markup=telegramcalendar.create_calendar())
    elif(callback_data[1] == "my_notes"):
        bot.edit_message_reply_markup(call.from_user.id, call.message.id)
        message_notes(call.from_user.id)

@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == "games")
def notes(call: CallbackQuery):
    callback_data = call.data.split(':')
    if (callback_data[1] == "coinflip"):
        bot.edit_message_reply_markup(call.from_user.id, call.message.id)
        t2 = Thread(target=coinflip, args=(bot, call))
        t2.start()



# Обработчик календаря
@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == "CALENDAR")
def note_date(call: CallbackQuery):
    selected, date = telegramcalendar.process_calendar_selection(call, bot)
    if (selected):
        bot.edit_message_reply_markup(call.from_user.id, call.message.id)
        mess = bot.send_message(call.from_user.id, "Введите время в 24-ом формате HH:MM и задачу через пробел")
        bot.register_next_step_handler(mess, telegramcalendar.create_note, call.from_user.id, date, bot)


@bot.message_handler(content_types=['text'])
def any_text(message):
    if (message.text == "Привет, Джарвис"):
        if (message.from_user.id not in users_d):
            bot.send_message(message.from_user.id, "Нажмите старт", reply_markup=markup_start)
        else:
            hello_user(message.from_user.id)
    else:
        text(message.from_user.id)

t1 = Thread(target=P_schedule.start_schedule, args=())
t1.start()

bot.polling(none_stop=True)
