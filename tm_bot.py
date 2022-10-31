import telebot
from config import keys, TOKEN
from extensions import APIExeption, ConvertionExeption
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def bot_hello(message: telebot.types.Message):
    text='Здравствуйте,Я могу показать актуальные курсы валют, а также конвентировать любую сумму!\
\nЧтобы узнать курс валюты, введите команду:\n <имя валюты, цену которой вы хотите узнать>\
<в какую валюту перевести>\
<колличество переводимой валюты>\nЧтобы увидеть список валют введите: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text='Доступные валюты для перевода:'
    for key in keys.keys():
        text='\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
   try:
        values=message.text.split(' ')
        if len(values)!=3:
            raise ConvertionExeption('Неверное колличество параметров!')

        quote, base, amount = values
        total_base=APIExeption.get_price(base, quote, amount)
   except ConvertionExeption as e:
       bot.reply_to(message, f'Ой! Что-то пошло не так!\n{e}')
   except Exception as e:
       bot.reply_to(message, f'Не удалось обработать команду\n{e}')
   else:
        text = f'Стоимость {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()