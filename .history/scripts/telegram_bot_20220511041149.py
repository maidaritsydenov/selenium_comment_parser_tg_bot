'''
Бот telegram.

1) 
'''
from collections import defaultdict
from queue import Queue
from time import sleep
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TELEGRAM_TOKEN, PHRASES_FILE_PATH, SCREEN_FILE_PATH


class BotApp:
    _JOB_INTERVAL = 5.0

    def __init__(self):
        self._filters_by_users = defaultdict(lambda: [])
        self._phrases_by_users = defaultdict(lambda: Queue())

    def _global_timer_add_users_phrases(self, job_context):
        # Прочитать файл
        # Заполнить очередь каждого пользователя - новыми строками из файла
        line = None
        with open(PHRASES_FILE_PATH, 'r') as f:
            while True:
                if line:
                    for chat_id in self._phrases_by_users.keys():
                        self._phrases_by_users[chat_id].put(line)
                    line = f.readline()
                else:
                    while not line:
                        sleep(self._JOB_INTERVAL)            
                        line = f.readline()
            

    def _pop_user_phrases(self, chat_id):
        # Обработать очередь пользователя
        # Выдать только те items, которые удовлетворяет 
        # self._filters_by_users
        # А всю очередь - очистить
        output_phrases = []
        user_queue = self._phrases_by_users[chat_id]
        user_filters = self._filters_by_users[chat_id]
        while not user_queue.empty():
            phrase = user_queue.get()            
            for user_filter in user_filters:
                if user_filter in phrase:
                    output_phrases.append(phrase)
        return output_phrases


    def _timer_check_filters(self, bot, job):
        chat_id = job.context
        found_phrases = self._pop_user_phrases(chat_id)
        for found_phrase in found_phrases:
            bot.send_message(chat_id=chat_id, text=found_phrase)
        if len(found_phrases) > 0:
            self._send_screen(bot, chat_id)

    def _callback_start(self, update, job_queue):
        update.message.reply_text('Welcome!')
        job_queue.run_repeating(
            self._timer_check_filters, 
            self._JOB_INTERVAL, 
            context=update.message.chat_id
        )

    def _callback_stop(self, update, job_queue):
        job_queue.stop()
        update.message.reply_text('Bye!')

    def _callback_add_filter(self, update, context):
        chat_id = update.message.chat_id
        command_arg = update.message.text
        import pdb; pdb.set_trace()
        self._filters_by_users[chat_id].append(command_arg)
        update.message.reply_text('Filter "%s" has been added.' % command_arg)

    def _callback_remove_filter(self, bot, update):
        chat_id = update.message.chat_id
        command_arg = update.message.text
        import pdb; pdb.set_trace()
        user_filter_list = self._filters_by_users[chat_id]
        if command_arg.is_digit():
            filter_num = int(command_arg)
        else:
            filter_num = user_filter_list.index(command_arg)
        del user_filter_list[filter_num]
        update.message.reply_text('Filter "%s" has been added.' % command_arg)

    def _callback_show_filters(self, bot, update):        
        user_filters = self._filters_by_users[chat_id]
        user_filters = ['%d. "%s"' % 
                            (i + 1, user_filter) \
                            for i, user_filter in enumerate(user_filters)]
        output_user_filters = '\n'.join(user_filters)
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text=output_user_filters)

    def _send_screen(self, bot, chat_id):
        bot.send_photo(chat_id, photo=open(SCREEN_FILE_PATH, 'rb'))

    def init(self):
        updater = Updater(TELEGRAM_TOKEN)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(
            CommandHandler("start", self._callback_start, pass_job_queue=True))
        dispatcher.add_handler(
            CommandHandler("stop", self._callback_stop, pass_job_queue=True))
        dispatcher.add_handler(
            CommandHandler("add", self._callback_add_filter))
        dispatcher.add_handler(
            CommandHandler("show", self._callback_show_filters))
        dispatcher.add_handler(
            CommandHandler("remove", self._callback_remove_filter))
        
        updater.job_queue.run_once(self._global_timer_add_users_phrases, when=0)

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    BotApp().init()