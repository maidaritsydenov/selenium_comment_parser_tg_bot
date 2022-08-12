'''
Бот telegram.

1) 
'''

from settings import TELEGRAM_TOKEN


class BotApp:


updater = Updater("5398930017:AAGzaYfcZhulbTm1-nONyBcqhhJUHGBwzxo")
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
updater.start_polling()
updater.idle()