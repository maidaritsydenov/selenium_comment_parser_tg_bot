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

    def _get_wait_presense_func(self, wait_selector, secs_wait):
        def get_presense_inner():
            WebDriverWait(self._driver, secs_wait).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, wait_selector)
                )
            )
        return get_presense_inner

    def _get_wait_title_func(self, wait_title_contains, secs_wait):
        def get_wait_title_inner():
            WebDriverWait(self._driver, secs_wait).until(
                EC.title_contains(wait_title_contains)
            )
        return get_wait_title_inner

    def _click_and_wait(
            self,             
            clk_selector,
            secs_wait,
            *,
            if_selector=None,
            wait_selector=None, 
            wait_title_contains=None):
        '''
        Нажимаем на селектор и ждём появление другого селектора
        '''
        if if_selector is None \
                or self._driver.find_elements_by_css_selector(if_selector):
            # Ждём, когда можно будет кликнуть
            wait_click_func = \
                self._get_wait_presense_func(clk_selector, secs_wait)
            wait_click_func()
            # Кликаем.
            self._driver.find_element_by_css_selector(clk_selector).click()
            # Ждём, пока целевой элемент не появится на странице
            wait_event_func = \
                self._get_wait_presense_func(wait_selector, secs_wait) \
                    if wait_title_contains is None \
                    else \
                        self._get_wait_title_func(
                            wait_title_contains, 
                            secs_wait
                        )            
            wait_event_func()

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
