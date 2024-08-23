class TypedWord:
    def __init__(self):
        # to track the words typed by the user
        self.typed_stack = []

        # to track the number of characters typed by the user
        self.character_count = 0

        self.corrected_character_count = 0

    def print_stack(self):
        print(self.typed_stack)

    def is_empty(self):
        return len(self.typed_stack) == 0

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.typed_stack[-1]

    def size(self):
        return len(self.typed_stack)

    def push(self, word):
        self.typed_stack.append(word)
        self.character_count += len(self.peek())

    def pop(self):
        if self.is_empty():
            return ""

        temp = self.typed_stack[-1]
        self.typed_stack.pop(-1)

        self.character_count -= len(temp)
        return temp

    def make_empty(self):
        while self.size():
            self.pop()

        self.corrected_character_count = 0

