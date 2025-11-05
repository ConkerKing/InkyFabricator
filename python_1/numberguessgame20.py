import tkinter as tk
from tkinter import messagebox
import random
import time

# =========================
# Game Logic
# =========================
class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game - Deluxe Edition")
        self.root.geometry("480x500")
        self.root.resizable(False, False)

        self.score = 0
        self.level = 1
        self.attempts_left = 0
        self.number_to_guess = 0
        self.start_time = None
        self.difficulty = None

        self.build_welcome_screen()

    # -------------------------
    # Screen Builders
    # -------------------------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_welcome_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="🎯 Number Guessing Game", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(self.root, text="Choose Difficulty:", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Easy", width=15, font=("Arial", 12),
                  command=lambda: self.start_game("Easy")).pack(pady=5)
        tk.Button(self.root, text="Normal", width=15, font=("Arial", 12),
                  command=lambda: self.start_game("Normal")).pack(pady=5)
        tk.Button(self.root, text="Hard", width=15, font=("Arial", 12),
                  command=lambda: self.start_game("Hard")).pack(pady=5)

    def build_game_screen(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Difficulty: {self.difficulty['name']}", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.root, text=f"Level {self.level}/{self.difficulty['levels']}", font=("Arial", 12)).pack()
        tk.Label(self.root, text=f"Range: 1 to {self.range_max}", font=("Arial", 12)).pack()

        self.attempts_label = tk.Label(self.root, text=f"Attempts Left: {self.attempts_left}", font=("Arial", 12))
        self.attempts_label.pack(pady=5)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 12))
        self.score_label.pack()

        tk.Label(self.root, text="Enter your guess:", font=("Arial", 12)).pack(pady=10)
        self.guess_entry = tk.Entry(self.root, font=("Arial", 14), justify="center")
        self.guess_entry.pack()
        self.guess_entry.focus()

        tk.Button(self.root, text="Submit Guess", font=("Arial", 12), command=self.check_guess).pack(pady=10)

        self.hint_label = tk.Label(self.root, text="", font=("Arial", 11), fg="blue")
        self.hint_label.pack(pady=10)

        tk.Button(self.root, text="Quit", command=self.root.quit).pack(pady=10)

    # -------------------------
    # Game Setup
    # -------------------------
    def start_game(self, difficulty_name):
        self.difficulty = self.get_difficulty(difficulty_name)
        self.level = 1
        self.score = 0
        self.start_level()

    def get_difficulty(self, name):
        if name == "Easy":
            return {"name": "Easy", "levels": 3, "attempts": 10, "base_range": 10, "hint_type": "direct"}
        elif name == "Normal":
            return {"name": "Normal", "levels": 5, "attempts": 7, "base_range": 50, "hint_type": "mixed"}
        else:
            return {"name": "Hard", "levels": 7, "attempts": 5, "base_range": 100, "hint_type": "riddle"}

    def start_level(self):
        self.range_max = int(self.difficulty["base_range"] * (self.level / self.difficulty["levels"])) + 5
        self.number_to_guess = random.randint(1, self.range_max)
        self.attempts_left = self.difficulty["attempts"]
        self.start_time = time.time()

        self.build_game_screen()

    # -------------------------
    # Hint System
    # -------------------------
    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def get_riddle_hint(self, number):
        clues = []
        if self.is_prime(number):
            clues.append("It’s a prime number.")
        elif int(number ** 0.5) ** 2 == number:
            clues.append("It’s a perfect square.")
        elif number % 5 == 0:
            clues.append("It’s divisible by 5.")
        elif number % 3 == 0:
            clues.append("It’s divisible by 3.")
        elif number % 2 == 0:
            clues.append("It’s an even number.")
        else:
            clues.append("It’s an odd number.")

        if number > 50:
            clues.append("It’s greater than 50.")
        else:
            clues.append("It’s 50 or less.")

        return random.choice(clues)

    def get_adaptive_hint(self, guess, target):
        diff = abs(guess - target)
        if diff == 0:
            return "🎯 Spot on!"
        elif diff <= 3:
            return "🔥 Super hot!"
        elif diff <= 10:
            return "🌡️ Getting warm."
        elif diff <= 20:
            return "❄️ A bit chilly."
        else:
            return "🥶 Freezing cold."

    # -------------------------
    # Game Logic
    # -------------------------
    def check_guess(self):
        guess_text = self.guess_entry.get().strip()
        if not guess_text.isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a valid number.")
            return

        guess = int(guess_text)
        self.attempts_left -= 1
        self.attempts_label.config(text=f"Attempts Left: {self.attempts_left}")

        if guess == self.number_to_guess:
            elapsed = int(time.time() - self.start_time)
            time_bonus = max(0, 10 - elapsed)
            gained = (self.attempts_left * 10) + (self.level * 5) + time_bonus
            self.score += gained

            messagebox.showinfo("Correct!", f"🎉 You cleared Level {self.level}!\n"
                                            f"You earned {gained} points.\n"
                                            f"Total Score: {self.score}")
            self.level += 1
            if self.level > self.difficulty["levels"]:
                self.show_victory_screen()
            else:
                self.start_level()
            return

        # Give adaptive hint
        hint = self.get_adaptive_hint(guess, self.number_to_guess)

        # Apply hint type logic
        if self.difficulty["hint_type"] == "direct":
            hint += " (Higher)" if guess < self.number_to_guess else " (Lower)"
        elif self.difficulty["hint_type"] == "mixed" and self.attempts_left % 2 == 0:
            hint += " (Hint: Higher)" if guess < self.number_to_guess else " (Hint: Lower)"
        elif self.difficulty["hint_type"] == "riddle":
            hint = self.get_riddle_hint(self.number_to_guess)

        self.hint_label.config(text=hint)

        if self.attempts_left <= 0:
            messagebox.showerror("Game Over", "💀 Out of attempts! Restarting from Level 1.")
            self.start_game(self.difficulty["name"])

    def show_victory_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="🏆 You Win!", font=("Arial", 24, "bold"), fg="green").pack(pady=30)
        tk.Label(self.root, text=f"Final Score: {self.score}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Play Again", font=("Arial", 14),
                  command=self.build_welcome_screen).pack(pady=20)
        tk.Button(self.root, text="Quit", font=("Arial", 14), command=self.root.quit).pack(pady=10)


# =========================
# Run the Game
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()
