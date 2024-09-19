import utils
from tkinter import *
from tkinter import font as tkfont
from tkinter import ttk

# stylish paramaters

pad_x = 24
pad_y = 12


#* Main window

root = Tk()
root.resizable(width=False, height=False)
root.title("Player switch")

#* Sub Frames

instruction_frame = ttk.Frame(
    root
)
instruction_frame.grid(
    column=0, row=0, sticky=N, padx=pad_x
)

#* Instructions

ttk.Label(
    instruction_frame, text="Use this window to quickly change player", font=16
).grid(
    column=0, row=0, pady=pad_y
)

ttk.Label(
    instruction_frame, text="Please note that you should return to the launcher\nbefore you change active player."
).grid(
    column=0, row=1, pady=pad_y
)

root.mainloop()

def player_switch():
    return