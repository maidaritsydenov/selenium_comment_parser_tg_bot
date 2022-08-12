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
    def _move_to_login_state(self):
        '''
        Залогинивание - любым способом на усмотрение пользователя класса.
        '''
        pass

    @abstractmethod
    def run(self):
        '''
        Основной метод пайплайна, который должен вызывать все остальные методы.
        '''
        pass