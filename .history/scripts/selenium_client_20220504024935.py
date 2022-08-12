'''
Клиент `Selenium`, выбирает самую активную трансляцию и сохраняет её чат и
снимок экрана.

1) Заходит на vk.com.
2) Переходит в live-трансляции.
3) Выбирает открывает трансляцию, идующую первой (наиболее популярную).
4) Раз в минуту обновляет снимок экрана и сохраняет в файл новые поступившие 
сообщения в чат.
'''
from selenium import webdriver
from pathlib import Path
from tempfile import gettempdir


class _VkSeleniumClientPipeline:
    @staticmethod
    def _get_user_data_dir():
        return f'{gettempdir()}/'

    def _open_chrome(self):
        '''
        Открытие браузера.
        '''
        cur_dir = Path(__file__).parent.resolve()
        self._driver = webdriver.Chrome(f'{cur_dir}/../data/chromedriver')
        options = webdriver.ChromeOptions() 
        options.add_argument("user-data-dir=C:\\Path") #Path to your chrome profile


    def run(self):
        '''
        Вызов всех функций - одна за одной.
        '''
        self._init_chrome()
        self._login()
        self._goto_live_broadcasts()
        self._open_broadcast()
        self._save_results()            


if __name__ == '__main__':
    # Точка входа.
    _VkSeleniumClientPipeline().run()