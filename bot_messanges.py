from datetime import datetime
from loader import bot,users_d
from keyboards import *
import random
from users import update_users
from whether import *

hello_words = [
    "Я ниче не делал",
    "Я соскучился по вам",
    "Сегодня прекрасный день"
]

citats_dict = [
    "Работа не волк, в лес не убежит"
]


#Отправка приветсвенного сообщения пользователю
def hello_user(user_id):
    bot.send_message(user_id, f"Здравствуйте <b>" + users_d[user_id]["name"] + f"</b>. {hello_words[random.randint(0,len(hello_words)-1)]}"
                                f"\nЧем займемся?🙃",
                     parse_mode="html", reply_markup=markup_menu)

def send_note(user_id,date):
    bot.send_message(user_id, f"Хей, надеюсь ты не забыл, но я всеравно напомню😎:\n\n📌{users_d[user_id]['notes'][date]}")
    del(users_d[user_id]["notes"][date])
    update_users(users_d)

def begin_message(user_id):
    bot.send_message(user_id,
                         "Здраствуйте, я Джарвис, бот помощник.\n"
                         "К сожалению мы с вами еще не знакомы, давайте заполним информацию")
    mess = bot.send_message(user_id, "Введите ваши Фамилию, имя и город\nФормат для ввода: \'Ф И Г\'")
    return mess

def message_notes(user_id):
    response = ""
    if len(users_d[user_id]["notes"]) == 0:
        print(len(users_d[user_id]["notes"]))
        response+=\
            "\n"\
            "Вы свободны от дел, можете погулять"
    else:
        for date,note in users_d[user_id]["notes"].items():
            response+=\
                "\n"\
                f"📌{date.date()}:\n"\
                f"{note}"
    bot.send_message(user_id, response)

def notes_for_day(user_id):
    response = ""
    if len(users_d[user_id]["notes"]) == 0:
        print(len(users_d[user_id]["notes"]))
        response+=\
            "\n"\
            "Вы ничего не запланировали на день"
    else:
        for date,note in users_d[user_id]["notes"].items():
            if(date.date() == datetime.now().date()):
                response+=\
                    "\n"\
                    f"📌{date.date()}:\n"\
                    f"{note}"
            else:
                response += \
                    "\n" \
                    "Вы ничего не запланировали на день"
    return(response)

def morning_hello():
    for user_id in users_d:
        bot.send_message(user_id, f"Доброе утро {users_d[user_id]['name']}\n{check_weather_one_hour(users_d[user_id]['city'])}\nЦитата дня: {citats_dict[0]}\nВаши планы на день: \n{notes_for_day(user_id)}")
        #bot.send_message(user_id, "Привет")
def text(user_id):
    bot.send_message(user_id,   "Возможно вы написали что-то умное, или отличную шутку\n"
                                "Но я ограничен технологиями своего времени чтобы понять вас😔\n"
                                "Перейдите по одной из вкладок меню")