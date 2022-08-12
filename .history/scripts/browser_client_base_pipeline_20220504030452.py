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

    def _open_browser(self):
        '''
        Открытие браузера.
        '''
        pass

    def _login(self):
        '''
        Залогинивание на целевой сайт.
        '''
        
