import telebot
from config import *
from extensions import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты, цену которой Вам надо узнать> \
 <имя валюты, в которой надо узнать цену первой валюты> \
 <количество первой валюты>;\n *ПРИМЕР <рубль доллар 100>*\n Увидеть список всех доступных  валют: \n /values "
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = "\n".join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    global base, sym, amount
    try:
        base, sym, amount = message.text.split(' ')
    except ValueError as e:
        bot.reply_to(message, "Неверное количество вводимых параметров")
    try:
        new_price = Convertor.get_price(base, sym, amount)
        bot.reply_to(message, new_price)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")


bot.polling()
