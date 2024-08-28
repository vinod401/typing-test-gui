class TypeTest:
    def __init__(self):
        self.word_list = []
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

        # for testing purpose
        self.generated_text = "the test string"

        # self.generated_text = ("The invention of Braille was a major turning point in the history of disability. "
        #                        "The writing system of raised dots used by visually impaired people was developed "
        #                        "by Louis Braille in nineteenth-century France. In a society that did not value "
        #                        "disabled people in general, blindness was particularly stigmatized, and lack of ")

        self.word_list = self.generated_text.strip().split(" ")

    def rest_default(self):

        self.word_index = 0
        self.typed_word_length = 0
        self.total_characters_typed = 0
        self.mistakes_typed = 0

        self.time = 0

