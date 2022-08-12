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
    def _check_login(self):
        '''
        Проверка состояния залогинивания и залогинивание, если нужно
        '''
        pass

    @abstractmethod
    def run(self):
        '''
        Основной метод пайплайна, который должен вызывать все остальные методы.
        '''
        pass