'''
Функция переключения на другой фрейм.
'''
from contextlib import contextmanager

@contextmanager
def switch_to_frame(driver, frame_id):
    try:
        self._driver.switch_to.frame('chatframe')