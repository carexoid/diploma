import telebot
from processors.recognition import get_info
from processors.image_preprocessor import filter_noise
from processors.description_processor import get_search_results, get_full_info_by_id

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
        filtered_image = filter_noise(downloaded_image)
        image_info = get_info(filtered_image)

        def results_validator(image_info):
            return len(image_info) != 0 and image_info[0].score > 0.9;

        if not results_validator(image_info):
            # retry recognizing image
            image_info = get_info(filtered_image)

        if results_validator(image_info):
            found_images = []

            current_result = 0
            while len(found_images) == 0 and image_info[current_result].score >= 0.9:
                found_images = get_search_results(image_info[current_result].description)

            keyboard = telebot.types.InlineKeyboardMarkup()

            i = 0
            for image in found_images:
                i += 1
                keyboard.add(telebot.types.InlineKeyboardButton(text=i, callback_data=image.id))

            bot.send_media_group(
                user_id,
                list(map(lambda element: telebot.types.InputMediaPhoto(element.image), found_images)))
            bot.send_message(user_id, "Choose piece of art, that looks like one you just sent", reply_markup=keyboard)
        else:
            bot.send_message(user_id, "Please, take a better picture of an art")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.message.chat.id

    bot.send_message(user_id, get_full_info_by_id(call.data))
