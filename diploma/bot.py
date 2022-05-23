import telebot
from processors.recognition import get_info
from processors.image_preprocessor import filter_noise
from processors.description_processor import get_description

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
        image_file = bot.get_file(message.photo[0].file_id)
        downloaded_image = bot.download_file(image_file.file_path)
        image_info = get_info(filter_noise(downloaded_image))

        if len(image_info) != 0 and image_info[0].score > 0.9:
            image_description = None

            current_result = 0
            while image_description is None and image_info[current_result].score >= 0.9:
                image_description = get_description(image_info[current_result].description)

            if image_description is not None:
                bot.send_message(user_id, image_description)
                return

        bot.send_message(user_id, "Please, take a better picture of an art")
