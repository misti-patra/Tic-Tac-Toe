# import tkinter as tk
# from tkinter import messagebox

# def check_winner():
#     for combo in [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]:
#         if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
#             buttons[combo[0]].config(bg = "green")
#             buttons[combo[1]].config(bg = "green")
#             buttons[combo[2]].config(bg = "green")
#             messagebox.showinfo("Tic-Tac-Toe", f"Player {buttons[combo[0]]['text']} wins!")
#             root.quit()

# def check_draw():
#     if all(button["text"] != "" for button in buttons) and not check_winner():
#         messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
#         return True  # Return True if it's a draw
#     return False  # Return False if not a draw

# def button_click(index):
#     global winner
#     if buttons[index]["text"] == "" and not winner:
#         buttons[index]["text"] = current_player
#         winner = check_winner()
#         if not winner:
#             if check_draw():
#                 root.quit()  # Exit the game if it's a draw
#             toggle_player()


# def toggle_player():
#     global current_player
#     current_player = "X" if current_player == "O" else "O"
#     label.config(text = f"Player {current_player}'s turn")


# root = tk.Tk()
# root.title("Tic-Tac-Toe")


# buttons = [tk.Button(root,text="", font = ("normal", 25), width=6, height=2, command=lambda i=i: button_click(i)) for i in range(9)]

# for i, button in enumerate(buttons):
#     button.grid(row=i //3, column=i % 3)


# current_player = "X"
# winner = False
# label = tk.Label(root, text =f"Player {current_player}'s turn", font=("normal",16))
# label.grid(row=3, column=0, columnspan=3)

# root.mainloop()

import tkinter as tk
from tkinter import messagebox
import random
import platform

# Sound alternative (simple workaround)
def play_sound():
    print("Beep!")  # placeholder for beep sound

# Initialize window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Globals
buttons = []
current_player = "X"
winner = False
last_move = None
scores = {"X": 0, "O": 0}
vs_ai = tk.BooleanVar()
emoji_mode = tk.BooleanVar()
dark_mode = tk.BooleanVar()
timer_id = None
time_left = 10

# Win combos
winning_combos = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8],
    [0,4,8], [2,4,6]
]

# Timer logic
def countdown():
    global time_left, timer_id
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time left: {time_left}s")
        timer_id = root.after(1000, countdown)
    else:
        toggle_player()
        if vs_ai.get() and current_player == "O":
            root.after(500, ai_move)
        start_timer()

# Toggle player
def toggle_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"
    label.config(text=f"Player {current_player}'s turn")

# Check win
def check_winner():
    global winner
    for combo in winning_combos:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
            for i in combo:
                buttons[i].config(bg="green")
            winner = True
            update_score(buttons[combo[0]]["text"])
            play_sound()
            messagebox.showinfo("Tic-Tac-Toe", f"Player {buttons[combo[0]]['text']} wins!")
            save_leaderboard(buttons[combo[0]]["text"])
            return True
    return False

# Draw
def check_draw():
    if all(button["text"] != "" for button in buttons) and not winner:
        messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
        return True
    return False

# Score update
def update_score(winner_symbol):
    scores[winner_symbol] += 1
    score_label.config(text=f"Score - X: {scores['X']} | O: {scores['O']}")

# Save to leaderboard file
def save_leaderboard(winner_symbol):
    with open("leaderboard.txt", "a") as f:
        f.write(f"{winner_symbol} won\n")

# Start timer
def start_timer():
    global time_left, timer_id
    if timer_id:
        root.after_cancel(timer_id)
    time_left = 10
    countdown()

# AI move
def ai_move():
    empty = [i for i, b in enumerate(buttons) if b["text"] == ""]
    if empty and not winner:
        move = random.choice(empty)
        make_move(move)

# Hint system
def give_hint():
    empty = [i for i, b in enumerate(buttons) if b["text"] == ""]
    if empty and not winner:
        hint = random.choice(empty)
        buttons[hint].config(bg="lightblue")
        root.after(1000, lambda: buttons[hint].config(bg="SystemButtonFace" if not dark_mode.get() else "#333"))

# Make move
def make_move(index):
    global last_move
    if buttons[index]["text"] == "" and not winner:
        if last_move is not None:
            buttons[last_move].config(bg="SystemButtonFace" if not dark_mode.get() else "#333")
        symbol = "😎" if current_player == "X" and emoji_mode.get() else ("🤖" if current_player == "O" and emoji_mode.get() else current_player)
        buttons[index]["text"] = symbol
        last_move = index
        buttons[index].config(bg="yellow")
        if not check_winner():
            if check_draw():
                return
            toggle_player()
            start_timer()
            if vs_ai.get() and current_player == "O":
                root.after(500, ai_move)

# Button click
def button_click(index):
    make_move(index)

# Reset
def reset_game():
    global winner, current_player, last_move
    for btn in buttons:
        btn.config(text="", bg="SystemButtonFace" if not dark_mode.get() else "#333")
    winner = False
    current_player = "X"
    last_move = None
    label.config(text=f"Player {current_player}'s turn")
    start_timer()

# Theme
def toggle_theme():
    color = "#222" if dark_mode.get() else "SystemButtonFace"
    fg_color = "white" if dark_mode.get() else "black"
    for b in buttons:
        b.config(bg=color)
    root.config(bg=color)
    label.config(bg=color, fg=fg_color)
    score_label.config(bg=color, fg=fg_color)
    timer_label.config(bg=color, fg=fg_color)

# UI Grid
for i in range(9):
    b = tk.Button(root, text="", font=("normal", 25), width=6, height=2, command=lambda i=i: button_click(i))
    b.grid(row=i//3, column=i%3)
    buttons.append(b)

label = tk.Label(root, text=f"Player {current_player}'s turn", font=("normal", 16))
label.grid(row=3, column=0, columnspan=3)

score_label = tk.Label(root, text="Score - X: 0 | O: 0", font=("normal", 14))
score_label.grid(row=4, column=0, columnspan=3)

timer_label = tk.Label(root, text="Time left: 10s", font=("normal", 14))
timer_label.grid(row=5, column=0, columnspan=3)

tk.Button(root, text="Reset", font=("normal", 14), command=reset_game).grid(row=6, column=0)
tk.Button(root, text="Hint", font=("normal", 14), command=give_hint).grid(row=6, column=1)
tk.Checkbutton(root, text="Play vs AI", variable=vs_ai).grid(row=6, column=2)
tk.Checkbutton(root, text="Emoji Mode", variable=emoji_mode).grid(row=7, column=0)
tk.Checkbutton(root, text="Dark Mode", variable=dark_mode, command=toggle_theme).grid(row=7, column=1)

# Start
toggle_theme()
start_timer()
root.mainloop()
