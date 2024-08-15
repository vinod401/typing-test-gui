
class TypeTest:
    def __init__(self):
        self.word_list = []
        self.word_index = 0
        self.typed_word_length = 0
        self.generated_text = None

        self.generate_text()

    def generate_text(self):
        """the function generates random multi-lined text from the text_bank """

        # for testing purpose
        self.generated_text = "The invention of Braille"

        self.word_list = self.generated_text.strip().split(" ")


