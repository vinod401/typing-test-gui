import json
import random
from typed_word import WordList

class TypeTest:
    def __init__(self):
        self.stack = WordList()
        self.word_list = self.stack.typed_stack

        self.word_index = 0

        # to track the characters typed for current word for every new word it starts with zero
        self.typed_word_length = 0

        # to track the time
        self.time = 0

        self.total_characters_typed = 0
        self.mistakes_typed = 0

        self.generated_text = None
        self.generate_text()

    def generate_text(self):
        """the function generates random multi-lined text from the text_bank """

        with open("typing_text.json") as file:
            data = json.load(file)

        index = str((random.randint(1, data["info"]["size"])))

        generated_text = data["data"][index]

        for word in generated_text.strip().split(" "):
            if word.strip():
                self.stack.push(word.strip())

    def rest_default(self):

        self.word_index = 0
        self.typed_word_length = 0
        self.total_characters_typed = 0

        self.mistakes_typed = 0

        self.time = 0


