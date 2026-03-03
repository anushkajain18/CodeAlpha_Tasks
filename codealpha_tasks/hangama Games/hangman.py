import tkinter as tk
import random
from tkinter import messagebox

# -------------------------------------------------
# WORD BANK (PREDEFINED – FAST & STABLE)
# -------------------------------------------------
word_bank = {
    "animals": {
        "easy": [
            "cat", "dog", "cow", "pig", "rat", "bat", "fox", "hen", "ant", "bee",
            "duck", "goat", "sheep", "horse", "deer", "frog", "fish", "crab"
        ],
        "medium": [
            "tiger", "lion", "zebra", "monkey", "elephant", "giraffe",
            "kangaroo", "leopard", "cheetah", "buffalo", "camel",
            "dolphin", "penguin", "crocodile", "squirrel", "hamster"
        ],
        "hard": [
            "hippopotamus", "rhinoceros", "orangutan", "chimpanzee",
            "alligator", "porcupine", "armadillo", "platypus",
            "salamander", "hedgehog", "chameleon"
        ]
    },

    "tech": {
        "easy": [
            "code", "data", "java", "loop", "array", "class", "object",
            "logic", "debug", "stack", "queue", "binary"
        ],
        "medium": [
            "python", "server", "network", "database", "algorithm",
            "compiler", "software", "hardware", "variable", "function",
            "frontend", "backend", "framework"
        ],
        "hard": [
            "microprocessor", "cryptography", "virtualization",
            "multithreading", "authentication", "serialization",
            "containerization", "orchestration", "loadbalancing"
        ]
    },

    "fruits": {
        "easy": [
            "apple", "banana", "mango", "pear", "grape", "peach",
            "plum", "kiwi", "lemon", "lime", "melon", "berry"
        ],
        "medium": [
            "papaya", "pineapple", "strawberry", "blueberry",
            "raspberry", "watermelon", "pomegranate",
            "coconut", "avocado"
        ],
        "hard": [
            "dragonfruit", "passionfruit", "cranberry",
            "jackfruit", "blackcurrant", "gooseberry",
            "mulberry", "boysenberry"
        ]
    }
}

# -------------------------------------------------
# GAME STATE VARIABLES
# -------------------------------------------------
word = ""
guessed_letters = []
attempts = 0
score = 0
hint_used = False
game_started = False

# -------------------------------------------------
# GAME LOGIC FUNCTIONS
# -------------------------------------------------
def start_game():
    global word, attempts, score, hint_used, game_started

    category = category_var.get()
    difficulty = difficulty_var.get()

    if not category or not difficulty:
        messagebox.showwarning("Hangman", "Please select category and difficulty")
        return

    guessed_letters.clear()
    hint_used = False
    score = 0
    game_started = True

    attempts = {"easy": 8, "medium": 6, "hard": 4}[difficulty]
    word = random.choice(word_bank[category][difficulty])

    update_word_display()
    attempts_label.config(text=f"Attempts: {attempts}")
    score_label.config(text=f"Score: {score}")

def update_word_display():
    display = " ".join(letter if letter in guessed_letters else "_" for letter in word)
    word_label.config(text=display)

    if "_" not in display and game_started:
        messagebox.showinfo("Hangman", "🎉 Congratulations! You won!")
        score_label.config(text=f"Score: {score + 50}")

def guess_letter(letter):
    global attempts, score

    if not game_started or attempts == 0 or letter in guessed_letters:
        return

    guessed_letters.append(letter)

    if letter in word:
        score += 10
    else:
        attempts -= 1
        score -= 5

    update_word_display()
    attempts_label.config(text=f"Attempts: {attempts}")
    score_label.config(text=f"Score: {score}")

    if attempts == 0:
        messagebox.showerror("Hangman", f"💀 Game Over!\nWord was: {word}")

def use_hint():
    global hint_used

    if hint_used or not game_started:
        return

    for letter in word:
        if letter not in guessed_letters:
            guessed_letters.append(letter)
            hint_used = True
            update_word_display()
            break

def restart_game():
    global game_started
    game_started = False
    category_var.set("")
    difficulty_var.set("")
    word_label.config(text="")
    attempts_label.config(text="Attempts: 0")
    score_label.config(text="Score: 0")

# -------------------------------------------------
# GUI SETUP
# -------------------------------------------------
root = tk.Tk()
root.title("Hangman Game")
root.geometry("520x620")
root.resizable(False, False)

tk.Label(root, text="🎯 Hangman Game", font=("Arial", 22, "bold")).pack(pady=10)

category_var = tk.StringVar()
difficulty_var = tk.StringVar()

tk.Label(root, text="Select Category").pack()
tk.OptionMenu(root, category_var, *word_bank.keys()).pack()

tk.Label(root, text="Select Difficulty").pack()
tk.OptionMenu(root, difficulty_var, "easy", "medium", "hard").pack()

tk.Button(
    root,
    text="▶ Start Game",
    font=("Arial", 12, "bold"),
    command=start_game
).pack(pady=10)

word_label = tk.Label(root, font=("Arial", 26))
word_label.pack(pady=15)

attempts_label = tk.Label(root, text="Attempts: 0")
attempts_label.pack()

score_label = tk.Label(root, text="Score: 0")
score_label.pack()

tk.Button(root, text="💡 Hint (One Time)", command=use_hint).pack(pady=4)
tk.Button(root, text="🔁 Restart Game", command=restart_game).pack(pady=4)

# Alphabet Buttons
letters_frame = tk.Frame(root)
letters_frame.pack(pady=10)

for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz"):
    tk.Button(
        letters_frame,
        text=letter.upper(),
        width=4,
        command=lambda l=letter: guess_letter(l)
    ).grid(row=i // 7, column=i % 7, padx=2, pady=2)

root.mainloop()
