import colorama
from colorama import Fore, Style
from game_loader import load_random_word, DIFFICULTY_SETTINGS

colorama.init(autoreset=True)

HANGMAN_PICS = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========""", """
       +---+
       |   |
       O   |
           |
           |
           |
    =========""", """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========""", """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========""", """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========""", """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========""", """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    ========="""
]

def play_cli():
    print(f"{Fore.CYAN}=== WELCOME TO HANGMAN ===")
    difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
    if difficulty not in DIFFICULTY_SETTINGS:
        difficulty = "medium"
        
    max_attempts = DIFFICULTY_SETTINGS[difficulty]["max_attempts"]
    word = load_random_word(difficulty)
    guessed_letters = set()
    incorrect_guesses = 0

    while incorrect_guesses < max_attempts:
        # Scale ASCII art stage to remaining attempts
        stage_idx = int((incorrect_guesses / max_attempts) * (len(HANGMAN_PICS) - 1))
        print(Fore.YELLOW + HANGMAN_PICS[stage_idx])

        # Display word with color formatting
        display = [
            f"{Fore.GREEN}{letter}{Style.RESET_ALL}" if letter in guessed_letters else "_"
            for letter in word
        ]
        print("\nWord: " + " ".join(display))
        print(f"Attempts left: {Fore.RED}{max_attempts - incorrect_guesses}")
        print(f"Guessed: {', '.join(sorted(guessed_letters))}\n")

        guess = input("Guess a letter: ").lower().strip()

        if len(guess) != 1 or not guess.isalpha():
            print(f"{Fore.RED}Invalid input. Please enter a single letter.")
            continue
        if guess in guessed_letters:
            print(f"{Fore.YELLOW}You already guessed '{guess}'.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print(f"{Fore.GREEN}Good guess!")
            if all(l in guessed_letters for l in word):
                print(f"\n{Fore.GREEN}🎉 You won! The word was: {word}")
                break
        else:
            incorrect_guesses += 1
            print(f"{Fore.RED}Wrong guess!")
    else:
        print(Fore.RED + HANGMAN_PICS[-1])
        print(f"\n{Fore.RED}Game Over! The word was: {word}")

if __name__ == "__main__":
    play_cli()