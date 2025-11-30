"""
Hangman Gamer — Final Edition (Cyber Theme V)
Created by: gamerdsh

Features:
- Fullscreen window (ESC returns to menu)
- Splash screen (Controller icon + Game Logo)
- Cyber/Matrix green-on-black theme
- Categories: Animals, Fruits, Random
- Difficulty: Easy / Medium / Hard (tries change)
- Keyboard + Mouse controls
- Simple SFX using winsound (Windows)
- Achievements (popup + confetti visual)
- Persistent score saved to hangman_scores.json
- Auto-start new game (same category/difficulty) after win/lose
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random, json, os, time
import threading
import winsound  # Windows built-in simple sound

# ---------------------- Config / Data ----------------------
SCOREFILE = "hangman_scores.json"
ICON_PNG = "controller_icon.png"   # used in splash if present
ICON_ICO = "controller_icon.ico"   # used for exe icon / window icon

CATEGORIES = {
    "Animals": {
        "lion": "King of the jungle",
        "tiger": "Striped big cat",
        "wolf": "Wild canine",
        "zebra": "Black & white stripes",
        "panda": "Black and white bear"
    },
    "Fruits": {
        "apple": "Keeps the doctor away",
        "banana": "Long yellow fruit",
        "mango": "Sweet tropical fruit",
        "orange": "Citrus fruit with vitamin C",
        "grape": "Small juicy fruit"
    },
    "Random": {}  # filled later as union
}
CATEGORIES["Random"] = {**CATEGORIES["Animals"], **CATEGORIES["Fruits"]}

DIFFICULTY_TRIES = {"Easy": 10, "Medium": 7, "Hard": 5}
MAX_HANGMAN_STEPS = 6  # visual steps (keeps same, but tries controlled by difficulty)

# ---------------------- Utilities ----------------------
def load_scores():
    if not os.path.exists(SCOREFILE):
        return {"games":0,"wins":0,"losses":0,"points":0}
    try:
        with open(SCOREFILE,"r") as f:
            return json.load(f)
    except Exception:
        return {"games":0,"wins":0,"losses":0,"points":0}

def save_scores(scores):
    try:
        with open(SCOREFILE,"w") as f:
            json.dump(scores,f)
    except Exception:
        pass

# SFX helpers (simple beeps)
def sfx_click():
    try:
        winsound.Beep(800, 70)
    except Exception:
        pass

def sfx_correct():
    try:
        winsound.Beep(1200, 100)
    except Exception:
        pass

def sfx_wrong():
    try:
        winsound.Beep(400, 120)
    except Exception:
        pass

def sfx_win():
    try:
        winsound.Beep(1000, 140)
        winsound.Beep(1400, 140)
    except Exception:
        pass

def sfx_lose():
    try:
        winsound.Beep(300, 250)
    except Exception:
        pass

# ---------------------- Main App ----------------------
class HangmanGamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Gamer — by gamerdsh")
        # try set icon (no crash if missing)
        try:
            self.root.iconbitmap(ICON_ICO)
        except Exception:
            pass

        # fullscreen and ESC binding
        self.fullscreen = True
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.show_menu())

        # theme colors (Cyber Matrix)
        self.colors = {
            "bg":"#050605",
            "fg":"#a6ff4d",
            "accent":"#00ff9b",
            "panel":"#071013",
            "bad":"#ff5c5c"
        }

        # load persistent scores
        self.scores = load_scores()

        # state
        self.category = "Animals"
        self.difficulty = "Medium"
        self.secret = ""
        self.hint = ""
        self.revealed = []
        self.guessed = set()
        self.missed = []
        self.tries = DIFFICULTY_TRIES[self.difficulty]
        self.round_start = time.time()
        self.achievements_unlocked = set()

        # build initial splash -> menu
        self.build_splash()

    # ---------- Splash Screen (Style B: Controller icon + Logo) ----------
    def build_splash(self):
        self.clear_all()
        frame = tk.Frame(self.root, bg=self.colors["bg"])
        frame.pack(expand=True, fill="both")
        # If PNG icon exists, show it
        logo_shown = False
        try:
            if os.path.exists(ICON_PNG):
                self.logo_img = tk.PhotoImage(file=ICON_PNG)
                lbl_icon = tk.Label(frame, image=self.logo_img, bg=self.colors["bg"])
                lbl_icon.pack(pady=(80,10))
                logo_shown = True
        except Exception:
            logo_shown = False

        title = tk.Label(frame, text="HANGMAN GAMER", font=("Consolas", 48, "bold"),
                         fg=self.colors["fg"], bg=self.colors["bg"])
        title.pack(pady=(20,10))
        subtitle = tk.Label(frame, text="by gamerdsh", font=("Arial", 16), fg=self.colors["accent"], bg=self.colors["bg"])
        subtitle.pack()

        # loading bar
        pb = ttk.Progressbar(frame, orient="horizontal", mode="determinate", length=600)
        pb.pack(pady=30)
        self.root.update()

        # animate loading (non-blocking)
        def run_loading():
            for i in range(101):
                pb['value'] = i
                time.sleep(0.01 + (0.0005 * i))
                self.root.update_idletasks()
            # short pause then show menu
            time.sleep(0.2)
            self.show_menu()
        threading.Thread(target=run_loading, daemon=True).start()

    # ---------- Main menu ----------
    def show_menu(self):
        sfx_click()
        self.clear_all()
        self.root.attributes("-fullscreen", True)
        frame = tk.Frame(self.root, bg=self.colors["bg"])
        frame.pack(expand=True, fill="both")

        title = tk.Label(frame, text="HANGMAN GAMER", font=("Consolas", 56, "bold"),
                         fg=self.colors["fg"], bg=self.colors["bg"])
        title.pack(pady=(60,10))

        # Category selector
        cat_frame = tk.Frame(frame, bg=self.colors["bg"])
        cat_frame.pack(pady=8)
        tk.Label(cat_frame, text="Category:", fg=self.colors["accent"], bg=self.colors["bg"], font=("Arial", 14)).grid(row=0,column=0,padx=6)
        self.cat_var = tk.StringVar(value=self.category)
        cat_menu = ttk.Combobox(cat_frame, textvariable=self.cat_var, values=list(CATEGORIES.keys()), state="readonly", width=20)
        cat_menu.grid(row=0,column=1, padx=6)

        # Difficulty selector
        diff_frame = tk.Frame(frame, bg=self.colors["bg"])
        diff_frame.pack(pady=8)
        tk.Label(diff_frame, text="Difficulty:", fg=self.colors["accent"], bg=self.colors["bg"], font=("Arial", 14)).grid(row=0,column=0,padx=6)
        self.diff_var = tk.StringVar(value=self.difficulty)
        diff_menu = ttk.Combobox(diff_frame, textvariable=self.diff_var, values=list(DIFFICULTY_TRIES.keys()), state="readonly", width=20)
        diff_menu.grid(row=0,column=1, padx=6)

        # Buttons
        btn_frame = tk.Frame(frame, bg=self.colors["bg"])
        btn_frame.pack(pady=20)
        start_btn = tk.Button(btn_frame, text="▶ START (Auto new round after finish)", font=("Arial",18,"bold"),
                              bg=self.colors["accent"], fg="#001000", width=28, command=self.start_game)
        start_btn.grid(row=0, column=0, pady=6, padx=6)

        view_btn = tk.Button(btn_frame, text="📊 Scoreboard", font=("Arial",14), bg=self.colors["panel"], fg=self.colors["fg"],
                             width=20, command=self.show_scoreboard)
        view_btn.grid(row=1, column=0, pady=6)

        about_btn = tk.Button(btn_frame, text="ℹ️ About / Credits", font=("Arial",14), bg=self.colors["panel"], fg=self.colors["fg"],
                              width=20, command=self.show_about)
        about_btn.grid(row=2, column=0, pady=6)

        exit_btn = tk.Button(btn_frame, text="Exit", font=("Arial",14), bg=self.colors["bad"], fg="white", width=20, command=self.root.destroy)
        exit_btn.grid(row=3, column=0, pady=12)

        # small footer
        footer = tk.Label(frame, text="Press ESC anytime to return to menu", fg="#888", bg=self.colors["bg"], font=("Arial", 10))
        footer.pack(side="bottom", pady=8)

    # ---------- Start game ----------
    def start_game(self):
        sfx_click()
        self.category = self.cat_var.get()
        self.difficulty = self.diff_var.get()
        self.tries = DIFFICULTY_TRIES.get(self.difficulty, 7)
        # choose word according to difficulty length rules (combo behavior)
        pool = [w for w in CATEGORIES[self.category].keys()]
        if self.difficulty == "Easy":
            pool = [w for w in pool if 3 <= len(w) <= 6]
        elif self.difficulty == "Medium":
            pool = [w for w in pool if 5 <= len(w) <= 8]
        else:
            pool = [w for w in pool if len(w) >= 6]
        if not pool:
            pool = list(CATEGORIES[self.category].keys())

        self.secret = random.choice(pool).lower()
        self.hint = CATEGORIES[self.category].get(self.secret,"No hint.")
        self.revealed = [False]*len(self.secret)
        self.guessed = set()
        self.missed = []
        self.round_start = time.time()
        self.build_game_ui()

    # ---------- Game UI ----------
    def build_game_ui(self):
        self.clear_all()
        frame = tk.Frame(self.root, bg=self.colors["bg"])
        frame.pack(expand=True, fill="both")

        top = tk.Frame(frame, bg=self.colors["bg"])
        top.pack(pady=6)
        title = tk.Label(top, text=f"Hangman Gamer — {self.category} ({self.difficulty})",
                         font=("Consolas", 24, "bold"), fg=self.colors["fg"], bg=self.colors["bg"])
        title.pack()

        # hangman canvas + word
        mid = tk.Frame(frame, bg=self.colors["bg"])
        mid.pack(pady=8, fill="both", expand=True)

        self.canvas = tk.Canvas(mid, width=540, height=420, bg=self.colors["panel"], highlightthickness=0)
        self.canvas.pack(side="left", padx=20, pady=10)
        self._draw_gallows()

        right = tk.Frame(mid, bg=self.colors["bg"])
        right.pack(side="right", padx=10, pady=10)

        self.word_label = tk.Label(right, text=self._display_word(), font=("Consolas",36), fg=self.colors["fg"], bg=self.colors["bg"])
        self.word_label.pack(pady=10)

        self.hint_label = tk.Label(right, text="Hint: ???", font=("Arial",14,"italic"), fg=self.colors["accent"], bg=self.colors["bg"])
        self.hint_label.pack(pady=6)

        self.missed_label = tk.Label(right, text="Missed: ", font=("Arial",14), fg=self.colors["bad"], bg=self.colors["bg"])
        self.missed_label.pack(pady=6)

        self.info_label = tk.Label(right, text=f"Tries left: {self.tries}", font=("Arial",14), fg=self.colors["fg"], bg=self.colors["bg"])
        self.info_label.pack(pady=6)

        self.score_label = tk.Label(right, text=f"Points: {self.scores.get('points',0)}", font=("Arial",14,"bold"), fg=self.colors["fg"], bg=self.colors["bg"])
        self.score_label.pack(pady=6)

        # keyboard letter buttons grid
        letters = tk.Frame(frame, bg=self.colors["bg"])
        letters.pack(side="bottom", pady=8)
        self.letter_buttons = {}
        for i,ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            b = tk.Button(letters, text=ch, width=4, height=2, bg=self.colors["panel"], fg=self.colors["fg"],
                          command=lambda c=ch: self.on_guess(c.lower()))
            b.grid(row=i//9, column=i%9, padx=3, pady=3)
            self.letter_buttons[ch] = b

        self.root.bind("<Key>", self._on_key)

    # ---------- Helpers ----------
    def clear_all(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _display_word(self):
        return " ".join([self.secret[i].upper() if self.revealed[i] else "_" for i in range(len(self.secret))])

    # ---------- Guesses ----------
    def on_guess(self, ch):
        # disable UI button and register guess
        btn = self.letter_buttons.get(ch.upper())
        if btn:
            btn.config(state="disabled")
        if ch in self.guessed:
            return
        self.guessed.add(ch)
        if ch in self.secret:
            sfx_correct()
            for i,c in enumerate(self.secret):
                if c==ch:
                    self.revealed[i]=True
        else:
            sfx_wrong()
            self.tries -= 1
            self.missed.append(ch)
        self.update_game_ui()
        self.check_end_conditions()

    def _on_key(self, event):
        ch = event.char.lower()
        if ch.isalpha() and len(ch)==1:
            self.on_guess(ch)

    def update_game_ui(self):
        # update labels, canvas
        self.word_label.config(text=self._display_word())
        self.missed_label.config(text="Missed: " + " ".join([m.upper() for m in self.missed]))
        self.info_label.config(text=f"Tries left: {self.tries}")
        self.score_label.config(text=f"Points: {self.scores.get('points',0)}")
        self._draw_hangman(min(len(self.missed), MAX_HANGMAN_STEPS))

    def show_hint(self):
        # hint rules: for Hard, only show when tries <=2 else locked
        if self.difficulty=="Hard" and self.tries>2:
            messagebox.showinfo("Hint Locked", "Hint unlocks when only 2 tries remain in Hard mode.")
            return
        self.hint_label.config(text="Hint: " + self.hint)

    # ---------- End Conditions ----------
    def check_end_conditions(self):
        if all(self.revealed):
            # win
            sfx_win()
            self._unlock_achievement("win")
            points = {"Easy":8,"Medium":12,"Hard":20}.get(self.difficulty,10)
            self.scores["points"] = self.scores.get("points",0) + points
            self.scores["wins"] = self.scores.get("wins",0) + 1
            self.scores["games"] = self.scores.get("games",0) + 1
            save_scores(self.scores)
            messagebox.showinfo("You Win!", f"You guessed: {self.secret.upper()}\n+{points} points")
            # auto-start a new game with same settings
            self.start_game()
        elif self.tries <= 0:
            sfx_lose()
            self._unlock_achievement("lose")
            self.scores["losses"] = self.scores.get("losses",0) + 1
            self.scores["games"] = self.scores.get("games",0) + 1
            save_scores(self.scores)
            messagebox.showerror("Game Over", f"You ran out of tries. Word was: {self.secret.upper()}")
            # auto-start new round
            self.start_game()

    # ---------- Draw hangman ----------
    def _draw_gallows(self):
        self.canvas.delete("all")
        # basic gallows
        self.canvas.create_line(50,380,350,380,fill=self.colors["fg"],width=4)   # base
        self.canvas.create_line(90,380,90,50,fill=self.colors["fg"],width=4)
        self.canvas.create_line(90,50,220,50,fill=self.colors["fg"],width=4)
        self.canvas.create_line(220,50,220,90,fill=self.colors["fg"],width=4)

    def _draw_hangman(self, step):
        # step from 0..6
        # remove old
        self.canvas.delete("part")
        if step>=1:
            # head
            self.canvas.create_oval(190,90,250,150,outline=self.colors["fg"],width=3,tag="part")
        if step>=2:
            # body
            self.canvas.create_line(220,150,220,230,fill=self.colors["fg"],width=3,tag="part")
        if step>=3:
            # left arm
            self.canvas.create_line(220,170,180,200,fill=self.colors["fg"],width=3,tag="part")
        if step>=4:
            # right arm
            self.canvas.create_line(220,170,260,200,fill=self.colors["fg"],width=3,tag="part")
        if step>=5:
            # left leg
            self.canvas.create_line(220,230,190,280,fill=self.colors["fg"],width=3,tag="part")
        if step>=6:
            # right leg
            self.canvas.create_line(220,230,250,280,fill=self.colors["fg"],width=3,tag="part")

    # ---------- Achievements ----------
    def _unlock_achievement(self, key):
        if key in self.achievements_unlocked:
            return
        self.achievements_unlocked.add(key)
        # popup with confetti
        self._achievement_popup("Achievement Unlocked", key.upper())

    def _achievement_popup(self, title, text):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("420x220")
        win.configure(bg=self.colors["bg"])
        tk.Label(win, text=title, font=("Arial",16,"bold"), fg=self.colors["accent"], bg=self.colors["bg"]).pack(pady=8)
        tk.Label(win, text=text, font=("Arial",14), fg=self.colors["fg"], bg=self.colors["bg"]).pack(pady=6)
        c = tk.Canvas(win, width=400, height=100, bg=self.colors["bg"], highlightthickness=0)
        c.pack()
        # simple confetti
        dots=[]
        for i in range(30):
            x=random.randint(0,400); y=random.randint(0,100)
            color=random.choice([self.colors["accent"], self.colors["fg"], "#7afcff", "#ff9bff"])
            dots.append(c.create_oval(x,y,x+6,y+6,fill=color,outline=""))
        def anim():
            for d in dots:
                c.move(d, 0, 5)
            win.after(80, anim)
        anim()
        self.root.after(2200, win.destroy)

    # ---------- Scoreboard / About ----------
    def show_scoreboard(self):
        sfx_click()
        sc = self.scores
        games = sc.get("games",0); wins=sc.get("wins",0); losses=sc.get("losses",0); points=sc.get("points",0)
        acc = (wins/games*100) if games else 0.0
        message = f"Games: {games}\nWins: {wins}\nLosses: {losses}\nPoints: {points}\nAccuracy: {acc:.1f}%"
        messagebox.showinfo("Scoreboard", message)

    def show_about(self):
        messagebox.showinfo("About", "Hangman Gamer\nCreated by: gamerdsh\nTheme: Cyber Matrix\nNo background music (SFX only)")

# ---------------------- Run ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGamer(root)
    root.mainloop()
