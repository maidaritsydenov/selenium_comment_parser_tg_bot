'''
Класс, сохраняющий сообщения в файл.

Класс сохранения сообщений в файл (без повтора).
Повторяющиеся сообщения среди этих последних - не сохраняются.
Повтор отслеживается только для последних `num_saved_last_messages` сообщений.
'''
import os
from queue import Queue


class ChatMessagesSaver:
    def __init__(self, save_path, num_saved_last_messages):
        self._save_path = save_path
        self._num_saved_last_messages = num_saved_last_messages
        self._messages_set = set([])
        self._messages_queue = Queue(maxsize=num_saved_last_messages)

    def load_messages(self):
        if os.path.exists(self._save_path):
            with open(self._save_path, 'r') as f:
                for msg in f:
                    self._add_local_message(msg)

    def add_messages(self, messages):
        # Не менять кодировку, автоматом идет cp1251,
        # для того чтобы без ошибки сообщения отправлялись в tg
        # менять encoding='utf-8' не надо
        with open(self._save_path, 'a', encoding='UTF-8') as f:
            for msg in messages:
                if self._add_local_message(msg):
                    f.write('%s\n' % msg)

    def _add_local_message(self, msg):
        message_added = False
        if msg not in self._messages_set:
            if self._messages_queue.full():
                removed_first_message = self._messages_queue.get()
                self._messages_set.remove(removed_first_message)
            self._messages_queue.put(msg)
            self._messages_set.add(msg)
            message_added = True
        return message_added
