'''
Клиент `Selenium`, выбирает самую активную трансляцию и сохраняет её чат и
снимок экрана.

1) Заходим на youtube.com.
2) Переходим в live-трансляции.
3) Выбираем первую трансляцию, (наиболее популярную).
4) Раз в минуту обновляем снимок экрана и сохраняет в файл новые поступившие 
сообщения в чат.
'''
from os import makedirs, environ, path
from time import sleep
import tempfile
from selenium import webdriver
from pathlib import Path
from tempfile import gettempdir
from browser_client_base_pipeline import BrowserClientBasePipeline
from switch_to_frame import switch_to_frame
from chat_messages_saver import ChatMessagesSaver


class _VkChromeClientPipeline(BrowserClientBasePipeline):
    def __init__(self):
        super().__init__()
        self._chat_messages_saver = None

    @classmethod
    def _init_output_directories(cls):
        '''
        Создаём все директории, которые потребуются пайплайну.
        '''        
        makedirs(cls._get_chrome_profile_data_dir(), exist_ok=True)
        makedirs(cls._get_saved_data_dir(), exist_ok=True)

    def _init_browser_parameters(self):
        '''
        Инициализация параметров браузера.
        '''
        self._chrome_options = webdriver.ChromeOptions()
        user_data_dir = self._get_chrome_profile_data_dir()
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
        self._save_screenshot()
        self._save_new_chat_messages()

    def _save_screenshot(self):
        self._driver.save_screenshot(
            path.join(tempfile.gettempdir(), 'result.png')
        )

    def _save_new_chat_messages(self):
        if self._chat_messages_saver is None:
            self._chat_messages_saver = ChatMessagesSaver()
        existing_messages = self._get_existing_chat_messages()
        self._chat_messages_saver.add_messages(existing_messages)

    def _get_existing_chat_messages(self):
        with switch_to_frame(self._driver, '#chatframe'):
            message_elements = \
                self._driver.find_elements_by_css_selector('#chat #message')
            message_texts = [x.get_attribute('innerText') \
                                for x in message_elements]
        return message_texts

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

    @classmethod
    def _get_chrome_profile_data_dir(self):
        return '{}/chrome-profile'.format(self._get_user_data_dir())

    @classmethod
    def _get_saved_data_dir(self):
        return f'{}/saved'.format(self._get_user_data_dir())

    def run(self):
        '''
        Вызов всех функций - одна за одной.
        '''
        self._init_output_directories()
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
