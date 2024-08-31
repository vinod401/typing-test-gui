import random
from tkinter import *
from typed_word import TypedWord
from text_to_type import TypeTest

# test window constants
TEXTBOX_FONT = ("arial", 30, "bold")
ENTRY_BOX_FONT = ("arial", 20, "bold")

TIME_MAX = 60
FONT = ("arial", 12, "bold")
BUTTON_FONT = ("arial", 10, "bold")
COLOR = "gray"

# result window
TEXT_COLOR = "#FFF4BD"
TEXT_FONT = ("arial", 20, "bold")
ACCURACY_FONT = ("arial", 22, "bold")

GOOD = "#39B54A"
AVERAGE = "#90CC50"
BAD = "#D34C4C"


class WelcomeWindow(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Welcome")

        self.bg = PhotoImage(file="image_resource/Welcome-01.png")
        self.canvas = Canvas(self.master, width=800, height=520)
        self.canvas.place(x=0, y=0)

        self.canvas.create_image(400, 260, image=self.bg)

        start_button = Button(self.master, text="Start", command=self.go_to_test_page, font=BUTTON_FONT,
                              foreground="white", background=AVERAGE, pady=10, padx=10)
        start_button.place(x=200, y=400)

        exit_button = Button(self.master, text="Exit", command=self.quit, font=BUTTON_FONT,
                             foreground="white", background=BAD, pady=10, padx=10)
        exit_button.place(x=600, y=400)

    def go_to_test_page(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.destroy()
        TestWindow(self.master)


class TestWindow(Frame):
    def __init__(self, master):
        super().__init__()

        # to track user typed words
        self.user_words = TypedWord()

        # the text to type
        self.type_test = TypeTest()

        # configure the root window
        self.master = master
        self.master.title("Test")
        self.master.config(padx=20, pady=20)

        # displays the time
        self.time_label = Label(self.master, text=f"Time Left : {TIME_MAX}", font=FONT, foreground=COLOR)
        self.time_label.grid(row=0, column=0, sticky="w", pady=20)

        self.gross_word_per_min = Label(self.master, text="GROSS WPM : 00", font=FONT, foreground=COLOR)
        self.gross_word_per_min.grid(row=0, column=1, pady=20)

        self.net_word_per_minute = Label(self.master, text="NET WPM : 00", font=FONT, foreground=COLOR)
        self.net_word_per_minute.grid(row=0, column=2, pady=20)

        self.accuracy = Label(self.master, text="Accuracy : 00", font=FONT, foreground=COLOR)
        self.accuracy.grid(row=0, column=3)

        # the text box displays the text to be typed
        self.text_box = Text(self.master, width=30, height=2, font=TEXTBOX_FONT, wrap=WORD, padx=50, pady=50)
        self.configure_text()
        self.text_box.grid(row=1, column=0, columnspan=4, pady=50)

        # variable the tracks the cursor location
        self.character_index = 0

        # display the text to type in the text box
        self.display_text()

        self.type_here = Label(self.master, text="Start Typing  in the >")
        self.type_here.grid()

        # the entry box the user can type
        char = self.register(self.avoid_space)
        self.entry_box = Entry(self.master, font=ENTRY_BOX_FONT, validate="key", validatecommand=(char, '%P'),
                               relief="solid")
        self.entry_box.grid(row=2, column=1, padx=5, pady=10, sticky="e")

        # the user can restart typying using the restart button the button will reset everything to start again
        self.restart_button = Button(self.master, text="Restart", command=self.restart_typing,
                                     background=GOOD, foreground="white", font=BUTTON_FONT, pady=5, padx=5)
        self.restart_button.grid(row=2, column=2)

        self.quit_button = Button(self.master, text="Quit", width=6, command=self.quit_typing,
                                  background=BAD, foreground="white", font=BUTTON_FONT, pady=5, padx=5)
        self.quit_button.grid(row=2, column=3)

        # the word in entry tracks the character in entered in the entry box
        self.word_in_entry = ""

        # all keys are bind to the function key_press
        self.key_release_id = self.entry_box.bind("<KeyRelease>", self.key_release)
        self.key_press_id = self.entry_box.bind("<KeyPress>", self.key_press)

        # to track state of timer
        self.timer_on = False

        # timer id
        self.timer = None

    def quit_typing(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.destroy()
        WelcomeWindow(self.master)

    def go_to_result(self, result):

        for widget in self.master.winfo_children():
            widget.destroy()

        self.destroy()
        ResultWindow(self.master, result)

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
        self.text_box.insert(END, self.type_test.generated_text)

        # highlight the first word
        self.text_box.delete(f"1.{self.character_index}",
                             f"1.{self.character_index + len(self.type_test.word_list[self.type_test.word_index])}")

        self.text_box.insert(f"1.{self.character_index}",
                             self.type_test.word_list[self.type_test.word_index], "current_word")

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

        if not self.timer_on and self.timer is None:
            self.start_timer()

        return True

    def key_press(self, event):

        """counts each key press other than special keys"""

        if event.keysym == "BackSpace":
            self.type_test.mistakes_typed += 1
            self.type_test.total_characters_typed += 1

        elif event.char and event.char != " ":
            self.type_test.total_characters_typed += 1

    def key_release(self, event):
        """handles every key release in the keyboard"""

        # every time a key is pressed the word_in_entry is updated
        self.word_in_entry = self.entry_box.get().strip()

        # the tab and enter key is not accepted
        if event.char == "\t" or event.char == "\r":
            return

        # space key is accepted only the word_in_entry have at least a valid character
        # clears the entry box and set the word in entry to empty string
        elif self.word_in_entry and event.char == " ":
            self.user_words.push(word=self.word_in_entry)

            # adding the count of incorrectly typed characters
            self.type_test.mistakes_typed += self.update_text_box()

            self.clear_entry()
            self.next_word()

        # if the backspace key is triggered
        elif event.keysym == "BackSpace":

            self.back_space()

        # if valid char other than space
        elif event.char and event.char != " ":
            self.update_meters(self.update_text_box())

    def back_space(self):
        """function handles all the backspace trigger"""

        # if type_test.typed_word_length is None
        self.text_box.config(state="normal")

        # if the length is less than zero then the highlight must move to the previous word
        if self.type_test.typed_word_length <= 0:
            # navigate to the previous word
            self.previous_word()
            return

        # if the word in the entry box is correctly typed
        if self.entry_box.get().strip() == self.type_test.word_list[self.type_test.word_index]:

            self.text_box.delete(f"1.{self.character_index}",
                                 f"1.{self.character_index + len(self.type_test.word_list[self.type_test.word_index])}")

            self.text_box.insert(f"1.{self.character_index}",
                                 self.type_test.word_list[self.type_test.word_index], "letter_correct")

        else:
            self.text_box.delete(f"1.{self.character_index}",
                                 f"1.{self.character_index + len(self.type_test.word_list[self.type_test.word_index])}")

            self.text_box.insert(f"1.{self.character_index}",
                                 self.type_test.word_list[self.type_test.word_index], "current_word")
            self.update_text_box()

        self.text_box.config(state="disabled")

        # update the length of the characters in the entry box
        self.type_test.typed_word_length = len(self.word_in_entry)

        # update the measuring values
        self.update_meters()

    def previous_word(self):
        """navigates to the previous word"""
        if self.user_words.peek():

            # remove the highlight from the current word
            self.text_box.delete(f"1.{self.character_index}",
                                 f"1.{self.character_index + len(self.type_test.word_list[self.type_test.word_index])}")

            self.text_box.insert(f"1.{self.character_index}",
                                 self.type_test.word_list[self.type_test.word_index])

            # update the word index by subtracting 1 so that it  points to the previous word
            self.type_test.word_index -= 1

            # update the character index to the beginning of the previous word
            self.character_index = self.character_index - len(self.type_test.word_list[self.type_test.word_index]) - 1

            # clear any entries in the entry box
            self.clear_entry()

            # pop the last completed word typed  from the user_words and display it in the entry box
            self.entry_box.insert(END, self.user_words.pop())

            # update the word in entry
            self.word_in_entry = self.entry_box.get()

            # # update the length of the characters in the entry box
            self.type_test.typed_word_length = len(self.word_in_entry)

            # delete the previous word and make it current
            self.text_box.delete(f"1.{self.character_index}",
                                 f"1.{self.character_index + len(self.type_test.word_list[self.type_test.word_index])}")

            # compare the word in entry with the original word and show indication on is it correct or not
            # the word is still active but already completed

            # if the word is correct
            if self.word_in_entry == self.type_test.word_list[self.type_test.word_index]:

                self.text_box.insert(f"1.{self.character_index}",
                                     self.type_test.word_list[self.type_test.word_index], "letter_correct")

            # this sets letters to current word
            # and then update text box is called to check the correction
            else:
                self.text_box.insert(f"1.{self.character_index}",
                                     self.type_test.word_list[self.type_test.word_index], "current_word")

                self.update_text_box()

    def next_word(self):
        """navigates to the next word and also check the previous word is correctly typed or not"""
        self.text_box.config(state="normal")

        # delete the current word
        self.text_box.delete(f"1.{self.character_index}",
                             f"1.{self.character_index + len(self.type_test.word_list[self.type_test.word_index])}")

        # checks the entered word is correct or wrong and update the text box with indication
        if self.word_in_entry == self.type_test.word_list[self.type_test.word_index]:

            self.text_box.insert(f"1.{self.character_index}",
                                 self.type_test.word_list[self.type_test.word_index], "correct_word")

            # counting and saving  the number of correctly typed characters

        else:
            self.text_box.insert(f"1.{self.character_index}",
                                 self.type_test.word_list[self.type_test.word_index], "incorrect_word")

        # update the cursor position
        # add the length of the previous word
        self.character_index = self.character_index + len(self.type_test.word_list[self.type_test.word_index]) + 1

        # update the word index
        self.type_test.word_index += 1

        # check whether the words to type are over
        if self.type_test.word_index != len(self.type_test.word_list):

            # highlight the next word to type
            self.text_box.delete(f"1.{self.character_index}",
                                 f"1.{self.character_index + len(self.type_test.word_list[self.type_test.word_index])}")

            self.text_box.insert(f"1.{self.character_index}",
                                 self.type_test.word_list[self.type_test.word_index], "current_word")

        # if there is no more word to type disable the entry box and unbind the keys
        # as this condition is triggered in the time count method this is no more needed
        else:
            self.stop_typing()

        # this code helps when the user navigate to next word and did not start typing
        # and decided to navigate to previous word
        # this becomes irrelevant when the user started typing the next word
        self.type_test.typed_word_length = -1

        self.text_box.config(state="disabled")

        # scroll to next line is the visible part is over
        if not self.text_box.dlineinfo(f"1.{self.character_index}"):
            self.text_box.yview_scroll(1, "units")

    def update_text_box(self):
        """this function updated the letters of current word with the appropriate indicate correct wrong not typed the
        function return number of incorrect characters typed"""

        self.text_box.config(state="normal")

        # the length of the word in the entry box is updated in each click
        self.type_test.typed_word_length = len(self.word_in_entry)

        # check each letter is typed correct and give color indication
        # red for wrongly typed letter and yellow for correct
        incorrect_letters = 0
        for i in range(self.type_test.typed_word_length):

            try:
                # check if i is valid index in the current word
                # if i is not a valid index then it gives  index error
                # the typed word is having length more than the correct word

                if self.type_test.word_list[self.type_test.word_index][i]:
                    self.text_box.delete(f"1.{self.character_index + i}",
                                         f"1.{self.character_index + i + 1}")

            except IndexError:
                # when the character count of typed word is more than the current word then update it with wrong
                self.text_box.delete(f"1.{self.character_index}",
                                     f"1.{self.character_index + len(self.type_test.word_list[self.type_test.word_index])}")

                self.text_box.insert(f"1.{self.character_index}",
                                     self.type_test.word_list[self.type_test.word_index], "letter_wrong")

                # every letter typed more than the actual word is counted incorrect

                incorrect_letters += (self.type_test.typed_word_length - i)

                return incorrect_letters

            else:

                if self.word_in_entry[i] == self.type_test.word_list[self.type_test.word_index][i]:

                    self.text_box.insert(f"1.{self.character_index + i}",
                                         self.type_test.word_list[self.type_test.word_index][i], "letter_correct")

                else:
                    self.text_box.insert(f"1.{self.character_index + i}",
                                         self.type_test.word_list[self.type_test.word_index][i], "letter_wrong")
                    incorrect_letters += 1

        self.text_box.config(state="disabled")

        return incorrect_letters

    def update_meters(self, current_mistake=0):

        """function to update the measuring values"""

        # update character per minute

        try:
            gross_wpm = int((self.type_test.total_characters_typed / 5) / (self.type_test.time / 60))

            net_wpm = gross_wpm - int(
                (((self.type_test.mistakes_typed + current_mistake) / 5) / (self.type_test.time / 60)))

        except ZeroDivisionError:
            gross_wpm = 0
            net_wpm = 0

        self.gross_word_per_min["text"] = "GROSS WPM : %02d" % gross_wpm

        self.net_word_per_minute["text"] = "NET WPM : %02d" % net_wpm

        try:
            accuracy = round(((net_wpm / gross_wpm) * 100))

        except ZeroDivisionError:
            accuracy = 0

        self.accuracy["text"] = f"Accuracy : {accuracy}%"

    def clock_count(self):
        """the function keeps the time and check all the possible triggers to end typing test in each second"""

        # when the user completes typing  all the word given in the text box
        # the entry box will already be disabled and self.timer_on will be made false
        if not self.timer_on:
            self.typing_test_end()

        # if the time reached the limit
        elif self.type_test.time >= TIME_MAX:
            self.time_label["text"] = f"Time Left : 00"
            self.stop_typing()
            self.typing_test_end()

        # update the count
        else:
            # self.time_label["text"] = f"Time : 0{count}"

            self.time_label["text"] = "Time Left : %02d" % abs(TIME_MAX - self.type_test.time)
            if self.type_test.time >= TIME_MAX - 10:

                # indication only few seconds left
                if self.type_test.time % 2 == 0:
                    self.time_label["background"] = 'red'
                else:
                    self.time_label["background"] = 'SystemButtonFace'
            self.type_test.time += 1
            self.timer = self.after(1000, self.clock_count)

    def start_timer(self):
        """start the timer"""
        # the timer is activated when the first valid character is typed in the

        if len(self.word_in_entry) < 1 and not self.timer_on:
            self.timer_on = True
            self.clock_count()
            self.restart_button.config(state="normal")
            # print("activate timer")

    def stop_typing(self):
        """stops the test stop accepting keys"""
        self.entry_box.config(state="disabled")
        self.entry_box.unbind("<KeyRelease>", self.key_release_id)
        self.entry_box.unbind("<KeyPress>", self.key_press_id)
        self.timer_on = False

    def typing_test_end(self):
        """display the result"""

        self.update_meters()

        # the gross word in one minute is the total number characters typed divided by 5 whole divided by the 60/60
        # that is 1 if the user finishes the given number of character before 60 seconds  type_test.time / 60
        try:
            gross_wpm = int((self.type_test.total_characters_typed / 5) / (self.type_test.time / 60))
            net_wpm = gross_wpm - int(((self.type_test.mistakes_typed / 5) / (self.type_test.time / 60)))

        except ZeroDivisionError:
            gross_wpm = 0
            net_wpm = 0

        try:
            accuracy = round((net_wpm / gross_wpm) * 100)

        except ZeroDivisionError:
            accuracy = 0

        result = {
            "net": net_wpm,
            "gross": gross_wpm,
            "accuracy": accuracy,
            "mistakes": self.type_test.mistakes_typed
        }

        self.go_to_result(result)

    def restart_typing(self):
        """the function will set to the default starting state of the test"""

        if not self.timer:
            return

        # make every thing to the default value so that the user can start from first
        self.timer_on = False

        self.character_index = 0
        self.word_in_entry = ""

        self.time_label["background"] = 'SystemButtonFace'

        self.time_label.config(text=f"Time Left : {TIME_MAX}")
        self.gross_word_per_min["text"] = "GROSS WPM : 00"
        self.net_word_per_minute["text"] = "NET WPM : 00"
        self.accuracy["text"] = "Accuracy : 00"

        self.user_words.make_empty()
        self.type_test.rest_default()

        self.text_box.config(state="normal")
        self.text_box.delete(0.0, END)
        self.display_text()

        self.entry_box.config(state="normal")
        self.key_release_id = self.entry_box.bind("<KeyRelease>", self.key_release)
        self.key_press_id = self.entry_box.bind("<KeyPress>", self.key_press)

        self.clear_entry()

        # cancel the timer
        self.after_cancel(self.timer)
        self.timer = None


class ResultWindow(Frame):
    def __init__(self, master, result):
        super().__init__()
        self.master = master
        self.master.title("Result")

        self.master.config(padx=20, pady=20)

        self.canvas = Canvas(self.master, width=620, height=400, )
        self.canvas.grid(row=0, column=0, columnspan=2, padx=60, pady=20)

        self.bg = PhotoImage(file="image_resource/Result.png")
        self.bg_image = self.canvas.create_image(310, 200, image=self.bg)

        self.retry_button = Button(text="Try Again!", command=self.go_to_test_page,
                                   foreground="white", background=GOOD, font=BUTTON_FONT, padx=10, pady=10)
        self.retry_button.grid(row=1, column=0, padx=50, )

        self.quit_button = Button(text="I Quit", command=self.quit,
                                  foreground="white", background=BAD, font=BUTTON_FONT, padx=10, pady=10)
        self.quit_button.grid(row=1, column=1, padx=50, )

        self.net = result["net"]
        self.gross = result["gross"]

        self.accuracy_percentage = result["accuracy"]

        if result["accuracy"] < 0:
            self.accuracy_percentage = 0
            self.net = 0

        elif result["accuracy"] == 100 and result["mistakes"] > 0:
            self.accuracy_percentage = 99

        else:
            self.accuracy_percentage = result["accuracy"]

        self.process()

    def process(self):
        """processing the result"""
        for x in range(self.accuracy_percentage + 1):

            if x >= 90:
                outline_color = GOOD
            elif x >= 75:
                outline_color = AVERAGE
            else:
                outline_color = BAD

            self.master.after(5)
            percentage_display = self.canvas.create_arc(254, 153, 367, 267, width=10, start=90,
                                                        extent=round(360 * (x / 100)),
                                                        style="arc", offset="center", outline=outline_color)
            accuracy_display = self.canvas.create_text(312, 208, text=f"{x}%", font=TEXT_FONT, fill=TEXT_COLOR)

            net_wpm_display = self.canvas.create_text(208, 318, text=random.randint(0, self.gross + 1), font=TEXT_FONT,
                                                      fill=TEXT_COLOR)

            gross_wpm_display = self.canvas.create_text(540, 318, text=random.randint(0, self.gross + 1),
                                                        font=TEXT_FONT,
                                                        fill=TEXT_COLOR)

            self.master.update()

            self.canvas.delete(accuracy_display)
            self.canvas.delete(net_wpm_display)
            self.canvas.delete(gross_wpm_display)
            self.canvas.delete(percentage_display)

        if x == 100:
            percentage_display = self.canvas.create_oval(254, 153, 367, 267, width=10, offset="center",
                                                         outline=outline_color)
        else:
            percentage_display = self.canvas.create_arc(254, 153, 367, 267, width=10, start=90,
                                                        extent=round(360 * (x / 100)),
                                                        style="arc", offset="center", outline=outline_color)

        accuracy_display = self.canvas.create_text(312, 208, text=f"{x}%", font=TEXT_FONT, fill=TEXT_COLOR)

        net_wpm_display = self.canvas.create_text(208, 318, text=self.net, font=TEXT_FONT, fill=TEXT_COLOR)

        gross_wpm_display = self.canvas.create_text(540, 318, text=self.gross, font=TEXT_FONT, fill=TEXT_COLOR)

        # self.type_again_button = Button(self.master, text="I can Do It More Better !", command=self.go_to_test_page)
        # self.type_again_button.grid()
        #
        # self.quit_button = Button(self.master, text="I Quit", command=self.exit_test)
        # self.quit_button.grid()

    def go_to_test_page(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.destroy()
        TestWindow(self.master)

# class APP(Tk):
#     def __init__(self):
#         super().__init__()
#
#         # configure the root window
#         self.title('Type Test')
#         self.config(padx=10, pady=10)
#         # displays the time
#         self.time_label = Label(self, text=f"Time Left : {TIME_MAX}", font=FONT, foreground=COLOR)
#         self.time_label.grid(row=0, column=0, sticky="w")
#
#         self.gross_word_per_min = Label(self, text="GROSS WPM : 00", font=FONT, foreground=COLOR)
#         self.gross_word_per_min.grid(row=0, column=1)
#
#         self.net_word_per_minute = Label(self, text="NET WPM : 00", font=FONT, foreground=COLOR)
#         self.net_word_per_minute.grid(row=0, column=2)
#
#         self.accuracy = Label(self, text="Accuracy : 00", font=FONT, foreground=COLOR)
#         self.accuracy.grid(row=0, column=3)
#
#         # the text box displays the text to be typed
#         self.text_box = Text(self, width=30, height=2, font=TEXTBOX_FONT, wrap=WORD, padx=50, pady=50)
#         self.configure_text()
#         self.text_box.grid(row=1, column=0, columnspan=4)
#
#         # variable the tracks the cursor location
#         self.character_index = 0
#
#         # display the text to type in the text box
#         self.display_text()
#
#         # the entry box the user can type
#         char = self.register(self.avoid_space)
#         self.entry_box = Entry(self, font=ENTRY_BOX_FONT, validate="key", validatecommand=(char, '%P'),
#                                relief="solid")
#         self.entry_box.grid(row=2, column=1, padx=5, pady=10, sticky="e")
#
#         # the user can restart typying using the restart button the button will reset everything to start again
#         self.restart = Button(text="Restart", command=self.restart_typing,
#                               background="blue", foreground="white", font=BUTTON_FONT, pady=5, padx=5)
#         self.restart.grid(row=2, column=2)
#
#         # the word in entry tracks the character in entered in the entry box
#         self.word_in_entry = ""
#
#         # all keys are bind to the function key_press
#         self.key_release_id = self.entry_box.bind("<KeyRelease>", self.key_release)
#         self.key_press_id = self.entry_box.bind("<KeyPress>", self.key_press)
#
#         # to track state of timer
#         self.timer_on = False
#
#         # timer id
#         self.timer = None
#
#     def configure_text(self):
#         """function to configure text style """
#
#         # tag to highlight the current word to type
#         self.text_box.tag_configure("current_word", background="green", foreground="white")
#
#         # after navigating to next word
#         # if the previous word is typed correct
#         self.text_box.tag_configure("correct_word", background="white", foreground="green")
#         # if the previous word is typed wrong
#         self.text_box.tag_configure("incorrect_word", background="white", foreground="red")
#
#         # if the letter is typed wrong
#         self.text_box.tag_configure("letter_wrong", background="green", foreground="red")
#         # if letter is typped correct
#         self.text_box.tag_configure("letter_correct", background="green", foreground="yellow")
#
#     def display_text(self):
#         """this function displays the text to type in the text box"""
#
#         # insert the generated text for the test in the text box
#         self.text_box.insert(END, type_test.generated_text)
#
#         # highlight the first word
#         self.text_box.delete(f"1.{self.character_index}",
#                              f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")
#
#         self.text_box.insert(f"1.{self.character_index}",
#                              type_test.word_list[type_test.word_index], "current_word")
#
#         # disable text box to avoid unnecessary interactions
#         self.text_box.config(state="disabled")
#
#     def clear_entry(self):
#         """function clears the entry box"""
#
#         self.entry_box.delete(first=0, last=END)
#
#     def avoid_space(self, input_char):
#         """this function make sure that there is no blank space in front of the text in the entry box"""
#
#         # the entry box won't accept a blank space in front of a word
#         # each word should start with a valid character not blank space and no blank space is allowed inbetween word
#         if " " in input_char:
#             return False
#
#         if not self.timer_on:
#             self.start_timer()
#
#         return True
#
#     def key_press(self, event):
#         """counts each key press other than special keys"""
#
#         if event.keysym == "BackSpace":
#             type_test.mistakes_typed += 1
#             type_test.total_characters_typed += 1
#
#         elif event.char:
#             type_test.total_characters_typed += 1
#
#     def key_release(self, event):
#         """handles every key release in the keyboard"""
#
#         # every time a key is pressed the word_in_entry is updated
#         self.word_in_entry = self.entry_box.get().strip()
#
#         # the tab and enter key is not accepted
#         if event.char == "\t" or event.char == "\r":
#             return
#
#         # space key is accepted only the word_in_entry have at least a valid character
#         # clears the entry box and set the word in entry to empty string
#         elif self.word_in_entry and event.char == " ":
#             user_words.push(word=self.word_in_entry)
#             # adding the count of incorrectly typed characters
#             type_test.mistakes_typed += self.update_text_box()
#             self.clear_entry()
#             self.next_word()
#
#         # if the backspace key is triggered
#         elif event.keysym == "BackSpace":
#
#             self.back_space()
#
#         # if valid char other than space
#         elif event.char and event.char != " ":
#             self.update_meters(self.update_text_box())
#
#     def back_space(self):
#         """function handles all the backspace trigger"""
#
#         # if type_test.typed_word_length is None
#         self.text_box.config(state="normal")
#
#         # if the length is less than zero then the highlight must move to the previous word
#         if type_test.typed_word_length <= 0:
#             # navigate to the previous word
#             self.previous_word()
#             return
#
#         # if the word in the entry box is correctly typed
#         if self.entry_box.get().strip() == type_test.word_list[type_test.word_index]:
#
#             self.text_box.delete(f"1.{self.character_index}",
#                                  f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")
#
#             self.text_box.insert(f"1.{self.character_index}",
#                                  type_test.word_list[type_test.word_index], "letter_correct")
#
#         else:
#             self.text_box.delete(f"1.{self.character_index}",
#                                  f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")
#
#             self.text_box.insert(f"1.{self.character_index}",
#                                  type_test.word_list[type_test.word_index], "current_word")
#             self.update_text_box()
#
#         self.text_box.config(state="disabled")
#
#         # update the length of the characters in the entry box
#         type_test.typed_word_length = len(self.word_in_entry)
#
#         # update the measuring values
#         self.update_meters()
#
#     def previous_word(self):
#         """navigates to the previous word"""
#         if user_words.peek():
#             # remove the highlight from the current word
#             self.text_box.delete(f"1.{self.character_index}",
#                                  f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")
#
#             self.text_box.insert(f"1.{self.character_index}",
#                                  type_test.word_list[type_test.word_index])
#
#             # update the word index by subtracting 1 so that it  points to the previous word
#             type_test.word_index -= 1
#
#             # update the character index to the beginning of the previous word
#             self.character_index = self.character_index - len(type_test.word_list[type_test.word_index]) - 1
#
#             # clear any entries in the entry box
#             self.clear_entry()
#
#             # pop the last completed word typed  from the user_words and display it in the entry box
#             self.entry_box.insert(END, user_words.pop())
#
#             # update the word in entry
#             self.word_in_entry = self.entry_box.get()
#
#             # # update the length of the characters in the entry box
#             type_test.typed_word_length = len(self.word_in_entry)
#
#             # delete the previous word and make it current
#             self.text_box.delete(f"1.{self.character_index}",
#                                  f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")
#
#             # compare the word in entry with the original word and show indication on is it correct or not
#             # the word is still active but already completed
#
#             # if the word is correct
#             if self.word_in_entry == type_test.word_list[type_test.word_index]:
#
#                 self.text_box.insert(f"1.{self.character_index}",
#                                      type_test.word_list[type_test.word_index], "letter_correct")
#
#             # this sets letters to current word
#             # and then update text box is called to check the correction
#             else:
#                 self.text_box.insert(f"1.{self.character_index}",
#                                      type_test.word_list[type_test.word_index], "current_word")
#
#                 self.update_text_box()
#
#     def next_word(self):
#         """navigates to the next word and also check the previous word is correctly typed or not"""
#         self.text_box.config(state="normal")
#
#         # delete the current word
#         self.text_box.delete(f"1.{self.character_index}",
#                              f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")
#
#         # checks the entered word is correct or wrong and update the text box with indication
#         if self.word_in_entry == type_test.word_list[type_test.word_index]:
#
#             self.text_box.insert(f"1.{self.character_index}",
#                                  type_test.word_list[type_test.word_index], "correct_word")
#
#             # counting and saving  the number of correctly typed characters
#
#         else:
#             self.text_box.insert(f"1.{self.character_index}",
#                                  type_test.word_list[type_test.word_index], "incorrect_word")
#
#         # update the cursor position
#         # add the length of the previous word
#         self.character_index = self.character_index + len(type_test.word_list[type_test.word_index]) + 1
#
#         # update the word index
#         type_test.word_index += 1
#
#         # check whether the words to type are over
#         if type_test.word_index != len(type_test.word_list):
#
#             # highlight the next word to type
#             self.text_box.delete(f"1.{self.character_index}",
#                                  f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")
#
#             self.text_box.insert(f"1.{self.character_index}",
#                                  type_test.word_list[type_test.word_index], "current_word")
#
#         # if there is no more word to type disable the entry box and unbind the keys
#         # as this condition is triggered in the time count method this is no more needed
#         else:
#             self.stop_typing()
#
#         # this code helps when the user navigate to next word and did not start typing
#         # and decided to navigate to previous word
#         # this becomes irrelevant when the user started typing the next word
#         type_test.typed_word_length = -1
#
#         self.text_box.config(state="disabled")
#
#         # scroll to next line is the visible part is over
#         if not self.text_box.dlineinfo(f"1.{self.character_index}"):
#             self.text_box.yview_scroll(1, "units")
#
#     def update_text_box(self):
#         """this function updated the letters of current word with the appropriate indicate correct wrong not typed the
#         function return number of incorrect characters typed"""
#
#         self.text_box.config(state="normal")
#
#         # the length of the word in the entry box is updated in each click
#         type_test.typed_word_length = len(self.word_in_entry)
#
#         # check each letter is typed correct and give color indication
#         # red for wrongly typed letter and yellow for correct
#         incorrect_letters = 0
#         for i in range(type_test.typed_word_length):
#
#             try:
#                 # check if i is valid index in the current word
#                 # if i is not a valid index then it gives  index error
#                 # the typed word is having length more than the correct word
#
#                 if type_test.word_list[type_test.word_index][i]:
#                     self.text_box.delete(f"1.{self.character_index + i}",
#                                          f"1.{self.character_index + i + 1}")
#
#             except IndexError:
#                 # when the character count of typed word is more than the current word then update it with wrong
#                 self.text_box.delete(f"1.{self.character_index}",
#                                      f"1.{self.character_index + len(type_test.word_list[type_test.word_index])}")
#
#                 self.text_box.insert(f"1.{self.character_index}",
#                                      type_test.word_list[type_test.word_index], "letter_wrong")
#
#                 return incorrect_letters
#
#             else:
#
#                 if self.word_in_entry[i] == type_test.word_list[type_test.word_index][i]:
#
#                     self.text_box.insert(f"1.{self.character_index + i}",
#                                          type_test.word_list[type_test.word_index][i], "letter_correct")
#
#                 else:
#                     self.text_box.insert(f"1.{self.character_index + i}",
#                                          type_test.word_list[type_test.word_index][i], "letter_wrong")
#                     incorrect_letters += 1
#
#         self.text_box.config(state="disabled")
#
#         return incorrect_letters
#
#     def update_meters(self, current_mistake=0):
#
#         """function to update the measuring values"""
#
#         # update character per minute
#         gross_wpm = int((type_test.total_characters_typed / 5) / (type_test.time / 60))
#         net_wpm = gross_wpm - int((((type_test.mistakes_typed + current_mistake) / 5) / (type_test.time / 60)))
#
#         self.gross_word_per_min["text"] = "GROSS WPM : %02d" % gross_wpm
#
#         self.net_word_per_minute["text"] = "NET WPM : %02d" % net_wpm
#
#         self.accuracy["text"] = "Accuracy : " + "%02d" % ((net_wpm / gross_wpm) * 100) + "%"
#
#     def clock_count(self):
#         """the function keeps the time and check all the possible triggers to end typing test in each second"""
#
#         # when the user completes typing  all the word given in the text box
#         # the entry box will already be disabled and self.timer_on will be made false
#         if not self.timer_on:
#             self.typing_test_end()
#
#         # if the time reached the limit
#         elif type_test.time >= TIME_MAX:
#             self.time_label["text"] = f"Time Left : 00"
#             self.stop_typing()
#             self.typing_test_end()
#
#         # update the count
#         else:
#             # self.time_label["text"] = f"Time : 0{count}"
#
#             self.time_label["text"] = "Time Left : %02d" % abs(TIME_MAX - type_test.time)
#             type_test.time += 1
#             self.timer = self.after(1000, self.clock_count)
#
#     def start_timer(self):
#         """start the timer"""
#         # the timer is activated when the first valid character is typed in the
#         if len(self.word_in_entry) < 1 and not self.timer_on:
#             self.timer_on = True
#             self.clock_count()
#             self.restart.config(state="normal")
#             # print("activate timer")
#
#     def stop_typing(self):
#         """stops the test stop accepting keys"""
#         self.entry_box.config(state="disabled")
#         self.entry_box.unbind("<KeyRelease>", self.key_release_id)
#         self.entry_box.unbind("<KeyPress>", self.key_press_id)
#         self.timer_on = False
#
#     def typing_test_end(self):
#         """display the result"""
#
#         self.update_meters()
#         print(f"Total Characters typed = {type_test.total_characters_typed}")
#         print(f"Mistakes = {type_test.mistakes_typed}")
#
#         # the gross word in one minute is the total number characters typed divided by 5 whole divided by the 60/60
#         # that is 1 if the user finishes the given number of character before 60 seconds  type_test.time / 60
#         gross_wpm = int((type_test.total_characters_typed / 5) / (type_test.time / 60))
#         net_wpm = gross_wpm - int(((type_test.mistakes_typed / 5) / (type_test.time / 60)))
#
#         print(f"Net WPM = {net_wpm}")
#         print(f"Gross WPM = {gross_wpm}")
#         print("Accuracy = " + "%02d" % ((net_wpm / gross_wpm) * 100) + "%")
#
#     def restart_typing(self):
#         """the function will set to the default starting state of the test"""
#
#         if not self.timer:
#             return
#
#         # make every thing to the default value so that the user can start from first
#         self.timer_on = False
#
#         # cancel the timer
#         self.after_cancel(self.timer)
#
#         self.character_index = 0
#         self.word_in_entry = ""
#
#         self.time_label.config(text=f"Time Left : {TIME_MAX}")
#         self.gross_word_per_min["text"] = "GROSS WPM : 00"
#         self.net_word_per_minute["text"] = "NET WPM : 00"
#         self.accuracy["text"] = "Accuracy : 00"
#         user_words.make_empty()
#         type_test.rest_default()
#
#         self.text_box.config(state="normal")
#         self.text_box.delete(0.0, END)
#         self.display_text()
#
#         self.entry_box.config(state="normal")
#         self.key_release_id = self.entry_box.bind("<KeyRelease>", self.key_release)
#         self.key_press_id = self.entry_box.bind("<KeyPress>", self.key_press)
#
#         self.clear_entry()
