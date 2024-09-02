from tkinter import *
from screen import WelcomeWindow, ResultWindow, TestWindow
if __name__ == "__main__":
    root = Tk()

    root.minsize(800, 520)
    root.maxsize(800, 520)

    WelcomeWindow(root)

    root.mainloop()

