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
            for line in f:
                if line not in self._messages_set:
                    if self._messages_queue.full():
                        self._messages_set.remove(self._messages_queue.get())
                    self._messages_queue.put(line)
                    self._messages_set.add(line)

    def _add_local_message(self, msg):
        if line not in self._messages_set:
                    if self._messages_queue.full():
                        self._messages_set.remove(self._messages_queue.get())
                    self._messages_queue.put(line)
                    self._messages_set.add(line)
