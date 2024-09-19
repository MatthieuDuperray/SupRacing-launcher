from tkinter import *
from tkinter import ttk
import os
import utils
import time
from leaderboard import update as leaderboard_update

# stylish paramaters

pad_x = 24
pad_y = 12

# main player profile

global player
player = ''

#* Main window

root = Tk()
root.resizable(width=False, height=False)
root.title("Login")

#* AC logo

ac_logo = PhotoImage(file='./Image/btn_AC_logo.png')
ttk.Label(
    root, image=ac_logo, anchor="center"
).grid(
    column=0, row=1, columnspan=2, pady=pad_y
)

#* Interactive stuff

first_log_frame = ttk.Frame(
    root
)
first_log_frame.grid(
    column=0, row=2, sticky=N, padx=(pad_x, pad_x/2)
)

loged_once_frame = ttk.Frame(
    root
)
loged_once_frame.grid(
    column=1, row=2, sticky=N, padx=(pad_x/2, pad_x)
)

#* First time log

ttk.Label(
    first_log_frame, text="First Time logging in?",
    font = 16
).grid(
    column=0, row=1, pady=pad_y
)

# Name

ttk.Label(
    first_log_frame, text="Enter your first name here: ",
    font = 12
).grid(
    column=0, row=2, sticky=W
)

first_name = StringVar()

first_name_entry = ttk.Entry(
    first_log_frame, textvariable=first_name
)
first_name_entry.grid(
    column=0, row=3, pady=(pad_y/2, pad_y), sticky=(E, W)
)

# Last Name

ttk.Label(
    first_log_frame, text="Enter your last name here: ",
    font = 12
).grid(
    column=0, row=4, sticky=W
)

last_name = StringVar()

last_name_entry = ttk.Entry(
    first_log_frame, textvariable=last_name
)
last_name_entry.grid(
    column=0, row=5, pady=(pad_y/2, pad_y), sticky=(E, W)
)

# Launch button

def lets_go_register():
    global player

    if first_name.get() == '' or last_name.get() == '':
        error['text'] = 'Please enter a Name and a last Name to register'
        error.grid(
            column=0, row=3, columnspan=2
        )
        return

    player = first_name.get().capitalize().strip() + "_" + last_name.get().upper().strip()
    
    if player in player_list:
        print("Profile exists already")
        utils.load_player(player)
    else:
        utils.create_player(player)

    utils.load_player(player)

    root.destroy()


launch = ttk.Button(
    root, text="Register and launch", command=lets_go_register
)
launch.grid(
    column=0, row=4, sticky=(N), pady=pad_y
)

#* Loged once before

ttk.Label(
    loged_once_frame, text="Logged once before?",
    font = 16
).grid(
    column=1, row=0, pady=pad_y, columnspan=2
)

# Get the list of previous players

player_list = os.listdir('./players')
player_list.sort()
player_list_var = StringVar(value=player_list)

player_listbox = Listbox(
    loged_once_frame, height=7, width=30, listvariable=player_list_var
)
player_listbox.grid(
    column=1, row=1, sticky=(E)
)
player_scrol = ttk.Scrollbar(
    loged_once_frame, orient=VERTICAL, command=player_listbox.yview
)
player_scrol.grid(
    column=2, row=1, sticky=(N,S,W)
)

# Launch button

def lets_go_connect():

    if player_listbox.curselection() == ():

        error['text'] = 'Please select a player'
        error.grid(
            column=0, row=3, columnspan=2
        )
        return
    
    global player
    player = player_list[player_listbox.curselection()[0]]

    utils.load_player(player)

    root.destroy()
    

launch = ttk.Button(
    root, text="Connect and launch", command=lets_go_connect
)
launch.grid(
    column=1, row=4, sticky=(N), pady=pad_y
)


# Error message

error = ttk.Label(
    root, font=12, foreground='red'
)


if __name__ == "__main__":

    root.mainloop()

    if player != '':
        start = time.asctime()

        utils.launch_game(244210, "AssettoCorsa.exe", player)

        end = time.asctime()    

        utils.save_player(player)
        utils.log(player, start, end)
        # sheet_log.sheet.add("1f-Myu8fBzV055cakvrHinSlJi9xiJ_ICsK2a6rLDbGA", 'Feuille 1!A:C',[[player, start, end]])
        leaderboard_update()
