from telegram.ext import Updater, CommandHandler
from sedlaif_bot.config import Config
import logging

TOKEN = Config.API_KEY
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# callback function for start handler
def start(bot, update):
    if update.message.chat.type=="private":
        bot.send_message(chat_id=update.message.chat_id, text="Hi there")

start_handler = CommandHandler('start', start)

dispatcher.add_handler(start_handler)

updater.start_polling()