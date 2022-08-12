'''
Клиент `Selenium`, выбирает самую активную трансляцию и сохраняет её чат и
снимок экрана.

1) Заходим на youtube.com.
2) Переходим в live-трансляции.
3) Выбирает открывает трансляцию, идующую первой (наиболее популярную).
4) Раз в минуту обновляет снимок экрана и сохраняет в файл новые поступившие 
сообщения в чат.
'''
from os import makedirs, environ, path
from time import sleep
import tempfile
from selenium import webdriver
from pathlib import Path
from tempfile import gettempdir
from browser_client_base_pipeline import BrowserClientBasePipeline


class _VkChromeClientPipeline(BrowserClientBasePipeline):

    def _init_browser_parameters(self):
        '''
        Инициализация параметров браузера.
        '''
        self._chrome_options = webdriver.ChromeOptions()
        user_data_dir = self._get_user_data_dir()
        makedirs(user_data_dir, exist_ok=True)
        self._chrome_options.add_argument(f'user-data-dir={user_data_dir}')
        self._chrome_options.add_argument('disable-extensions')
        self._chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-automation']
        )
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

    def _goto_main_page(self):
        self._driver.get('https://youtube.com')

    def _goto_live_broadcasts(self):
        '''
        Переместиться в трансляции.
        '''
        self._click_and_wait(
            '#guide-button',
            if_selector='#guide-button[pressed="false"]',
            wait_selector='#guide-button[pressed="true"]'
        )
        self._click_and_wait(
            'a[id="endpoint"][title="Live"]', 
            wait_title_contains='Live'
        )

    def _open_main_broadcast(self):
        '''
        Открыть главную трансляцию.
        '''
        self._click_and_wait(
            'a[id="video-title"]', 
            # Панель кнопок `Like` и т.п.
            wait_selector='#top-level-buttons-computed'
        )

    def _save_results(self):
        '''
        Сохраняем результата, получаемые с `youtube.com`.
        '''
        self._driver.save_screenshot(
            path.join(tempfile.gettempdir(), 'result.png')
        )

    @staticmethod
    def _sleep():
        sleep(10.0)


    def _click_and_wait(
            self, 
            clk_selector,
            secs_wait=10.0,
            *,
            if_selector=None,
            wait_selector=None,
            wait_title_contains=None):
        '''
        Нажимаем на селектор и ждём появление другого селектора
        '''
        super()._click_and_wait(
            clk_selector,
            secs_wait,
            if_selector=if_selector,
            wait_selector=wait_selector,
            wait_title_contains=wait_title_contains
        )

    @classmethod
    def _get_user_data_dir(cls):
        return f'{gettempdir()}/.{cls.__name__}'

    def run(self):
        '''
        Вызов всех функций - одна за одной.
        '''
        self._init_browser_parameters()
        self._open_browser()
        self._goto_main_page()
        self._goto_live_broadcasts()
        self._open_main_broadcast()
        while True:
            self._save_results()
            self._sleep()


if __name__ == '__main__':
    # Точка входа.
    _VkChromeClientPipeline().run()
