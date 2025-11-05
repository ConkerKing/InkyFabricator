import random
import sys
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


# ================================
# Utility Functions
# ================================
def slow_print(text, delay=0.03):
    """Print text slowly for dramatic effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def countdown_timer(seconds):
    """Simple countdown timer."""
    for i in range(seconds, 0, -1):
        print(Fore.CYAN + f"⏳ Time left: {i} sec", end="\r")
        time.sleep(1)
    print(Style.RESET_ALL)


def get_ascii_banner():
    """Return a fancy ASCII banner."""
    return f"""{Fore.YELLOW}
 _   _                 _                  _____                      
| \\ | |               | |                / ____|                     
|  \\| |_   _ _ __ ___ | |__   ___ _ __  | |  __ _   _  ___  ___  ___ 
| . ` | | | | '_ ` _ \\| '_ \\ / _ \\ '__| | | |_ | | | |/ _ \\/ _ \\/ __|
| |\\  | |_| | | | | | | |_) |  __/ |    | |__| | |_| |  __/  __/\\__ \\
|_| \\_|\\__,_|_| |_| |_|_.__/ \\___|_|     \\_____|\\__,_|\\___|\\___||___/
{Style.RESET_ALL}"""


def get_victory_banner():
    """Return ASCII art for victory."""
    return f"""{Fore.GREEN}
__     ______  _    _   _      ____   _    _   _ 
\\ \\   / / __ \\| |  | | | |    / __ \\ /\\ \\  | | | |
 \\ \\_/ / |  | | |  | | | |   | |  | /  \\ \\ | |_| |
  \\   /| |  | | |  | | | |   | |  |/ /\\ \\ \\|  _  |
   | | | |__| | |__| | | |___| |_/ / ____ \\ | | | |
   |_|  \\____/ \\____/  |______\\____/_/    \\_\\_| |_|
{Style.RESET_ALL}"""


# ================================
# Riddle and Hint System
# ================================
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def get_riddle_hint(number):
    """Enhanced riddle-style hints for Hard mode."""
    clues = []

    if is_prime(number):
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

    if number < 10:
        clues.append("It’s a single-digit number.")
    elif number >= 90:
        clues.append("It’s close to 100.")

    return random.choice(clues)


def get_adaptive_hint(guess, target):
    """Give adaptive hot/cold hints based on distance."""
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


# ================================
# Difficulty and Game Logic
# ================================
def select_difficulty():
    slow_print("\nSelect a difficulty:")
    slow_print("1. Easy")
    slow_print("2. Normal")
    slow_print("3. Hard")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        print("Invalid input. Please enter 1, 2, or 3.")


def setup_difficulty(choice):
    """Configure difficulty settings."""
    if choice == "1":
        return {
            "name": "Easy",
            "levels": 3,
            "attempts": 10,
            "base_range": 10,
            "hint_type": "direct",
            "timer": 0
        }
    elif choice == "2":
        return {
            "name": "Normal",
            "levels": 5,
            "attempts": 7,
            "base_range": 50,
            "hint_type": "mixed",
            "timer": 25
        }
    else:
        return {
            "name": "Hard",
            "levels": 7,
            "attempts": 5,
            "base_range": 100,
            "hint_type": "riddle",
            "timer": 20
        }


def play_level(level, difficulty, score):
    """Play a single level and return (success, new_score)."""
    level_range = int(difficulty["base_range"] * (level / difficulty["levels"])) + 5
    number_to_guess = random.randint(1, level_range)
    attempts_left = difficulty["attempts"]
    start_time = time.time()

    slow_print(f"\n{Fore.CYAN}Level {level} — Range: 1 to {level_range}")
    slow_print(f"You have {attempts_left} attempts!")

    while attempts_left > 0:
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")
            continue

        if guess == number_to_guess:
            elapsed = int(time.time() - start_time)
            time_bonus = max(0, 10 - elapsed)
            gained = (attempts_left * 10) + (level * 5) + time_bonus
            score += gained

            slow_print(Fore.GREEN + f"🎉 Correct! You cleared Level {level}!")
            slow_print(Fore.YELLOW + f"🏅 You earned {gained} points (Total: {score})")
            return True, score

        attempts_left -= 1
        print(Fore.MAGENTA + get_adaptive_hint(guess, number_to_guess))

        if difficulty["hint_type"] == "direct":
            if guess < number_to_guess:
                print("Too low! Try higher.")
            else:
                print("Too high! Try lower.")
        elif difficulty["hint_type"] == "mixed" and attempts_left % 2 == 0:
            if guess < number_to_guess:
                print("Hint: The number is higher.")
            else:
                print("Hint: The number is lower.")
        elif difficulty["hint_type"] == "riddle":
            print(Fore.BLUE + get_riddle_hint(number_to_guess))

        print(Fore.CYAN + f"Attempts left: {attempts_left}")

        if difficulty["timer"]:
            elapsed = int(time.time() - start_time)
            if elapsed > difficulty["timer"]:
                slow_print(Fore.RED + "\n⏰ Time’s up! You ran out of time.")
                return False, score

    slow_print(Fore.RED + "\n💀 Out of attempts! Game over.")
    return False, score


def play_game():
    """Main game loop."""
    print(get_ascii_banner())
    slow_print("🎯 Welcome to the Number Guessing Game — Deluxe Edition!\n")

    difficulty_choice = select_difficulty()
    difficulty = setup_difficulty(difficulty_choice)

    slow_print(f"\nYou selected {difficulty['name']} mode.")
    slow_print("Let's begin!\n")

    score = 0

    for level in range(1, difficulty["levels"] + 1):
        success, score = play_level(level, difficulty, score)
        if not success:
            slow_print(Fore.RED + "Restarting from Level 1...")
            return play_game()

    slow_print(get_victory_banner())
    slow_print(Fore.YELLOW + f"🏆 Final Score: {score}")
    slow_print("Thanks for playing!\n")
    sys.exit()


if __name__ == "__main__":
    play_game()
