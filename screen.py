from tkinter import *
from typed_word import TypedWord
from text_to_type import TypeTest
import time

TEXTBOX_FONT = ("arial", 30, "bold")
ENTRY_BOX_FONT = ("arial", 20, "bold")
# time in seconds
TIME = 100
# to track user typed words
user_words = TypedWord()

# the text to type
type_test = TypeTest()


class App(Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Type Test')

        # displays the time
        self.time_label = Label(self, text=f"Time Left : {TIME}")
        self.time_label.pack()

        self.cpm = Label(self, text="CPM : 00")
        self.cpm.pack()

        self.correct_cpm = Label(self, text="Corrected CPM : 00")
        self.correct_cpm.pack()

        # the text box displays the text to be typed
        self.text_box = Text(self, width=30, height=2, font=TEXTBOX_FONT, wrap=WORD, padx=50, pady=50)
        self.configure_text()
        self.text_box.pack()

        # variable the tracks the cursor location
        self.character_index = 0

        # display the text to type in the text box
        self.display_text()

        # the entry box the user can type
        char = self.register(self.avoid_space)
        self.entry_box = Entry(self, font=ENTRY_BOX_FONT, validate="key", validatecommand=(char, '%P'),)
        self.entry_box.pack()

        # the user can restart typying using the restart button the button will reset everything to start again
        self.restart = Button(text="Restart", command=self.restart_typing, state="disabled")
        self.restart.pack()

        # the word in entry tracks the character in entered in the entry box
        self.word_in_entry = ""

        # all keys are bind to the function key_press
        self.key = self.entry_box.bind("<KeyRelease>", self.key_press)

        # to track state of timer
        self.timer_on = False

        # timer id
        self.timer = None

    def configure_text(self):
        """function to configure text style """

        # tag to highlight the current word to type
        self.text_box.tag_configure("current_word", background="green", foreground="white")

        # after navigating to next word
        # if the previous word is typed correct
        self.text_box.tag_configure("correct_word", background="white", foreground="green")
        # if the previous word is typed wrong
        self.text_box.tag_configure("incorrect_word", background="white", foreground="red")

        # if the letter is typed wrong
        self.text_box.tag_configure("letter_wrong", background="green", foreground="red")
        # if letter is typped correct
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

        if not self.timer_on:
            self.start_timer()

        return True

    def key_press(self, event):
        """handles every key release in the keyboard"""

        # every time a key is pressed the word_in_entry is updated
        self.word_in_entry = self.entry_box.get().strip()

        # the tab and enter key is not accepted
        if event.char == "\t" or event.char == "\r":
            return

        # space key is accepted only the word_in_entry have at least a valid character
        # clears the entry box and set the word in entry to empty string
        elif self.word_in_entry and event.char == " ":
            user_words.push(word=self.word_in_entry)

            # adding the count of correctly typed characters typed
            user_words.corrected_character_count += self.update_text_box()
            print(f"wrong characters: {user_words.character_count - user_words.corrected_character_count}")

            self.clear_entry()
            self.next_word()

        # if the backspace key is triggered
        elif event.keysym == "BackSpace":

            self.back_space()

        # if valid char other than space
        elif event.char and event.char != " ":
            current_correct_letters = self.update_text_box()

            self.update_meters(current_correct_letters)

    def back_space(self):
        """function handles all the backspace trigger"""

        # if type_test.typed_word_length is None
        self.text_box.config(state="normal")

        # if the length is less than zero then the highlight must move to the previous word
        if type_test.typed_word_length <= 0:
            # navigate to the previous word
            self.previous_word()
            return

        # if the word in the entry box is correctly typed
        if self.entry_box.get().strip() == type_test.word_list[type_test.word_index]:

            self.text_box.delete(f"1.{self.character_index}",
                                 f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")

            self.text_box.insert(f"1.{self.character_index}",
                                 type_test.word_list[type_test.word_index], "letter_correct")

        else:
            self.text_box.delete(f"1.{self.character_index}",
                                 f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")

            self.text_box.insert(f"1.{self.character_index}",
                                 type_test.word_list[type_test.word_index], "current_word")
            self.update_text_box()

        # if the word in the entry box is not correct but with in the length of the correct word
        # elif len(self.entry_box.get().strip()) <= len(type_test.word_list[type_test.word_index]):
        #
        #     # update it as current word
        #     self.text_box.delete(f"1.{self.character_index}",
        #                          f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")
        #
        #     self.text_box.insert(f"1.{self.character_index}",
        #                          type_test.word_list[type_test.word_index], "current_word")
        #
        #     # the for loop is used to tackle the situation that the user may remove letters
        #     # inbetween using arrows and mouse
        #     # so a for loop can update the word every time a change is made
        #     # the for loop updates the correctly and wrongly typed letters in each backspace trigger
        #     for i in range(len(self.word_in_entry)):
        #         self.text_box.delete(f"1.{self.character_index + i}",
        #                              f"1.{self.character_index + i + 1}")
        #
        #         if self.word_in_entry[i] == type_test.word_list[type_test.word_index][i]:
        #             self.text_box.insert(f"1.{self.character_index + i}",
        #                                  type_test.word_list[type_test.word_index][i], "letter_correct")
        #
        #         else:
        #             self.text_box.insert(f"1.{self.character_index + i}",
        #                                  type_test.word_list[type_test.word_index][i], "letter_wrong")

        self.text_box.config(state="disabled")

        # update the length of the characters in the entry box
        type_test.typed_word_length = len(self.word_in_entry)

        # update the measuring values
        self.update_meters()

    def previous_word(self):
        """navigates to the previous word"""
        if user_words.peek():
            # remove the highlight from the current word
            self.text_box.delete(f"1.{self.character_index}",
                                 f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")

            self.text_box.insert(f"1.{self.character_index}",
                                 type_test.word_list[type_test.word_index])

            # update the word index by subtracting 1 so that it  points to the previous word
            type_test.word_index -= 1

            # update the character index to the beginning of the previous word
            self.character_index = self.character_index - len(type_test.word_list[type_test.word_index]) - 1

            # clear any entries in the entry box
            self.clear_entry()

            # pop the last completed word typed  from the user_words and display it in the entry box
            self.entry_box.insert(END, user_words.pop())

            # update the word in entry
            self.word_in_entry = self.entry_box.get()

            # # update the length of the characters in the entry box
            type_test.typed_word_length = len(self.word_in_entry)

            # delete the previous word and make it current
            self.text_box.delete(f"1.{self.character_index}",
                                 f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")

            # compare the word in entry with the original word and show indication on is it correct or not
            # the word is still active but already completed

            # if the word is correct
            if self.word_in_entry == type_test.word_list[type_test.word_index]:

                self.text_box.insert(f"1.{self.character_index}",
                                     type_test.word_list[type_test.word_index], "letter_correct")

                # remove the correctly typed character count
                user_words.corrected_character_count -= len(type_test.word_list[type_test.word_index])

            # this sets letters to current word
            # and then update text box is called to check the correction
            else:
                self.text_box.insert(f"1.{self.character_index}",
                                     type_test.word_list[type_test.word_index], "current_word")

                # remove the correctly typed character count
                user_words.corrected_character_count -= self.update_text_box()
                # self.update_text_box()

    def next_word(self):
        """navigates to the next word and also check the previous word is correctly typed or not"""
        self.text_box.config(state="normal")

        # delete the current word
        self.text_box.delete(f"1.{self.character_index}",
                             f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")

        # checks the entered word is correct or wrong and update the text box with indication
        if self.word_in_entry == type_test.word_list[type_test.word_index]:

            self.text_box.insert(f"1.{self.character_index}",
                                 type_test.word_list[type_test.word_index], "correct_word")

            # counting and saving  the number of correctly typed characters

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
        # as this condition is triggered in the time count method this is no more needed
        else:
            self.stop_typing()

        # this code helps when the user navigate to next word and did not start typing
        # and decided to navigate to previous word
        # this becomes irrelevant when the user started typing the next word
        type_test.typed_word_length = -1

        self.text_box.config(state="disabled")

        # scroll to next line is the visible part is over
        if not self.text_box.dlineinfo(f"1.{self.character_index}"):
            self.text_box.yview_scroll(1, "units")

    def update_text_box(self):
        """this function updated the letters of current word with the appropriate indicate correct wrong not typed the
        function return number of correct characters typed"""

        self.text_box.config(state="normal")

        # the length of the word in the entry box is updated in each click
        type_test.typed_word_length = len(self.word_in_entry)

        # check each letter is typed correct and give color indication
        # red for wrongly typed letter and yellow for correct
        correct_letter_count = 0
        for i in range(len(self.word_in_entry)):

            try:
                # check if i is valid index in the current word
                # if i is not a valid index then it gives  index error
                # the typed word is having length more than the correct word

                if type_test.word_list[type_test.word_index][i]:
                    self.text_box.delete(f"1.{self.character_index + i}",
                                         f"1.{self.character_index + i + 1}")

            except IndexError:
                # when the character count of typed word is more than the current word then update it with wrong
                self.text_box.delete(f"1.{self.character_index}",
                                     f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")

                self.text_box.insert(f"1.{self.character_index}",
                                     type_test.word_list[type_test.word_index], "letter_wrong")

                return correct_letter_count

            else:

                if self.word_in_entry[i] == type_test.word_list[type_test.word_index][i]:

                    self.text_box.insert(f"1.{self.character_index + i}",
                                         type_test.word_list[type_test.word_index][i], "letter_correct")

                    correct_letter_count += 1

                else:
                    self.text_box.insert(f"1.{self.character_index + i}",
                                         type_test.word_list[type_test.word_index][i], "letter_wrong")

        self.text_box.config(state="disabled")

        return correct_letter_count

    def update_meters(self, count=0):

        """function to update the measuring values"""

        # update character per minute

        self.cpm["text"] = "CPM : %02d" % (user_words.character_count+type_test.typed_word_length)
        self.correct_cpm["text"] = "corrected CPM : %02d" % user_words.corrected_character_count

    def clock_count(self, count):
        """the function keeps the time and check all the possible triggers to end typing test in each second"""

        # when the user completes typing  all the word given in the text box
        # the entry box will already be disabled and self.timer_on will be made falase
        if not self.timer_on:

            self.typing_test_end()

        # if the time reached the limit
        elif count <= 0:
            self.time_label["text"] = f"Time Left : 0{count}"
            self.stop_typing()

            self.typing_test_end()

        # update the count
        else:
            # self.time_label["text"] = f"Time : 0{count}"

            self.time_label["text"] = "Time Left : %02d" % count

            self.timer = self.after(1000, self.clock_count, count - 1)

    def start_timer(self):
        """start the timer"""
        # the timer is activated when the first valid character is typed in the
        if len(self.word_in_entry) < 1 and not self.timer_on:
            self.timer_on = True
            self.clock_count(TIME)
            self.restart.config(state="normal")
            # print("activate timer")

    def stop_typing(self):
        """stops the test stop accepting keys"""
        self.entry_box.config(state="disabled")
        self.entry_box.unbind("<Key>", self.key)
        self.timer_on = False

    def typing_test_end(self):
        """display the result"""
        pass

    def restart_typing(self):
        """the function will set to the default starting state of the test"""

        # make every thing to the default value so that the user can start from first
        self.timer_on = False

        # cancel the timer
        self.after_cancel(self.timer)

        self.character_index = 0
        self.word_in_entry = ""

        self.time_label.config(text=f"Time Left : {TIME}")
        self.cpm["text"] = "CPM : 00"
        user_words.make_empty()
        type_test.rest_default()

        self.text_box.config(state="normal")
        self.text_box.delete(0.0, END)
        self.display_text()

        self.entry_box.config(state="normal")
        self.key = self.entry_box.bind("<KeyRelease>", self.key_press)

        self.clear_entry()
