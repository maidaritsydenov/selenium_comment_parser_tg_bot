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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebdriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        self._click_and_wait(
            'yt-formatted-string:contains("Трансляции")', 
            'yt-formatted-string[id="text"]'
        )

    def _open_main_broadcast(self):
        '''
        Открыть главную трансляцию.
        '''
        self._click_and_wait('a[id="video-title"]', 'div[id="primary_inner"]')

    def _go_to_page(self, url):
        '''
        Переход по `url`.
        '''
        self._driver.get(url)

    def _click_and_wait(self, clk_selector, wait_selector, secs_wait=10.0):
        '''
        Нажимаем на селектор и ждём появление другого селектора
        '''
        self._driver.find_element_by_css_selector(clk_selector).click()
        WebdriverWait(self._driver, secs_wait).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, wait_selector)
            )
        )

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
