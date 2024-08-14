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

        # insert the generated text for the test in the text box
        self.text_box.insert(END, type_test.generated_text)

        # highlight the first word
        self.text_box.delete(f"1.{self.character_index}",
                             f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")

        self.text_box.insert(f"1.{self.character_index}",
                             type_test.word_list[type_test.word_index], "current_word")

        # disable text box to avoid unnecessary interactions
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
            user_words.push(word=self.word_in_entry)
            self.clear_entry()
            self.next_word()
            # user_words.print_stack()

        # if the backspace key is triggered
        elif event.keysym == "BackSpace":
            print("backspace")

        # if valid char other than space
        elif event.char and event.char != " ":
            self.update_text_box()

    def next_word(self):

        self.text_box.config(state="normal")

        # delete the current word
        self.text_box.delete(f"1.{self.character_index}",
                             f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")

        # checks the entered word is correct or wrong and update the text box with indication
        if self.word_in_entry == type_test.word_list[type_test.word_index]:

            self.text_box.insert(f"1.{self.character_index}",
                                 type_test.word_list[type_test.word_index], "correct_word")
        else:
            self.text_box.insert(f"1.{self.character_index}",
                                 type_test.word_list[type_test.word_index], "incorrect_word")

        # update the cursor position
        # add the length of the previous word
        self.character_index = self.character_index + len(type_test.word_list[type_test.word_index]) + 1

        # update the word index
        type_test.word_index += 1

        # check whether the words to type are over
        if type_test.word_index != len(type_test.word_list):

            # highlight the next word to type
            self.text_box.delete(f"1.{self.character_index}",
                                 f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")

            self.text_box.insert(f"1.{self.character_index}",
                                 type_test.word_list[type_test.word_index], "current_word")

        # if there is no more word to type disable the entry box and unbind the keys
        else:
            self.entry_box.config(state="disabled")
            self.entry_box.unbind("<Key>", self.key)

        self.text_box.config(state="disabled")

    def update_text_box(self):
        self.text_box.config(state="normal")

        # if the typed word have characters more than the original word it is considered as wrongly typed
        if len(self.word_in_entry) > len(type_test.word_list[type_test.word_index]):

            self.text_box.delete(f"1.{self.character_index}",
                                 f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")

            self.text_box.insert(f"1.{self.character_index}",
                                 type_test.word_list[type_test.word_index], "letter_wrong")
            return

        # check each letter if typed correct
        for i in range(len(self.word_in_entry)):
            self.text_box.delete(f"1.{self.character_index + i}",
                                 f"1.{self.character_index + i + 1}")

            if self.word_in_entry[i] == type_test.word_list[type_test.word_index][i]:

                self.text_box.insert(f"1.{self.character_index + i}",
                                     type_test.word_list[type_test.word_index][i], "letter_correct")
            else:
                self.text_box.insert(f"1.{self.character_index + i}",
                                     type_test.word_list[type_test.word_index][i], "letter_wrong")

        self.text_box.config(state="disabled")
