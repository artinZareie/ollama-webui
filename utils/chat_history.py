import json
from datetime import datetime

class ChatHistory:
    pass
    class ChatHistory:
        def __init__(self):
            self.history = []

        def add_message(self, sender, message):
            self.history.append({
                'timestamp': datetime.now().isoformat(),
                'sender': sender,
                'message': message
            })

        def get_messages(self):
            return self.history

        def get_message(self, index):
            if 0 <= index < len(self.history):
                return self.history[index]
            else:
                raise IndexError("Message index out of range")

        def update_message(self, index, sender=None, message=None):
            if 0 <= index < len(self.history):
                if sender:
                    self.history[index]['sender'] = sender
                if message:
                    self.history[index]['message'] = message
            else:
                raise IndexError("Message index out of range")

        def delete_message(self, index):
            if 0 <= index < len(self.history):
                del self.history[index]
            else:
                raise IndexError("Message index out of range")

        def to_json(self, filepath):
            with open(filepath, 'w') as f:
                json.dump(self.history, f, indent=4)

        def from_json(self, filepath):
            with open(filepath, 'r') as f:
                self.history = json.load(f)

        def to_gradio_format(self):
            return [{'text': msg['message'], 'is_user': msg['sender'] == 'user'} for msg in self.history]

        def to_ollama_format(self):
            return [{'role': 'user' if msg['sender'] == 'user' else 'assistant', 'content': msg['message']} for msg in self.history]
