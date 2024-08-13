class WordTyped:
    def __init__(self):
        self.typed_stack = []

    def print_stack(self):
        for i in range(len(self.typed_stack) - 1, -1, -1):
            print(self.typed_stack[i])

    def is_empty(self):
        return len(self.typed_stack) == 0

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.typed_stack[-1]

    def size(self):
        return len(self.typed_stack)

    def push(self, value):
        self.typed_stack.append(value)

    def pop(self):
        if self.is_empty():
            return ""

        temp = self.typed_stack[-1]
        self.typed_stack.pop(-1)

        return temp
