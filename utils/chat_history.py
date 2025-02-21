import json

class ChatHistory:
    def __init__(self):
        self.history_list = []
        self.history_dict = []

    def append_user_message(self, message):
        self.history_list.append((message, None))
        self.history_dict.append({'role': 'user', 'content': message})

    def append_assistant_message(self, message):
        self.history_list[-1] = (self.history_list[-1][0], message)
        self.history_dict.append({'role': 'assistant', 'content': message})

    def get_list(self):
        return self.history_list

    def get_dict(self):
        return self.history_dict
    
    def clear(self):
        self.history_list.clear()
        self.history_dict.clear()

    def to_json(self):
        return json.dumps(self.history_dict, indent=4)

    def save(self, file):
        with open(file, 'w') as f:
            json.dump(self.history_dict, f, indent=4)

    def load(self, file):
        with open(file, 'r') as f:
            self.history_dict = json.load(f)
            self.history_list = [(entry['content'], None) 
                                 if entry['role'] == 'user' else (self.history_list[-1][0], entry['content']) 
                                 for entry in self.history_dict]