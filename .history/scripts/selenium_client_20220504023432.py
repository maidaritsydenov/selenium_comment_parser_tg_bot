'''
Клиент `Selenium`, выбирает самую активную трансляцию и сохраняет её чат и
снимок экрана.

1) Заходит на vk.com.
2) Переходит в live-трансляции.
3) Выбирает открывает трансляцию, идующую первой (наиболее популярную).
4) Раз в минуту обновляет снимок экрана и сохраняет в файл новые поступившие 
сообщения в чат.
'''

class VkSeleniumClientPipeline:
    def run():
        '''
        Точка входа. Вызов всех функций - одна за одной.
        '''
        try:
            self._open_browser()
            self._login()
            self._goto_live_broadcasts()
            self._open_broadcast()
            self._save_results()
        except:
            


if __name__ == '__main__':
