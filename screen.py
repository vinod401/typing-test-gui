from tkinter import *
from typed_word import TypedWord
from text_to_type import TypeTest

TEXTBOX_FONT = ("arial", 18, "bold")
ENTRY_BOX_FONT = ("arial", 15, "normal")

# to track user typed words
user_words = TypedWord()

# the text to type
type_test = TypeTest()


class App(Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Type Test')

        # the text box displays the text to be typed
        self.text_box = Text(self, height=4, font=TEXTBOX_FONT, wrap=WORD)
        self.configure_text()
        self.text_box.pack()

        # variable the tracks the cursor location
        self.character_index = 0

        self.display_text()

        # the entry box the user can type
        char = self.register(self.avoid_space)
        self.entry_box = Entry(self, font=ENTRY_BOX_FONT, validate="key", validatecommand=(char, '%P'))
        self.entry_box.pack()

        # the word in entry tracks the character in entered in the entry box
        self.word_in_entry = ""

        # all keys are bind to the function key_press
        self.key = self.entry_box.bind("<KeyRelease>", self.key_press)

    def configure_text(self):
        """function to configure text style """

        self.text_box.tag_configure("current_word", background="green", foreground="white")
        self.text_box.tag_configure("correct_word", background="white", foreground="green")
        self.text_box.tag_configure("incorrect_word", background="white", foreground="red")

        self.text_box.tag_configure("letter_wrong", background="green", foreground="red")
        self.text_box.tag_configure("letter_correct", background="green", foreground="yellow")

    def display_text(self):
        """this function displays the text to type in the text box"""
        self.text_box.insert(END, type_test.generated_text)

        self.text_box.delete(f"1.{self.character_index}",
                             f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")

        self.text_box.insert(f"1.{self.character_index}",
                             type_test.word_list[type_test.word_index], "current_word")

        self.text_box.config(state="disabled")


    def clear_entry(self):
        """function clears the entry box"""

        self.entry_box.delete(first=0, last=END)

    def avoid_space(self, input_char):
        """this function make sure that there is no blank space in front of the text in the entry box"""

        # the entry box won't accept a blank space in front of a word
        # each word should start with a valid character not blank space and no blank space is allowed inbetween word
        if " " in input_char:
            return False

        return True

    def key_press(self, event):

        # every time a key is pressed the word_in_entry is updated
        self.word_in_entry = self.entry_box.get().strip()

        # the tab and enter key is not accepted
        if event.char == "\t" or event.char == "\r":
            return

        # space key is accepted only the word_in_entry have at least a valid character
        # clears the entry box and set the word in entry to empty string
        elif self.word_in_entry and event.char == " ":
            print(self.word_in_entry)

            user_words.push(word=self.word_in_entry)
            self.clear_entry()
            user_words.print_stack()

        # if the backspace key is triggered
        elif event.keysym == "BackSpace":
            print("backspace")

        # if valid char other than space
        elif event.char and event.char != " ":
            self.update_text_box()

    def update_text_box(self):
        self.text_box.config(state="normal")
        print(self.word_in_entry)
        self.text_box.config(state="disabled")
