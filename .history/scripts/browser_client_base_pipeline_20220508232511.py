'''
Базовый абстрактны класс браузера.
'''
from abc import ABCMeta, abstractmethod


class BrowserClientBasePipeline(meta=ABCMeta):
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

    @abstractmethod
    def _goto_page(self, url):
        '''
        Логику перехода на страницу - реализовать в отдельном методе.
        '''
        pass

    def _click_and_wait(self, clk_selector, wait_selector, secs_wait):
        '''
        Нажимаем на селектор и ждём появление другого селектора
        '''
        super().click_and_wait(clk_selector, wait_selector, secs_wait=10.0)
        self._driver.find_element_by_css_selector(clk_selector).click()
        WebdriverWait(self._driver, secs_wait).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, wait_selector)
            )
        )

    @abstractmethod
    def run(self):
        '''
        Основной метод пайплайна, который должен вызывать все остальные методы.
        '''
        pass