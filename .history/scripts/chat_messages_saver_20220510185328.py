'''

'''
from queue import Queue

class ChatMessagesSaver:
    def __init__(self, save_path, num_saved_last_messages):
        self._save_path = save_path
        self._num_saved_last_messages = num_saved_last_messages
        self._messages_set = set([])
        self._messages_queue = Queue(maxsize=num_saved_last_messages)

    def load_messages(self):
        with open(self._save_path, 'r') as f:
            for msg in f:
                self._add_local_message(msg)

    def add_messages(self, messages):
        for msg in messages:
            if self._add_local_message(msg):
                with open(self._save_path, 'a') as f:
                    f.write

    def _add_local_message(self, msg):
        message_added = False
        if msg not in self._messages_set:
            if self._messages_queue.full():
                self._messages_set.remove(self._messages_queue.get())
            self._messages_queue.put(msg)
            self._messages_set.add(msg)
            message_added = True
        return message_added
