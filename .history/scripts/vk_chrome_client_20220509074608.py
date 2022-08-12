'''
Клиент `Selenium`, выбирает самую активную трансляцию и сохраняет её чат и
снимок экрана.

1) Заходит на vk.com.
2) Переходит в live-трансляции.
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
        self._chrome_options.add_argument('disable-features=InfiniteSessionRestore')
        #self._chrome_options.add_argument('no-startup-window')
        self._chrome_options.add_experimental_option(
            'excludeSwitches',
            ['load-extension', 'enable-automation']
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
            'yt-formatted-string[title="Live"]', 
            'div.badge-style-type-live-now'
        )

    def _open_main_broadcast(self):
        '''
        Открыть главную трансляцию.
        '''
        self._click_and_wait('a[id="video-title"]', 'div[id="primary_inner"]')

    def _save_results(self):
        '''
        Сохраняем результата, получаемые с `youtube.com`.
        '''
        self._driver.save_screenshot(
            path.join(tempfile.gettempdir(), 'result.png')
        )

    def sleep(self):
        sleep(10.0)


    def _click_and_wait(self, clk_selector, wait_selector, secs_wait=10.0):
        '''
        Нажимаем на селектор и ждём появление другого селектора
        '''
        super()._click_and_wait(
            clk_selector, 
            wait_selector, 
            secs_wait=secs_wait
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
