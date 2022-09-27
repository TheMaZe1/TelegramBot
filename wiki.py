import wikipedia

from loader import bot

wikipedia.set_lang("ru")

def get_info(mess):
    req = mess.text
    try:
        page = wikipedia.page(req)
        m = page.summary
    except wikipedia.exceptions.DisambiguationError as error:
        page = wikipedia.page(error.options[0])
        m = page.summary
    except Exception as ex:
        m = "Упс, ничего не найдено по вашему запросу"
    bot.send_message(mess.from_user.id, m)