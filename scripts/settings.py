# import os
from os.path import expanduser

HOME_DIR = expanduser("~")

TELEGRAM_TOKEN = 'Enter Telegram Token'
_PATH_COMMON_PART = f'{HOME_DIR}/._VkChromeClientPipeline/saved'
PHRASES_FILE_PATH = f'{_PATH_COMMON_PART}/messages.txt'
SCREEN_FILE_PATH = f'{_PATH_COMMON_PART}/screen.png'
ALLOWED_USERS = ['maidaritsydenov']
