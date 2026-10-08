import tkinter as tk
from tkinter import messagebox
from game_loader import load_random_word, DIFFICULTY_SETTINGS

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Hangman")
        self.root.geometry("600x550")
        
        self.difficulty = "medium"
        self.reset_game()

        # UI Elements
        self.canvas = tk.Canvas(self.root, width=200, height=200, bg="white")
        self.canvas.pack(pady=10)

        self.word_label = tk.Label(self.root, text="", font=("Helvetica", 20, "bold"))
        self.word_label.pack(pady=10)

        self.info_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.info_label.pack(pady=5)

        # On-screen keyboard frame
        self.keyboard_frame = tk.Frame(self.root)
        self.keyboard_frame.pack(pady=10)
        self.buttons = {}
        self.create_keyboard()

        self.new_game()

    def reset_game(self):
        self.word = load_random_word(self.difficulty)
        self.max_attempts = DIFFICULTY_SETTINGS[self.difficulty]["max_attempts"]
        self.guessed_letters = set()
        self.incorrect_guesses = 0

    def create_keyboard(self):
        letters = "abcdefghijklmnopqrstuvwxyz"
        for i, letter in enumerate(letters):
            btn = tk.Button(
                self.keyboard_frame, text=letter.upper(), width=4, height=2,
                command=lambda l=letter: self.make_guess(l)
            )
            btn.grid(row=i//9, column=i%9, padx=2, pady=2)
            self.buttons[letter] = btn

    def new_game(self):
        self.reset_game()
        self.canvas.delete("all")
        self.draw_gallows()
        self.update_display()
        for btn in self.buttons.values():
            btn.config(state="normal")

    def draw_gallows(self):
        self.canvas.create_line(20, 180, 180, 180, width=3)
        self.canvas.create_line(50, 180, 50, 20, width=3)
        self.canvas.create_line(50, 20, 120, 20, width=3)
        self.canvas.create_line(120, 20, 120, 40, width=2)

    def draw_body_part(self):
        parts = [
            lambda: self.canvas.create_oval(105, 40, 135, 70, width=2),          # Head
            lambda: self.canvas.create_line(120, 70, 120, 120, width=2),        # Body
            lambda: self.canvas.create_line(120, 85, 95, 105, width=2),         # Left Arm
            lambda: self.canvas.create_line(120, 85, 145, 105, width=2),        # Right Arm
            lambda: self.canvas.create_line(120, 120, 95, 155, width=2),        # Left Leg
            lambda: self.canvas.create_line(120, 120, 145, 155, width=2)        # Right Leg
        ]
        if self.incorrect_guesses <= len(parts):
            parts[self.incorrect_guesses - 1]()

    def update_display(self):
        display = [l.upper() if l in self.guessed_letters else "_" for l in self.word]
        self.word_label.config(text=" ".join(display))
        attempts_left = self.max_attempts - self.incorrect_guesses
        self.info_label.config(text=f"Difficulty: {self.difficulty.capitalize()} | Attempts Left: {attempts_left}")

    def make_guess(self, letter):
        self.buttons[letter].config(state="disabled")
        self.guessed_letters.add(letter)

        if letter in self.word:
            self.update_display()
            if all(l in self.guessed_letters for l in self.word):
                messagebox.showinfo("Hangman", "Congratulations! You won!")
                self.new_game()
        else:
            self.incorrect_guesses += 1
            self.draw_body_part()
            self.update_display()
            if self.incorrect_guesses >= self.max_attempts:
                messagebox.showerror("Hangman", f"Game Over! Word was: {self.word}")
                self.new_game()

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()