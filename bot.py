import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 
        "Принял. Сначала диагностика 1000₽, потом решим по протоколу.\n\n"
        "Напиши:\n1. Имя\n2. Проблему\n3. Точку Б"
    )

@bot.message_handler(func=lambda m: True)
def echo_message(message):
    bot.send_message(message.chat.id, "✅ Принял сообщение. Диагностика 1000₽ — готов к созвону?")

print("Бот запущен.")
bot.infinity_polling()
