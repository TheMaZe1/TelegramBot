from loader import *
from keyboards import *

#Обновлениие базы пользователей
def update_users(users_d):
    with open('saved_users.pkl', 'wb') as f:  #
        pickle.dump(users_d, f)

#Отправка приветсвенного сообщения пользователю
def hello_user(message, user_id):
    bot.send_message(user_id, "Здравсвтуйте <b>" + users_d[user_id]["name"] + "</b>\nЯ скучал\nЧем займемся?",
                     parse_mode="html", reply_markup=markup_menu)

#Создание пользовател и сохранение его в базе
def create_profile(message, users_d, user_id):
    mes = message.text.split()
    if (len(mes) != 3):
        bot.send_message(message.from_user.id, "Криворукий, формат для дибилов, да?", reply_markup=markup_main)
    else:
        for i in mes:
            if (i.isdigit()):
                bot.send_message(message.from_user.id, "Криворукий, формат для дибилов, да?", reply_markup=markup_main)
                break
            else:
                info = message.text.split()
                users_d[user_id] = {"surname": info[0],
                                    "name": info[1],
                                    "city": info[2]
                                    }
                update_users(users_d)
                bot.send_message(message.chat.id, "Рад познакомится <b>" + users_d[user_id]["name"] + "</b>",
                                 parse_mode="html", reply_markup=markup_main)
                break

#Проверка наличия пользователя в базе
def check_user(user_id):
    if user_id not in users_d:
        return False
    else:
        return True
