from telegram.ext import BaseFilter, CommandHandler, MessageHandler, Updater
from sedlaif_bot.config import Config
import logging

TOKEN = Config.API_KEY
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


# custom class to filter messages for echo handler
class EchoFilter(BaseFilter):
    def filter(self, message):
        split = message.text.split('/')
        return split[0] == 'e'


# callback function for respective handlers
def start_callback(bot, update):
    if update.message.chat.type == "private":
        bot.send_message(chat_id=update.message.chat_id, text="Hi there")

def echo_callback(bot, update):
    split = update.message.text.split('/')
    reply = split[1]
    bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

    # if message is not a reply, simply echo the text
    if is_reply(update) is False:
            bot.send_message(chat_id=update.message.chat_id, text=reply)

    # if it is a reply, echo to the replied message
    else:
        replied_message_id = is_reply(update)[1]
        bot.send_message(chat_id=update.message.chat_id, text=reply, reply_to_message_id=replied_message_id)


# checks if message is a reply to another message
def is_reply(update):
    if(update.message.reply_to_message is not None):
        replied_message=update.message.reply_to_message.text
        replied_message_id=update.message.reply_to_message.message_id
        return [replied_message,replied_message_id]
    else:
        return False

echo_filter = EchoFilter()

start_handler = CommandHandler('start', start_callback)
echo_handler = MessageHandler(echo_filter, echo_callback)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()