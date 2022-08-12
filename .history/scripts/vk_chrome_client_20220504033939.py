'''
Клиент `Selenium`, выбирает самую активную трансляцию и сохраняет её чат и
снимок экрана.

1) Заходит на vk.com.
2) Переходит в live-трансляции.
3) Выбирает открывает трансляцию, идующую первой (наиболее популярную).
4) Раз в минуту обновляет снимок экрана и сохраняет в файл новые поступившие 
сообщения в чат.
'''
from os import makedirs, environ
from selenium import webdriver
from pathlib import Path
from tempfile import gettempdir
from browser_client_base_pipeline import BrowserClientBasePipeline


class _VkChromeClientPipeline(BrowserClientBasePipeline):
    @classmethod
    def _get_user_data_dir(cls):
        return f'{gettempdir()}/.{cls.__name__}'

    def _init_browser_parameters(self):
        '''
        Инициализация параметров браузера.
        '''
        self._chrome_options = webdriver.ChromeOptions()
        user_data_dir = self._get_user_data_dir()
        makedirs(user_data_dir, exist_ok=True)
        self._chrome_options.add_argument(f'user-data-dir={user_data_dir}')
        self._chromedriver_path = (
            '{}/../data/chromedriver'.format(Path(__file__).parent.resolve())
        )
        

    def _open_browser(self):
        '''
        Открытие браузера.
        '''
        self._driver = webdriver.Chrome(
            self._chromedriver_path, 
            chrome_options=self._chrome_options
        )

    def _goto_live_broadcasts(self):
        '''
        Переместиться в трансляции.
        '''
        live_broadcast_url = self._find_live_broadcast_selector()
        self._click_and_wait(live_broadcast_url)

    def _find_live_broadcast_link(self):
        '''
        Найти на странице ссылку на live-трансляции.
        '''
        pass

    def _go_to_page(self, url):
        '''
        Переход в `url`.
        '''
        self._driver.get(url)

    def run(self):
        '''
        Вызов всех функций - одна за одной.
        '''
        self._init_browser_parameters()
        self._open_browser()
        self._goto_live_broadcasts()
        self._open_main_broadcast()
        while True:
            self._save_results()
            self._sleep()


if __name__ == '__main__':
    # Точка входа.
    _VkChromeClientPipeline().run()
