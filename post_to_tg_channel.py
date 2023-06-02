import os
import argparse
import random
import time
from telegram import Bot
from dotenv import load_dotenv
from PIL import Image


UPLOAD_FILE_MAX_SIZE = 20000000
IMAGE_HEIGHT = 600
IMAGE_WIDTH = 800


def post_photo_to_tg(image, bot, chat):
    with open(image, 'rb') as photo_file:
        bot.send_photo(chat_id=chat, photo=photo_file)


def get_images_to_upload():
    image_path_pars = os.walk('images')
    photos_to_upload = []
    for address, directory, files in image_path_pars:
        images = files
        for image in images:
            if os.stat(f'images/{image}').st_size > UPLOAD_FILE_MAX_SIZE:
                image = Image.open(f'images/{image}')
                image.thumbnail((IMAGE_WIDTH, IMAGE_HEIGHT))
            photos_to_upload.append(image)
    return photos_to_upload


if __name__ == '__main__':
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
    telegram_bot = Bot(token=telegram_token)
    upload_time = os.getenv("TG_PUBLICATION_PERIOD", default=14400)
    photos_to_upload = get_images_to_upload()
    command_arguments = argparse.ArgumentParser \
        (description='Скрипт для выгрузки картинок в группу telegram. Можно выгрузить случайное фото или фото по имени '
                     'файла. Так же можно задать автопубликацию через каждые "PUBLICATION_TIME" секунд (из переменной '
                     'окружения), по умолчанию - 14400(4 часа)')
    command_arguments.add_argument('-p', '--photo', help='Имя файла')
    args = command_arguments.parse_args()
    if args.photo:
        post_photo_to_tg(f'images/{args.photo}', telegram_bot, chat_id)
    else:
        while True:
            for photo in photos_to_upload:
                post_photo_to_tg(f'images/{photo}', telegram_bot, chat_id)
                time.sleep(int(upload_time))
            random.shuffle(photos_to_upload)

