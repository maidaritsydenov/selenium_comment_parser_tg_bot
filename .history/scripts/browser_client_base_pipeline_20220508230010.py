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

    @abstractmethod
    def _click_and_wait(self, clk_selector, wait_selector):
        '''
        Нажимаем на селектор и ждём появление другого селектора
        '''

    @abstractmethod
    def run(self):
        '''
        Основной метод пайплайна, который должен вызывать все остальные методы.
        '''
        pass