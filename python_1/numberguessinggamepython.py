import random
import sys
import time


def slow_print(text, delay=0.03):
    """Print text slowly for effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()




def get_riddle_hint(number):
    """Generate a riddle-like hint for the hard difficulty."""
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




def select_difficulty():
    """Prompt player to choose a difficulty level."""
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
    """Configure settings based on chosen difficulty."""
    if choice == "1":
        return {
            "name": "Easy",
            "levels": 3,
            "attempts": 10,
            "base_range": 10,
            "hint_type": "direct"
        }
    elif choice == "2":
        return {
            "name": "Normal",
            "levels": 5,
            "attempts": 7,
            "base_range": 50,
            "hint_type": "mixed"
        }
    else:
        return {
            "name": "Hard",
            "levels": 7,
            "attempts": 5,
            "base_range": 100,
            "hint_type": "riddle"
        }




def play_level(level, difficulty):
    """Play one level of the game."""
    level_range = difficulty["base_range"] * (level / difficulty["levels"])
    number_to_guess = random.randint(1, int(level_range))
    attempts_left = difficulty["attempts"]
    wrong_attempts = 0


    slow_print(f"\nLevel {level} — Range: 1 to {int(level_range)}")
    slow_print(f"You have {attempts_left} attempts!")


    while attempts_left > 0:
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Please enter a valid number.")
            continue


        if guess == number_to_guess:
            slow_print(f"🎉 Correct! You cleared Level {level}!")
            return True


        attempts_left -= 1
        wrong_attempts += 1


        if difficulty["hint_type"] == "direct":
            if guess < number_to_guess:
                print("Too low! Try higher.")
            else:
                print("Too high! Try lower.")


        elif difficulty["hint_type"] == "mixed":
            if wrong_attempts % 2 == 0:
                if guess < number_to_guess:
                    print("Hint: The number is higher.")
                else:
                    print("Hint: The number is lower.")
            else:
                print("No hint this time!")


        elif difficulty["hint_type"] == "riddle":
            print(get_riddle_hint(number_to_guess))


        print(f"Attempts left: {attempts_left}")


    # Out of attempts
    slow_print("\n💀 Out of attempts! Game over.")
    return False




def play_game():
    """Main game loop."""
    slow_print("🎯 Welcome to the Number Guessing Game!")
    slow_print("Try to guess the secret number before you run out of attempts.\n")


    difficulty_choice = select_difficulty()
    difficulty = setup_difficulty(difficulty_choice)


    slow_print(f"\nYou selected {difficulty['name']} mode.")
    slow_print("Let's begin!\n")


    for level in range(1, difficulty["levels"] + 1):
        success = play_level(level, difficulty)
        if not success:
            slow_print("Restarting from Level 1...")
            return play_game()  # Restart game


    # Player completes all levels
    slow_print("\n🏆 Congratulations! You completed all levels!")
    slow_print("Thanks for playing!\n")
    sys.exit()




if __name__ == "__main__":
    play_game()