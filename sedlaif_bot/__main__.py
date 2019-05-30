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

class SedFilter(BaseFilter):
    def filter(self, message):
        split = message.text.split('/')
        return split[0] == 's' and len(split)>=3

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

def sed_callback(bot, update):
    split = update.message.text.split('/')
    bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

    replied_message = is_reply(update)[0]
    replied_message_id = is_reply(update)[1]
        
    if(len(split)%2==0):
        #s/*/*..g command
        if(split[-1]=="g"):
            reply = replied_message
            for word in range(1,len(split)-1,2):
                reply = reply.replace(split[word],split[word+1])
            bot.send_message(chat_id=update.message.chat_id, text=reply, reply_to_message_id=replied_message_id)
    else:
        #s/*/*.. command
        reply = replied_message
        for word in range(1,len(split),2):
            reply=reply.replace(split[word],split[word+1],1)
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
sed_filter = SedFilter()

start_handler = CommandHandler('start', start_callback)
echo_handler = MessageHandler(echo_filter, echo_callback)
sed_handler = MessageHandler(sed_filter, sed_callback)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(sed_handler)

updater.start_polling()
