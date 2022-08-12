'''
Бот telegram.

1) 
'''

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, 
from settings import TELEGRAM_TOKEN


class BotApp:
    def _callback_start(self, *args, **kwargs):
        


    def init(self):
        updater = Updater(TELEGRAM_TOKEN)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(
            CommandHandler("start", self._callback_start, pass_job_queue=True))
        dispatcher.add_handler(
            CommandHandler("stop", self._callback_stop, pass_job_queue=True))
        dispatcher.add_handler(
            CommandHandler("add-filter", self._callback_add_filter))
        dispatcher.add_handler(
            CommandHandler("show-filters", self._callback_show_filters))
        dispatcher.add_handler(
            CommandHandler("remove-filter", self._callback_remove_filter))
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    BotApp().init()