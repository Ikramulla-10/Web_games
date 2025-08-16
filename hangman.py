import tkinter as tk
import random
import os

# Load words from file or use default
def load_words():
    if os.path.exists("words.txt"):
        with open("words.txt", "r") as f:
            return [line.strip().lower() for line in f if line.strip()]
    return ['python', 'hangman', 'developer', 'function', 'variable', 'interface']

# Setup game
def start_game(difficulty='medium'):
    global word, word_letters, guessed_letters, lives, max_lives
    guessed_letters = set()

    word = random.choice(load_words())
    word_letters = set(word)

    difficulty_levels = {
        'easy': 10,
        'medium': 6,
        'hard': 4
    }
    max_lives = lives = difficulty_levels.get(difficulty, 6)

    entry.config(state='normal')
    guess_button.config(state='normal')
    entry.delete(0, tk.END)

    result_label.config(text="")
    canvas.delete("all")
    draw_base()
    update_display()

# Display word progress
def get_display_word():
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

# Handle guesses
def guess_letter():
    global lives
    letter = entry.get().lower()
    entry.delete(0, tk.END)

    if not letter or len(letter) != 1 or not letter.isalpha():
        result_label.config(text="Enter a single letter.")
        return

    if letter in guessed_letters:
        result_label.config(text="Already guessed.")
        return

    guessed_letters.add(letter)

    if letter in word_letters:
        word_letters.remove(letter)
        result_label.config(text="Correct!")
    else:
        lives -= 1
        result_label.config(text="Wrong!")
        draw_hangman()

    update_display()

    if lives == 0:
        result_label.config(text=f"You lost! Word was: {word}")
        entry.config(state='disabled')
        guess_button.config(state='disabled')
    elif not word_letters:
        result_label.config(text=f"You won! Word: {word}")
        entry.config(state='disabled')
        guess_button.config(state='disabled')

# Update UI
def update_display():
    word_label.config(text=get_display_word())
    lives_label.config(text=f"Lives left: {lives}")
    guessed_label.config(text="Guessed: " + ' '.join(sorted(guessed_letters)))

# Drawing base and stick figure
def draw_base():
    canvas.create_line(20, 180, 120, 180)     # base
    canvas.create_line(70, 180, 70, 20)       # pole
    canvas.create_line(70, 20, 130, 20)       # top beam
    canvas.create_line(130, 20, 130, 40)      # rope

def draw_hangman():
    parts = [
        lambda: canvas.create_oval(115, 40, 145, 70),        # head
        lambda: canvas.create_line(130, 70, 130, 110),       # body
        lambda: canvas.create_line(130, 80, 110, 100),       # left arm
        lambda: canvas.create_line(130, 80, 150, 100),       # right arm
        lambda: canvas.create_line(130, 110, 110, 140),      # left leg
        lambda: canvas.create_line(130, 110, 150, 140),      # right leg
    ]
    part_index = max_lives - lives - 1
    if part_index < len(parts):
        parts[part_index]()

# Start new game from dropdown
def start_new_difficulty(event=None):
    level = difficulty_var.get()
    start_game(level)

# GUI setup
root = tk.Tk()
root.title("Hangman Game")
root.geometry("500x450")

difficulty_var = tk.StringVar(value='medium')
difficulty_menu = tk.OptionMenu(root, difficulty_var, 'easy', 'medium', 'hard', command=start_new_difficulty)
difficulty_menu.pack(pady=5)

canvas = tk.Canvas(root, width=200, height=200, bg='white')
canvas.pack()

word_label = tk.Label(root, text='', font=('Helvetica', 24))
word_label.pack(pady=10)

entry = tk.Entry(root, font=('Helvetica', 16), justify='center')
entry.pack()

guess_button = tk.Button(root, text="Guess", command=guess_letter)
guess_button.pack(pady=5)

result_label = tk.Label(root, text="", font=('Helvetica', 12))
result_label.pack()

lives_label = tk.Label(root, text="", font=('Helvetica', 12))
lives_label.pack()

guessed_label = tk.Label(root, text="", font=('Helvetica', 12))
guessed_label.pack()

restart_button = tk.Button(root, text="Restart Game", command=lambda: start_game(difficulty_var.get()))
restart_button.pack(pady=10)

start_game()
root.mainloop()