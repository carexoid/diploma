import telebot
from processors.recognition import get_info

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
    user_id = message.from_user.id

    bot.send_message(
        user_id,
        "Processing your picture...")

    if len(message.photo) != 0:
        image_info = bot.get_file(message.photo[0].file_id)
        downloaded_image = bot.download_file(image_info.file_path)
        print(downloaded_image) # TODO: remove
        bot.send_message(
            user_id,
            get_info(downloaded_image)[0].description)
