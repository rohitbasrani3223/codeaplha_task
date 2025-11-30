"""
Hangman Ultimate — Dark + Neon themes, Categories, Combo Difficulty, Achievements & Persistent Scores
Author: gamerdsh (as requested)
Run: python hangman_ultimate.py
"""

import json
import os
import random
import time
import tkinter as tk
from tkinter import messagebox

# ---------------------- Persistent Data ----------------------
DATA_FILE = "hangman_scores.json"
MAX_SCORE = 100

def load_scores():
    if not os.path.exists(DATA_FILE):
        return {"games": 0, "wins": 0, "losses": 0, "points": 0, "streak": 0, "best_streak": 0, "highscore": 0}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"games": 0, "wins": 0, "losses": 0, "points": 0, "streak": 0, "best_streak": 0, "highscore": 0}

def save_scores(scores):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(scores, f)
    except Exception:
        pass

# ---------------------- Word Data (Categories) ----------------------
ANIMALS = {
    "ant": "A small insect that lives in colonies.",
    "baboon": "A monkey found in Africa.",
    "bat": "A nocturnal flying mammal.",
    "bear": "A large mammal that may hibernate.",
    "camel": "An animal with humps found in deserts.",
    "cat": "A common household pet.",
    "cobra": "A venomous snake that can spread a hood.",
    "crow": "A black bird known for intelligence.",
    "dog": "A loyal pet often called man's best friend.",
    "eagle": "A bird of prey with excellent eyesight.",
    "fox": "A clever animal with a bushy tail.",
    "lion": "The king of the jungle.",
    "monkey": "A playful mammal that likes trees.",
    "panda": "A black and white bear from China.",
    "python": "A large non-venomous snake.",
    "shark": "A powerful fish with sharp teeth.",
    "sheep": "An animal known for wool.",
    "spider": "An arachnid that spins webs.",
    "tiger": "A striped big cat.",
    "wolf": "A wild canine that hunts in packs.",
    "zebra": "An African horse-like animal with black & white stripes."
}

FRUITS = {
    "apple": "Keeps the doctor away (famous phrase).",
    "banana": "Long yellow fruit, great source of potassium.",
    "cherry": "Small red fruit often on top of desserts.",
    "date": "Sweet fruit often eaten dried.",
    "fig": "A soft fruit with many tiny seeds.",
    "grape": "Small juicy fruit, used to make wine.",
    "lemon": "Sour yellow citrus fruit.",
    "mango": "Sweet tropical stone fruit.",
    "orange": "Citrus fruit known for vitamin C.",
    "papaya": "Tropical fruit with orange flesh.",
    "peach": "Fuzzy skin and sweet interior.",
    "pear": "Juicy fruit with a bell shape.",
    "plum": "Sweet stone fruit with smooth skin.",
    "kiwi": "Brown fuzzy outside, green inside.",
    "melon": "Large juicy fruit, many varieties.",
}

CATEGORIES = {
    "Animals": ANIMALS,
    "Fruits": FRUITS,
    "Random": {**ANIMALS, **FRUITS}
}

# ---------------------- Themes (Dark & Neon) ----------------------
THEMES = {
    "Dark": {
        "bg": "#0b1220",
        "fg": "#cfe8ff",
        "accent": "#6fb3ff",
        "idle": "#20304a",
        "correct": "#2ecc71",
        "wrong": "#ff6b6b",
        "banner_colors": ["#cfe8ff", "#9fbfff", "#6fb3ff"]
    },
    "Neon": {
        "bg": "#04070a",
        "fg": "#e0f7ff",
        "accent": "#00ffd5",
        "idle": "#0b1320",
        "correct": "#39ff14",
        "wrong": "#ff3b81",
        "banner_colors": ["#00ffd5", "#b300ff", "#ff3b81"]
    }
}

