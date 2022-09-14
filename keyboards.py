from telebot import types
from telebot.callback_data import CallbackData

menu_callback = CallbackData("button_name", prefix= "menu")
settings_callback = CallbackData("button_name", prefix = "settings")
note_callback = CallbackData("button_name", prefix = "notes")
game_callback = CallbackData("button_name", prefix = "games")

#основная клавиатура
markup_main = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
itembtn = types.KeyboardButton('Привет, Джарвис')
markup_main.add(itembtn)

#старт клавиатура
markup_start = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
itembtn = types.KeyboardButton('/start')
markup_start.add(itembtn)

#клавиатура под меню
markup_menu = types.InlineKeyboardMarkup(row_width=1)
itembtn1 = types.InlineKeyboardButton('☀️Че по погоде☁️', callback_data=menu_callback.new(button_name = "weather"))
itembtn2 = types.InlineKeyboardButton('⚙️Настройки⚙️', callback_data=menu_callback.new(button_name = "settings"))
itembtn3 = types.InlineKeyboardButton('📝Ежедневник📝', callback_data=menu_callback.new(button_name = "notebook"))
itembtn4 = types.InlineKeyboardButton('📝Расскажи мне что это📝', callback_data=menu_callback.new(button_name = "wiki"))
itembtn5 = types.InlineKeyboardButton('🎮Игры🎮', callback_data=menu_callback.new(button_name = "games"))
markup_menu.add(itembtn1)
markup_menu.add(itembtn2)
markup_menu.add(itembtn3)
markup_menu.add(itembtn4)
markup_menu.add(itembtn5)

#клавиатура под настройки
markup_settings = types.InlineKeyboardMarkup(row_width=1)
itembtn1 = types.InlineKeyboardButton('Редактировать профиль🖊', callback_data=settings_callback.new(button_name = "edit_profile"))
#itembtn2 = types.InlineKeyboardButton('Настройки', callback_data=menu_callback.new(button_name = "settings"))
markup_settings.add(itembtn1)

#клавиатура под заметки
markup_notebook = types.InlineKeyboardMarkup(row_width=1)
itembtn1 = types.InlineKeyboardButton('Мои дела📜', callback_data=note_callback.new(button_name = "my_notes"))
itembtn2 = types.InlineKeyboardButton('Создать заметку✏️', callback_data=note_callback.new(button_name = "create_note"))
markup_notebook.add(itembtn1)
markup_notebook.add(itembtn2)

markup_games = types.InlineKeyboardMarkup(row_width=1)
itembtn1 = types.InlineKeyboardButton('Монетка\U0001FA99', callback_data=game_callback.new(button_name = "coinflip"))
#itembtn2 = types.InlineKeyboardButton('Создать заметку✏️', callback_data=note_callback.new(button_name = "create_note"))
markup_games.add(itembtn1)
#markup_notebook.add(itembtn2)
