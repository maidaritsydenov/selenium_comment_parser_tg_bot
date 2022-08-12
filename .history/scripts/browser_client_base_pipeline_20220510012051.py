'''
Базовый абстрактны класс браузера.
'''
from abc import ABCMeta, ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BrowserClientBasePipeline(ABC):
    def __init__(self):
        self._driver = None

    def __del__(self):
        if self._driver is not None:
            self._driver.quit()

    @abstractmethod
    def _init_browser_parameters(self):
        '''
        Инициализация параметров браузера.
        '''
        pass

    @abstractmethod
    def _open_browser(self):
        '''
        Открытие браузера.
        '''
        pass

    def _click_and_wait(
            self, clk_selector, wait_selector, secs_wait):
        '''
        Нажимаем на селектор и ждём появление другого селектора
        '''
        self._driver.find_element_by_css_selector(clk_selector).click()
        WebDriverWait(self._driver, secs_wait).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, wait_selector)
            )
        )

    def _go_to_page(self, url):
        '''
        Переход по `url`.
        '''
        self._driver.get(url)

    @abstractmethod
    def run(self):
        '''
        Основной метод пайплайна, который должен вызывать все остальные методы.
        '''
        pass
