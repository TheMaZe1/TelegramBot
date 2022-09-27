from datetime import datetime
from loader import *
from keyboards import *

#Обновлениие базы пользователей
def update_users(users_d):
    with open('saved_users.pkl', 'wb') as f:  #
        pickle.dump(users_d, f)

#Создание пользовател и сохранение его в базе
def create_profile(message, users_d, user_id):
    mes = message.text.split()
    if (len(mes) != 3):
        bot.send_message(message.from_user.id, "Ну я же написал формат для ввода :(", reply_markup=markup_main)
    else:
        for i in mes:
            if (i.isdigit()):
                bot.send_message(message.from_user.id, "Ну я же написал формат для ввода :(", reply_markup=markup_main)
                break
            else:
                info = message.text.split()
                users_d[user_id] = {"surname": info[0],
                                    "name": info[1],
                                    "city": info[2],
                                    "notes": {}
                                    }
                update_users(users_d)
                bot.send_message(message.chat.id, "Рад познакомиться <b>" + users_d[user_id]["name"] + "</b>",
                                 parse_mode="html", reply_markup=markup_main)
                logger(f"create/edit user:{user_id}, {users_d[user_id]['name']}, {users_d[user_id]['surname']}, {users_d[user_id]['city']}")
                print(f"create/edit user:{user_id}, {users_d[user_id]['name']}, {users_d[user_id]['surname']}, {users_d[user_id]['city']}")
                break

#Проверка наличия пользователя в базе
def check_user(user_id):
    if user_id not in users_d:
        return False
    else:
        return True

def logger(text):
    with open("log.txt", "a",encoding="UTF-8") as f:
        f.write(str(datetime.now()) +": "+text+"\n")