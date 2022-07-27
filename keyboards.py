from telebot import types
from telebot.callback_data import CallbackData

menu_callback = CallbackData("button_name", prefix= "menu")
settings_callback = CallbackData("button_name", prefix = "settings")

#основная клавиатура
markup_main = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
itembtn = types.KeyboardButton('Привет, Дима')
markup_main.add(itembtn)

#старт клавиатура
markup_start = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
itembtn = types.KeyboardButton('/start')
markup_start.add(itembtn)

#клавиатура под меню
markup_menu = types.InlineKeyboardMarkup(row_width=1)
itembtn1 = types.InlineKeyboardButton('Че по погоде', callback_data=menu_callback.new(button_name = "weather"))
itembtn2 = types.InlineKeyboardButton('Настройки', callback_data=menu_callback.new(button_name = "settings"))
itembtn3 = types.InlineKeyboardButton('Записать задачу', callback_data=menu_callback.new(button_name = "notebook"))
markup_menu.add(itembtn1)
markup_menu.add(itembtn2)
markup_menu.add(itembtn3)

#клавиатура под настройки
markup_settings = types.InlineKeyboardMarkup(row_width=1)
itembtn1 = types.InlineKeyboardButton('Редактировать профиль', callback_data=settings_callback.new(button_name = "edit_profile"))
#itembtn2 = types.InlineKeyboardButton('Настройки', callback_data=menu_callback.new(button_name = "settings"))
markup_settings.add(itembtn1)
