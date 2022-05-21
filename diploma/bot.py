import telebot

from setup import telegram_token

bot = telebot.TeleBot(telegram_token)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.from_user.id,
        "Hi, I am Art Recognition Bot! "
        "I will help you find information about an art object! "
        "Just send me the photo of it")


@bot.message_handler(content_types=["photo"])
def process_photo(message):
    bot.send_message(
        message.from_user.id,
        "Processing your picture...")
