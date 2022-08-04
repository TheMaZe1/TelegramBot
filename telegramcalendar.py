import datetime
import calendar
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import users_d
from users import update_users
from scheduler_handler import queue_scheduler

def create_callback_data(action,year,month,day):
    return 'CALENDAR' + ":" + ":".join([action,str(year),str(month),str(day)])

#Создание календаря для текущего месяца
def create_calendar(year=None,month=None):
    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    #First row - Month and Year
    row=[]
    row.append(InlineKeyboardButton(calendar.month_name[month]+" "+str(year),callback_data=data_ignore))
    keyboard.append(row)
    #Second row - Week Days
    row=[]
    for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
        row.append(InlineKeyboardButton(day,callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(str(day),callback_data=create_callback_data("DAY",year,month,day)))
        keyboard.append(row)
    #Last row - Buttons
    row=[]
    row.append(InlineKeyboardButton("<",callback_data=create_callback_data("PREV-MONTH",year,month,day)))
    row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
    row.append(InlineKeyboardButton(">",callback_data=create_callback_data("NEXT-MONTH",year,month,day)))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)

#Обработка нажатия кнопок в календаре
def process_calendar_selection(update,bot):

    ret_data = (False,None)
    query = update
    # print(query)
    (_,action,year,month,day) = query.data.split(":")
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        bot.answer_callback_query(callback_query_id= query.id)
    elif action == "DAY":
        # bot.edit_message_text(text=query.message.text,
        #     chat_id=query.message.from_user.id,
        #     message_id=query.message.message_id
        #     )
        ret_data = True,datetime.datetime(int(year),int(month),int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.from_user.id,
            message_id=query.message.id,
            reply_markup=create_calendar(int(pre.year),int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.from_user.id,
            message_id=query.message.id,
            reply_markup=create_calendar(int(ne.year),int(ne.month)))
    else:
        bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data

#создание записи в календаре
def create_note(mess, user_id, date_orig, bot):
    try:
        time = mess.text[:mess.text.index(' ')]
        note = mess.text[mess.text.index(' ') + 1:]
        time = datetime.time(int(time[:2]), int(time[3:5]))
        date = date_orig.combine(date_orig.date(), time)
        if "notes" in users_d[user_id]:
            users_d[user_id]["notes"][date] = note
            update_users(users_d)
            queue_scheduler.append(date)
        else:
            users_d[user_id]["notes"] = {date:note}
            update_users(users_d)
        bot.send_message(user_id, f"Хорошо, напомню вам что в {date.time()}, {date.date()}\n Нужно:{note}")
    except Exception:
        bot.send_message(user_id, "Формат для дибилов?, пробуй еще раз")
        mess = bot.send_message(user_id, "Введите время в 24-ом формате HH:MM и задачу через пробел")
        bot.register_next_step_handler(mess, create_note, user_id, date_orig,bot)