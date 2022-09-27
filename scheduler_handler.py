from scheduler import Scheduler
import time
from bot_messanges import *
import datetime

queue_scheduler = {}

class P_schedule():  # Class для работы с schedule
    def start_schedule():  # Запуск schedule
        scheduler = Scheduler()
        scheduler.daily(datetime.time(hour=8, minute=00), morning_hello, args=())
        ######Параметры для schedule######
        for user in users_d:
            for date in users_d[user]["notes"]:
                scheduler.once(date,send_note,args=(user,date))
        #print(scheduler)
        ##################################
        while True:  # Запуск цикла
            scheduler.exec_jobs()
            if len(queue_scheduler)!=0:
                for user in queue_scheduler:
                    scheduler.once(queue_scheduler[user], send_note, args=(user, queue_scheduler[user]))
            queue_scheduler.clear()
            time.sleep(1)