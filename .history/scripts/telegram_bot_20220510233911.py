'''
Бот telegram.

1) 
'''

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, 
from settings import TELEGRAM_TOKEN


class BotApp:
    def _start(self, *args, **kwargs):
        l = 4


    def init(self):
        updater = Updater(TELEGRAM_TOKEN)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self._start))
        dispatcher.add_handler(CommandHandler("addword", self._add_word))
        dispatcher.add_handler(CommandHandler("show-word", self._add_word))
        #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    BotApp().init()