'''
Функция переключения на другой фрейм.
'''
from contextlib import contextmanager

@contextmanager
def switch_to_frame(driver, frame_selector):
    try:
        driver.switch_to.frame(
            driver.find_element_by_css_selector(frame_selector)
        )
    except:
        pass
    else:
        yield None
    finally:
        driver.switch_to.default_content()