import os
import random
from telegram import Bot, InputMediaPhoto
from dotenv import load_dotenv

load_dotenv()
telegram_token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=telegram_token)

dir = 'images'
random_photo = os.path.join(dir, random.choice(os.listdir(dir)))
upload_photo = InputMediaPhoto(media=open(f'{random_photo}', 'rb'))
bot.send_media_group(chat_id='@spacephotocollection', media=[upload_photo])
