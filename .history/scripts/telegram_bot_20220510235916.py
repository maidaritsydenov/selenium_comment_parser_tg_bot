'''
Бот telegram.

1) 
'''

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TELEGRAM_TOKEN


class BotApp:
    @staticmethod
    def _get_filter_key(chat_id, user_id, phrase):
        return '%s-%s-' % (chat_id, user_id, phrase)

    def _callback_check_filters(self, bot, job_data):
        self._load_external_chat()
        char_id, user_id = job_data.context
        if 



    def _callback_start(self, bot, update, job_queue):
        bot.send_message(chat_id=update.message.chat_id, 'Welcome!')
        job_queue.run_repeating(
            self._callback_check_filters, 5, context=update.message.chat_id)


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