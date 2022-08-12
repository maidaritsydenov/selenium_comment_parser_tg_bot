'''
Бот telegram.

1) 
'''

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, 
from settings import TELEGRAM_TOKEN


class BotApp:
    def _start(self, *args, **kwargs):
        


    def init(self):
        updater = Updater(TELEGRAM_TOKEN)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self._start))
        dispatcher.add_handler(CommandHandler("stop", self._stop))
        dispatcher.add_handler(CommandHandler("add-filter", self._add_filter))
        dispatcher.add_handler(
            CommandHandler(
                "show-filters", 
                self._show_filters
            )
        )
        dispatcher.add_handler(
            CommandHandler(
                    "remove-filter-number",
                    self._remove_filter_number
            )
        )
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    BotApp().init()