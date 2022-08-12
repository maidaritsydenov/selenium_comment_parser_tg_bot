'''

'''

class ChatMessagesSaver:
    def __init__(self, save_path, num_saved_last_messages):
        self._save_path = save_path
        self._num_saved_last_messages = num_saved_last_messages
        self._messages_set = set([])

    def load_messages(self):
        with open(self._save_path, 'r') as f:
            for line in f:
                if line not in 
