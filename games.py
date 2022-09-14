import random
import time


def coinflip(bot,call):
    mes = bot.send_animation(call.from_user.id,
                             "https://psv4.userapi.com/c235131/u183029942/docs/d47/e70286ea591e/coin-flip.gif?extra=1RBCM3i-Kvkjt9oY8mfwfw_4F8SGyJsxrJWOYD-PuV4y7TrtqudKnimvI8meZQzPMn5UxSDDXKqPyeaw0s5MfTTN2FhEeB4nVfB58sTy2wyMrsoyxuWSLMbcDmFg57UeHTkM0c1BhExTyC_HKtOUeJA")
    time.sleep(5)
    bot.delete_message(call.from_user.id, mes.id)
    coin = random.randint(0,1)
    if coin==1:
        bot.send_message(call.from_user.id,"Результат: Орел")
    else:
        bot.send_message(call.from_user.id, "Результат: Решка")