# ---------------------- Difficulty (Combo Mode) ----------------------
# We implement Combo mode: difficulty influences word length, number of tries, and hint timing
DIFFICULTY_SETTINGS = {
    "Easy": {"max_tries": 8, "min_len": 3, "max_len": 6, "hint_delay": 0},      # hint available immediately
    "Medium": {"max_tries": 6, "min_len": 5, "max_len": 8, "hint_delay": 1},    # hint available after 1 wrong guess
    "Hard": {"max_tries": 4, "min_len": 7, "max_len": 20, "hint_delay": 2},     # hint hidden until last 2 tries left
}

# ---------------------- Hangman Game Class ----------------------
class HangmanGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Hangman Ultimate — by gamerdsh")
        # optional: set icon .ico if present
        try:
            self.root.iconbitmap("game_icon.ico")
        except Exception:
            pass
        self.root.geometry("880x720")
        self.root.resizable(False, False)

        # initial theme, load scores
        self.theme_name = "Dark"
        self.theme = THEMES[self.theme_name]
        self.scores = load_scores()

        # game state
        self.category_name = "Random"
        self.word_hints = CATEGORIES[self.category_name]
        self.secret_word = ""
        self.hint = ""
        self.correct_indices = []  # list of booleans for each char index
        self.guessed_letters = set()
        self.missed_letters = []
        self.max_tries = 6
        self.difficulty = "Medium"
        self.round_start_time = 0
        self.win_streak = 0

        # build UI
        self._build_gui()
        self.new_game()

        # key binding
        self.root.bind("<Key>", self._on_keypress)

    # ---------- UI Building ----------
    def _build_gui(self):
        self.root.configure(bg=self.theme["bg"])

        # Header banner (animated colors)
        top = tk.Frame(self.root, bg=self.theme["bg"])
        top.pack(pady=8)
        self.banner = tk.Label(top, text="HANGMAN ULTIMATE", font=("Helvetica", 32, "bold"),
                               fg=self.theme["fg"], bg=self.theme["bg"])
        self.banner.pack()
        self._animate_banner(0)

        # Controls row: Theme, Category, Difficulty
        ctrl = tk.Frame(self.root, bg=self.theme["bg"])
        ctrl.pack(pady=6)

        tk.Label(ctrl, text="Theme:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=0, column=0, padx=6)
        self.theme_var = tk.StringVar(value=self.theme_name)
        tk.OptionMenu(ctrl, self.theme_var, *THEMES.keys(), command=self._on_theme_change).grid(row=0, column=1)

        tk.Label(ctrl, text="Category:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=0, column=2, padx=6)
        self.category_var = tk.StringVar(value=self.category_name)
        tk.OptionMenu(ctrl, self.category_var, *CATEGORIES.keys(), command=self._on_category_change).grid(row=0, column=3)

        tk.Label(ctrl, text="Difficulty:", bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=0, column=4, padx=6)
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        tk.OptionMenu(ctrl, self.difficulty_var, "Easy", "Medium", "Hard", command=self._on_difficulty_change).grid(row=0, column=5)

        # Canvas for drawing
        self.canvas = tk.Canvas(self.root, width=380, height=380, bg=self.theme["bg"], highlightthickness=0)
        self.canvas.pack(pady=6)

        # Word display + hint + missed + score
        info = tk.Frame(self.root, bg=self.theme["bg"])
        info.pack(pady=4)

        self.word_label = tk.Label(info, text="", font=("Consolas", 28, "bold"), fg=self.theme["fg"], bg=self.theme["bg"])
        self.word_label.grid(row=0, column=0, columnspan=3, pady=6)

        self.hint_label = tk.Label(info, text="Hint: ???", font=("Arial", 12, "italic"), fg=self.theme["accent"], bg=self.theme["bg"])
        self.hint_label.grid(row=1, column=0, sticky="w", padx=6)

        self.missed_label = tk.Label(info, text="Missed: ", font=("Arial", 12), fg=self.theme["wrong"], bg=self.theme["bg"])
        self.missed_label.grid(row=1, column=1, sticky="w", padx=6)

        self.score_label = tk.Label(info, text=f"Points: {self.scores.get('points',0)}", font=("Arial", 12, "bold"), fg=self.theme["fg"], bg=self.theme["bg"])
        self.score_label.grid(row=1, column=2, sticky="e", padx=6)

        # Alphabet buttons
        letters = tk.Frame(self.root, bg=self.theme["bg"])
        letters.pack(pady=8)
        self.letter_buttons = {}
        for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = tk.Button(letters, text=ch, width=4, font=("Arial", 11, "bold"),
                            bg=self.theme["idle"], fg=self.theme["fg"],
                            command=lambda c=ch: self.guess_letter(c.lower()))
            btn.grid(row=i//9, column=i%9, padx=3, pady=3)
            self.letter_buttons[ch] = btn

        # Bottom controls: hint, new game, scoreboard, reset
        bottom = tk.Frame(self.root, bg=self.theme["bg"])
        bottom.pack(pady=6)
        self.hint_btn = tk.Button(bottom, text="Show Hint", command=self.reveal_hint, bg=self.theme["idle"])
        self.hint_btn.grid(row=0, column=0, padx=6)
        tk.Button(bottom, text="New Game", command=self.new_game, bg=self.theme["accent"]).grid(row=0, column=1, padx=6)
        tk.Button(bottom, text="View Scoreboard", command=self.show_scoreboard, bg=self.theme["idle"]).grid(row=0, column=2, padx=6)
        tk.Button(bottom, text="Reset Scores", command=self.reset_scores, bg=self.theme["idle"]).grid(row=0, column=3, padx=6)

        # Achievements text area
        self.achievement_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"), fg=self.theme["accent"], bg=self.theme["bg"])
        self.achievement_label.pack(pady=6)

    # ---------- Theme & small animations ----------
    def _on_theme_change(self, new_theme):
        self.theme_name = new_theme
        self.theme = THEMES[self.theme_name]
        self._recolor_ui()

    def _recolor_ui(self):
        # recolor main widgets
        self.root.configure(bg=self.theme["bg"])
        self.banner.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.canvas.config(bg=self.theme["bg"])
        self.word_label.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.hint_label.config(bg=self.theme["bg"], fg=self.theme["accent"])
        self.missed_label.config(bg=self.theme["bg"], fg=self.theme["wrong"])
        self.score_label.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.achievement_label.config(bg=self.theme["bg"], fg=self.theme["accent"])
        for btn in self.letter_buttons.values():
            btn.config(bg=self.theme["idle"], fg=self.theme["fg"])

    def _animate_banner(self, step):
        colors = self.theme["banner_colors"]
        self.banner.config(fg=colors[step % len(colors)])
        self.root.after(500, lambda: self._animate_banner(step+1))

    def _flash_button(self, key, correct=True):
        btn = self.letter_buttons.get(key.upper())
        if not btn:
            return
        color = self.theme["correct"] if correct else self.theme["wrong"]
        btn.config(bg=color, state=tk.DISABLED)
        self.root.after(400, lambda: btn.config(bg=self.theme["idle"]))

    # ---------- Category & Difficulty handlers ----------
    def _on_category_change(self, new_cat):
        self.category_name = new_cat
        self.word_hints = CATEGORIES[self.category_name]
        self.new_game()

    def _on_difficulty_change(self, new_diff):
        self.difficulty = new_diff
        self.new_game()

    # ---------- Game flow ----------
    def new_game(self):
        # choose word pool by difficulty and category
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        pool = [w for w in self.word_hints.keys() if settings["min_len"] <= len(w) <= settings["max_len"]]
        if not pool:
            pool = list(self.word_hints.keys())
        self.secret_word = random.choice(pool).lower()
        self.hint = self.word_hints.get(self.secret_word, "No hint available.")
        # track revealed indices separately (False = hidden)
        self.correct_indices = [False] * len(self.secret_word)
        self.guessed_letters = set()
        self.missed_letters = []
        self.max_tries = settings["max_tries"]
        self.round_start_time = time.time()
        # reset buttons
        for btn in self.letter_buttons.values():
            btn.config(state=tk.NORMAL, bg=self.theme["idle"])
        # update displays
        self._update_display()
        self._draw_gallows()
        self.hint_label.config(text="Hint: ???" if settings["hint_delay"] > 0 and self.difficulty=="Hard" else f"Hint: {self.hint if settings['hint_delay']==0 else '???'}")
        # small round info
        self._show_temp_info(f"Category: {self.category_name}  |  Difficulty: {self.difficulty}")

    def reveal_hint(self):
        # reveal only if allowed by difficulty timing rules
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        # For Hard, hint is hidden until last 2 tries left => allowed if remaining tries <=2
        remaining = self.max_tries - len(self.missed_letters)
        if self.difficulty == "Hard" and remaining > 2:
            messagebox.showinfo("Hint Locked", "Hint is locked in Hard difficulty until you have 2 tries left.")
            return
        self.hint_label.config(text=f"Hint: {self.hint}")

    def guess_letter(self, letter):
        # prevent repeated guesses
        if letter in self.guessed_letters:
            return
        self.guessed_letters.add(letter)
        # correct?
        if letter in self.secret_word:
            # reveal ALL positions (standard rule) but for extra challenge we could reveal one by one; using standard reveal for fairness
            for i, ch in enumerate(self.secret_word):
                if ch == letter:
                    self.correct_indices[i] = True
            self._flash_button(letter, correct=True)
        else:
            self.missed_letters.append(letter)
            self._flash_button(letter, correct=False)

        self._update_display()
        self._draw_hangman(len(self.missed_letters))

        # check win / lose
        if self._check_win():
            self._on_win()
        elif len(self.missed_letters) >= self.max_tries:
            self._on_loss()

    def _on_win(self):
        elapsed = time.time() - self.round_start_time
        # points = base by difficulty + bonus for speed and no-mistake
        base = {"Easy": 8, "Medium": 12, "Hard": 20}[self.difficulty]
        speed_bonus = max(0, int((30 - elapsed) // 5))  # small bonus for quick wins
        no_mistake_bonus = 10 if len(self.missed_letters) == 0 else 0
        points = base + speed_bonus + no_mistake_bonus
        self.scores["games"] = self.scores.get("games", 0) + 1
        self.scores["wins"] = self.scores.get("wins", 0) + 1
        self.scores["points"] = self.scores.get("points", 0) + points
        self.scores["streak"] = self.scores.get("streak", 0) + 1
        self.scores["best_streak"] = max(self.scores.get("best_streak", 0), self.scores.get("streak", 0))
        if self.scores["points"] > self.scores.get("highscore", 0):
            self.scores["highscore"] = self.scores["points"]
        save_scores(self.scores)
        self._update_score_label()
        # Achievements
        if no_mistake_bonus:
            self._show_achievement("No Mistakes!", f"You got it perfectly +{points} pts")
        if self.scores["streak"] >= 3:
            self._show_achievement("Hot Streak!", f"{self.scores['streak']} wins in a row!")
        if elapsed <= 10:
            self._show_achievement("Speedy!", f"Quick win in {int(elapsed)}s")
        messagebox.showinfo("You Win!", f"Well done! The word was '{self.secret_word}'.\nPoints: {points}")
        self.new_game()

    def _on_loss(self):
        self.scores["games"] = self.scores.get("games", 0) + 1
        self.scores["losses"] = self.scores.get("losses", 0) + 1
        self.scores["streak"] = 0
        save_scores(self.scores)
        self._update_score_label()
        self._show_achievement("Game Over", f"The word was '{self.secret_word}'")
        messagebox.showerror("Game Over", f"You ran out of tries. The word was: {self.secret_word}")
        self.new_game()

    # ---------- Display helpers ----------
    def _update_display(self):
        # join with spaces
        shown = " ".join(self.secret_word[i].upper() if self.correct_indices[i] else "_" for i in range(len(self.secret_word)))
        self.word_label.config(text=shown)
        self.missed_label.config(text="Missed: " + " ".join(self.missed_letters))
        self.hint_label.update()
        self._update_score_label()

    def _update_score_label(self):
        self.score_label.config(text=f"Points: {self.scores.get('points',0)}  |  Wins: {self.scores.get('wins',0)}")

    def _check_win(self):
        return all(self.correct_indices)

    def _show_achievement(self, title, text=""):
        # animate achievement label briefly
        self.achievement_label.config(text=f"{title}: {text}")
        self.root.after(2200, lambda: self.achievement_label.config(text=""))

    def _show_temp_info(self, text, ms=1400):
        # small text on canvas temporarily
        t = self.canvas.create_text(190, 350, text=text, fill=self.theme["fg"], font=("Arial", 10, "italic"), tags="temp")
        self.root.after(ms, lambda: self.canvas.delete(t))

    # ---------- Drawing (gallows + character) ----------
    def _draw_gallows(self):
        self.canvas.delete("all")
        c = self.canvas
        # base
        c.create_line(40, 340, 340, 340, width=4, fill=self.theme["fg"])
        c.create_line(80, 340, 80, 60, width=4, fill=self.theme["fg"])
        c.create_line(80, 60, 220, 60, width=4, fill=self.theme["fg"])
        c.create_line(220, 60, 220, 90, width=4, fill=self.theme["fg"])
        c.create_text(190, 20, text=f"Style: {self.theme_name} | Cat: {self.category_name}", fill=self.theme["fg"], font=("Arial", 10, "italic"))

    def _draw_hangman(self, step):
        # draws up to 6 parts depending on step
        c = self.canvas
        # head
        if step >= 1:
            c.create_oval(200, 90, 240, 130, width=2, outline=self.theme["fg"])
        # body
        if step >= 2:
            c.create_line(220, 130, 220, 190, width=2, fill=self.theme["fg"])
        # left arm
        if step >= 3:
            c.create_line(220, 140, 190, 165, width=2, fill=self.theme["fg"])
        # right arm
        if step >= 4:
            c.create_line(220, 140, 250, 165, width=2, fill=self.theme["fg"])
        # left leg
        if step >= 5:
            c.create_line(220, 190, 195, 230, width=2, fill=self.theme["fg"])
        # right leg
        if step >= 6:
            c.create_line(220, 190, 245, 230, width=2, fill=self.theme["fg"])

    # ---------- Keyboard binding ----------
    def _on_keypress(self, event):
        ch = event.char.lower()
        if ch.isalpha() and len(ch) == 1:
            if ch in self.guessed_letters:
                return
            # simulate button press visually
            btn = self.letter_buttons.get(ch.upper())
            if btn and btn["state"] == tk.NORMAL:
                btn.config(relief=tk.SUNKEN)
                self.root.after(120, lambda b=btn: b.config(relief=tk.RAISED))
            self.guess_letter(ch)

    # ---------- Scoreboard UI ----------
    def show_scoreboard(self):
        wins = self.scores.get("wins", 0)
        losses = self.scores.get("losses", 0)
        games = self.scores.get("games", 0)
        points = self.scores.get("points", 0)
        streak = self.scores.get("streak", 0)
        best = self.scores.get("best_streak", 0)
        high = self.scores.get("highscore", 0)
        accuracy = (wins / games * 100) if games else 0.0

        msg = (
            f"Games: {games}\n"
            f"Wins: {wins}\n"
            f"Losses: {losses}\n"
            f"Points: {points}\n"
            f"Accuracy: {accuracy:.1f}%\n"
            f"Current Streak: {streak}\n"
            f"Best Streak: {best}\n"
            f"High Score: {high}"
        )
        messagebox.showinfo("📊 Scoreboard", msg)

    def reset_scores(self):
        if not messagebox.askyesno("Reset Scores", "Are you sure you want to reset saved scores?"):
            return
        self.scores = {"games": 0, "wins": 0, "losses": 0, "points": 0, "streak": 0, "best_streak": 0, "highscore": 0}
        save_scores(self.scores)
        self._update_score_label()
        messagebox.showinfo("Reset", "Scores have been reset.")

# ---------------------- Run App ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGame(root)
    root.mainloop()
