import json
import random

class WordManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, "r") as data_file:
                return json.load(data_file)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=1)

    def get_next_word(self):
        while True:
            next_word = random.choice(list(self.data))
            repeats_number = self.data[next_word][1]
            if repeats_number > 0:
                return next_word, repeats_number

    def update_word_count(self, word, sign="+"):
        if sign=="+":
            self.data[word][1] += 1
        else:
            self.data[word][1] -= 1

        self.save_data()

    def add_word(self, spanish_word, english_word, repeat_count):
        new_word = {spanish_word: [english_word, repeat_count]}
        self.data.update(new_word)
        self.save_data()

    def get_english_translation(self, spanish_word):
        return self.data[spanish_word][0]

    def get_spanish_translation(self, english_word):
        keys = []
        for key, value in self.data.items():
            if value[0] == english_word:
                keys.append(key)
        return keys[0] if keys else ""
