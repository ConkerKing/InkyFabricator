import tkinter as tk
from tkinter import messagebox
import random

# -----------------------------
# Global game state
# -----------------------------
difficulty_settings = {}
number_to_guess = 0
attempts_left = 0
current_level = 1
wrong_attempts = 0


# -----------------------------
# Helper Functions
# -----------------------------
def get_riddle_hint(number):
    """Generate a riddle-like hint for hard difficulty."""
    hints = []

    if number % 2 == 0:
        hints.append("It’s an even number.")
    else:
        hints.append("It’s an odd number.")

    if number % 5 == 0:
        hints.append("It’s a multiple of 5.")
    elif number % 3 == 0:
        hints.append("It’s divisible by 3.")

    if number > 50:
        hints.append("It’s greater than 50.")
    else:
        hints.append("It’s 50 or less.")

    if number < 10:
        hints.append("It’s a single-digit number.")
    elif number >= 90:
        hints.append("It’s close to 100.")

    return random.choice(hints)


def setup_difficulty(choice):
    """Set the parameters for the selected difficulty."""
    global difficulty_settings

    if choice == "Easy":
        difficulty_settings = {"name": "Easy", "levels": 3, "attempts": 10, "base_range": 10, "hint_type": "direct"}
    elif choice == "Normal":
        difficulty_settings = {"name": "Normal", "levels": 5, "attempts": 7, "base_range": 50, "hint_type": "mixed"}
    else:
        difficulty_settings = {"name": "Hard", "levels": 7, "attempts": 5, "base_range": 100, "hint_type": "riddle"}

    start_level(1)


def start_level(level):
    """Initialize a new level."""
    global number_to_guess, attempts_left, current_level, wrong_attempts

    current_level = level
    wrong_attempts = 0
    level_range = int(difficulty_settings["base_range"] * (level / difficulty_settings["levels"]))
    number_to_guess = random.randint(1, level_range)
    attempts_left = difficulty_settings["attempts"]

    update_display(f"Level {level} — Range: 1 to {level_range}\nYou have {attempts_left} attempts.")


def check_guess():
    """Handle the player's guess."""
    global attempts_left, wrong_attempts, number_to_guess, current_level

    guess = entry_guess.get().strip()

    if not guess.isdigit():
        update_display("⚠️ Please enter a valid number.")
        return

    guess = int(guess)
    entry_guess.delete(0, tk.END)
    wrong_attempts += 1
    attempts_left -= 1

    # Correct guess
    if guess == number_to_guess:
        if current_level < difficulty_settings["levels"]:
            messagebox.showinfo("Correct!", f"🎉 You cleared Level {current_level}!")
            start_level(current_level + 1)
        else:
            messagebox.showinfo("Victory!", "🏆 You completed all levels! You Win!")
            reset_game()
        return

    # Incorrect guess
    hint_type = difficulty_settings["hint_type"]

    if hint_type == "direct":
        hint = "Too low! Try higher." if guess < number_to_guess else "Too high! Try lower."

    elif hint_type == "mixed":
        if wrong_attempts % 2 == 0:
            hint = "Hint: Higher!" if guess < number_to_guess else "Hint: Lower!"
        else:
            hint = "No hint this time!"

    else:  # riddle
        hint = get_riddle_hint(number_to_guess)

    if attempts_left > 0:
        update_display(f"{hint}\nAttempts left: {attempts_left}")
    else:
        messagebox.showwarning("Game Over", "💀 Out of attempts! Restarting...")
        start_level(1)


def update_display(message):
    """Update the on-screen message label."""
    label_message.config(text=message)


def reset_game():
    """Return to the main menu."""
    frame_game.pack_forget()
    frame_menu.pack(pady=20)
    update_display("")


# -----------------------------
# Tkinter UI Setup
# -----------------------------
window = tk.Tk()
window.title("🎯 Number Guessing Game")
window.geometry("400x400")
window.resizable(False, False)

# --- Main Menu ---
frame_menu = tk.Frame(window)
frame_menu.pack(pady=20)

label_welcome = tk.Label(frame_menu, text="Welcome to the Number Guessing Game!", font=("Arial", 14))
label_welcome.pack(pady=10)

btn_easy = tk.Button(frame_menu, text="Easy", width=20, command=lambda: switch_to_game("Easy"))
btn_normal = tk.Button(frame_menu, text="Normal", width=20, command=lambda: switch_to_game("Normal"))
btn_hard = tk.Button(frame_menu, text="Hard", width=20, command=lambda: switch_to_game("Hard"))
btn_easy.pack(pady=5)
btn_normal.pack(pady=5)
btn_hard.pack(pady=5)


def switch_to_game(choice):
    """Switch from menu to gameplay."""
    frame_menu.pack_forget()
    frame_game.pack(pady=20)
    setup_difficulty(choice)


# --- Game Screen ---
frame_game = tk.Frame(window)

label_message = tk.Label(frame_game, text="", font=("Arial", 12), wraplength=350, justify="center")
label_message.pack(pady=20)

entry_guess = tk.Entry(frame_game, font=("Arial", 12))
entry_guess.pack(pady=10)

btn_submit = tk.Button(frame_game, text="Submit Guess", command=check_guess)
btn_submit.pack(pady=5)

btn_back = tk.Button(frame_game, text="Back to Menu", command=reset_game)
btn_back.pack(pady=5)

# Start App
window.mainloop()
