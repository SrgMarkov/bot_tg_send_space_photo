import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()
telegram_token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=telegram_token)
print(bot.get_me())
bot.send_message(chat_id='@spacephotocollection', text="Bambaleilo!!!")