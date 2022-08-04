from loader import *
from users import users_d,update_users
from scheduler import Scheduler
import time

queue_scheduler = []

def send_test(user_id,date):
    bot.send_message(user_id, users_d[user_id]["notes"][date])
    del(users_d[user_id]["notes"][date])
    update_users(users_d)


class P_schedule():  # Class для работы с schedule
    def start_schedule():  # Запуск schedule
        scheduler = Scheduler()
        ######Параметры для schedule######
        for user in users_d:
            for date in users_d[user]["notes"]:
                print(date)
                scheduler.once(date,send_test,args=(user,date))
        print(scheduler)
        ##################################
        while True:  # Запуск цикла
            scheduler.exec_jobs()
            if len(queue_scheduler)!=0:
                for date in queue_scheduler:
                    scheduler.once(date, send_test, args=(user, date))
                    queue_scheduler.remove(date)
            time.sleep(1)