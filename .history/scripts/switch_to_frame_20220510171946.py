'''
Функция переключения на другой фрейм.
'''
from contextlib import contextmanager

@contextmanager
def switch_to_frame(driver, frame_id):
    try:
        driver.switch_to.frame(frame_id)
    except:
        pass
    else:
        yield
    finally:
        driver.switch_to.default_content()