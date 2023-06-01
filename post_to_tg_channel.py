import os
import argparse
import random
import time
from telegram import Bot
from dotenv import load_dotenv
from PIL import Image


def post_photo_to_tg(image, token, chat):
    bot = Bot(token=token)
    bot.send_photo(chat_id=chat, photo=open(image, 'rb'))


def get_images_to_upload():
    image_path_pars = os.walk('images')
    photos_to_upload = []
    for address, directory, files in image_path_pars:
        images = files
        for image in images:
            if os.stat(f'images/{image}').st_size > 20000000:
                image = Image.open(f'images/{image}')
                image.thumbnail((800, 600))
            photos_to_upload.append(image)
    return photos_to_upload


if __name__ == '__main__':
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
    upload_time = os.getenv("TG_PUBLICATION_PERIOD", default=14400)
    command_arguments = argparse.ArgumentParser \
        (description='Скрипт для выгрузки картинок в группу telegram. Можно выгрузить случайное фото или фото по имени '
                     'файла. Так же можно задать автопубликацию через каждые "PUBLICATION_TIME" секунд (из переменной '
                     'окружения), по умолчанию - 14400(4 часа)')
    command_arguments.add_argument('-p', '--photo', help='Имя файла', default=random.choice(get_images_to_upload()))
    command_arguments.add_argument('-su', '--start_upload', help='Запустить выгрузку фотографий', default=False)
    args = command_arguments.parse_args()
    if args.start_upload:
        photos_to_upload = get_images_to_upload()
        while True:
            for photo in photos_to_upload:
                post_photo_to_tg(f'images/{photo}', telegram_token, chat_id)
                time.sleep(int(upload_time))
            random.shuffle(photos_to_upload)
    else:
        post_photo_to_tg(f'images/{args.photo}', telegram_token, chat_id)
