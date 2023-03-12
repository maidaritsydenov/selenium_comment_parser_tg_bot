'''
Клиент `Selenium`, выбирает самую активную трансляцию и сохраняет её чат и
снимок экрана.

1) Заходим на youtube.com.
2) Переходим в live-трансляции.
3) Выбираем первую трансляцию, (наиболее популярную).
4) Раз в минуту обновляем снимок экрана и сохраняет в файл новые поступившие
сообщения в чат.
'''
import os
from time import sleep
from pathlib import Path
from selenium import webdriver
from browser_client_base_pipeline import BrowserClientBasePipeline
from chat_messages_saver import ChatMessagesSaver
from settings import HOME_DIR


def _log_method(f):
    print('Starting: %s().' % f.__name__)
    return f


class _VkChromeClientPipeline(BrowserClientBasePipeline):
    _WAIT_SECS = 10.0

    def __init__(self, manual_open_main_broadcast):
        super().__init__()
        self._chat_messages_saver = None
        self._manual_open_main_broadcast = manual_open_main_broadcast

    @classmethod
    def _init_output_directories(cls):
        '''
        Создаём все директории, которые потребуются пайплайну.
        '''
        os.makedirs(cls._get_chrome_profile_data_dir(), exist_ok=True)
        os.makedirs(cls._get_result_data_dir(), exist_ok=True)

    def _init_browser_parameters(self, headless):
        '''
        Инициализация параметров браузера.
        '''
        self._chrome_options = webdriver.ChromeOptions()
        user_data_dir = self._get_chrome_profile_data_dir()
        self._chrome_options.add_argument(f'user-data-dir={user_data_dir}')
        self._chrome_options.add_argument('disable-extensions')
        self._chrome_options.add_argument('mute-audio')
        if headless:
            self._chrome_options.add_argument('headless')
        self._chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-automation']
        )
        self._chromedriver_path = (
            # "D:/Dev_local/chromedriver_win32/chromedriver"
            '{}/../chromedriver_win32/chromedriver.exe'.format(Path(__file__).parent.resolve())
        )

    @_log_method
    def _open_browser(self):
        '''
        Открытие браузера.
        '''
        self._driver = webdriver.Chrome(
            self._chromedriver_path,
            chrome_options=self._chrome_options
        )

    @_log_method
    def _goto_main_page(self):
        self._driver.get('https://youtube.com')

    @_log_method
    def _goto_live_broadcasts(self):
        '''
        Переместиться в трансляции.
        '''
        # self._click_and_wait(
        #     '#guide-button',
        #     if_selector='#guide-button:not([pressed="true"])',
        #     wait_selector='#guide-button[pressed="true"]'
        # )
        self._click_and_wait(
            'yt-icon-button[id="guide-button"][toggleable="true"]',
            wait_title_contains='Трансляции'
        )
        self._click_and_wait(
            'a[id="endpoint"][title="Трансляции"]',
            wait_title_contains='Трансляции'
        )

    @_log_method
    def _open_main_broadcast(self):
        '''
        Открыть главную трансляцию.
        '''
        if self._manual_open_main_broadcast:
            input('Откройте трансляцию вручную и нажмите <Enter>.')
        else:
            self._click_and_wait(
                'a[id="video-title"]',
                # Панель кнопок `Like` и т.п.
                wait_selector='#top-level-buttons-computed'
            )

    @_log_method
    def _save_results(self):
        '''
        Сохраняем результата, получаемые с `youtube.com`.
        '''
        self._save_screenshot()
        self._save_new_chat_messages()

    def _save_screenshot(self):
        self._driver.save_screenshot(
            os.path.join(self._get_result_data_dir(), 'screen.png')
        )

    def _save_new_chat_messages(self):
        if self._chat_messages_saver is None:
            self._chat_messages_saver = ChatMessagesSaver(
                os.path.join(self._get_result_data_dir(), 'messages.txt'),
                num_saved_last_messages=100
            )
            self._chat_messages_saver.load_messages()
        existing_messages = self._get_existing_chat_messages()
        self._chat_messages_saver.add_messages(existing_messages)

    def _get_existing_chat_messages(self):
        with self._switch_to_frame('#chatframe', self._WAIT_SECS):
            message_elements = \
                self._driver.find_elements('css selector', '#chat #message')
            message_texts = [x.get_attribute('innerText') \
                             for x in message_elements]
        return message_texts

    @classmethod
    def _sleep(cls):
        sleep(cls._WAIT_SECS)

    def _click_and_wait(
            self,
            clk_selector,
            wait_secs=_WAIT_SECS,
            *,
            if_selector=None,
            wait_selector=None,
            wait_title_contains=None):
        '''
        Нажимаем на селектор и ждём появление другого селектора
        '''
        super()._click_and_wait(
            clk_selector,
            wait_secs,
            if_selector=if_selector,
            wait_selector=wait_selector,
            wait_title_contains=wait_title_contains
        )

    @classmethod
    def _get_app_data_dir(cls):
        return '{}/.{}'.format(HOME_DIR, cls.__name__)

    @classmethod
    def _get_chrome_profile_data_dir(self):
        return '{}/chrome-profile'.format(self._get_app_data_dir())

    @classmethod
    def _get_result_data_dir(self):
        return '{}/saved'.format(self._get_app_data_dir())

    def run(self, headless):
        '''
        Вызов всех функций - одна за одной.
        '''
        self._init_output_directories()
        self._init_browser_parameters(headless)
        self._open_browser()
        self._goto_main_page()
        self._goto_live_broadcasts()
        self._open_main_broadcast()
        while True:
            self._save_results()
            self._sleep()


if __name__ == '__main__':
    # Точка входа.
    # Запускаем ютуб в невидимом режиме (Для VSC)
    _VkChromeClientPipeline(
        not (os.environ.get('manual_open_main_broadcast', False) is False)
    ).run(
        headless=not (os.environ.get('headless', False) is False)
    )
