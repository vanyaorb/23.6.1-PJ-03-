import telebot
from telebot import types
from config import TOKEN
from extensions import APIException, CurrencyConverter

# Экземпляр бота с использованием токена
bot = telebot.TeleBot(TOKEN)

# Обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Привет! Этот бот может помочь Вам узнать цену на определенное количество валюты. "
                                      "Для получения цены введите сообщение в формате: "
                                      "<имя валюты цену которой вы хотите узнать> "
                                      "<имя валюты, в которой надо узнать цену первой валюты> "
                                      "<количество первой валюты>\n"
                                      "Например: USD RUB 100\n"
                                      "Для просмотра доступных валют введите /values")

# Обработчик команды /values
@bot.message_handler(commands=['values'])
def handle_values(message):
    bot.send_message(message.chat.id, "Доступные валюты: USD (доллар США), EUR (евро), RUB (рубль РФ) и др.")

# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        base, quote, amount = message.text.split()
        result = CurrencyConverter.get_price(base, quote, amount)
        bot.send_message(message.chat.id, f"Цена {amount} {quote} в {base}: {result}")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат сообщения. Пожалуйста, введите сообщение в формате: "
                                          "<имя валюты> <имя валюты, в которой надо узнать цену первой валюты> "
                                          "<количество первой валюты>")
    except APIException as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

if __name__ == "__main__":
    bot.polling(none_stop=True)
