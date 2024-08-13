from tkinter import *


class App(Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Type Test')

        self.text_box = Text()
        self.text_box.pack()

        self.entry_box = Entry()
        self.entry_box.pack()
