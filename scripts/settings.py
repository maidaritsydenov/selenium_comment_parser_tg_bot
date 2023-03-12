import os
from os.path import expanduser

HOME_DIR = expanduser("~")
CURDIR = os.path.abspath(os.curdir)


TELEGRAM_TOKEN = '6161827603:AAHIQSOmr5PIcGE4uWqqvxzPmvSN3yAiyoU'
_PATH_COMMON_PART = f'{HOME_DIR}/._VkChromeClientPipeline/saved'
PHRASES_FILE_PATH = f'{_PATH_COMMON_PART}/messages.txt'
SCREEN_FILE_PATH = f'{_PATH_COMMON_PART}/screen.png'
ALLOWED_USERS = ['maidaritsydenov']
