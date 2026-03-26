import tkinter as tk
from tkinter import font as tkfont

BG        = "#0f1117"
COL_TEXT  = "#eceff1"
COL_DIM   = "#455a64"
COL_PANEL = "#1a1d26"
COL_ACTIVE = "#ffe082"
BTN_BG    = "#4a5568"
BTN_HOVER = "#718096"
BTN_FG    = "#ffffff"
PAD       = 60
NODE_R    = 26


class BaseAnimator:

    STEP_DELAY = 700

    def __init__(self, root, title=""):
        self.root     = root
        self.running  = False
        self.after_id = None
        self.step_idx = 0
        self.events   = []
        self.done     = False

        root.title(title)
        root.configure(bg=BG)
        root.resizable(True, True)

        self.f_title  = tkfont.Font(family="Courier New", size=15, weight="bold")
        self.f_label  = tkfont.Font(family="Courier New", size=9)
        self.f_status = tkfont.Font(family="Courier New", size=10, weight="bold")

        self._build_chrome(title)

    def _build_chrome(self, title):
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill=tk.X, padx=16, pady=(12, 0))
        tk.Label(top, text=title, font=self.f_title,
                 bg=BG, fg=COL_TEXT).pack(side=tk.LEFT)

        btns = tk.Frame(top, bg=BG)
        btns.pack(side=tk.RIGHT)
        self._make_btn(btns, "New Scenario", self.new_scenario)
        self._make_btn(btns, "Reset",        self.reset)
        self._make_btn(btns, "Step",         self.step_once)
        self.run_btn = self._make_btn(btns, "Run", self.toggle_run)

        mid = tk.Frame(self.root, bg=BG)
        mid.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        self.canvas = tk.Canvas(mid, bg=BG, bd=0, highlightthickness=0,
                                width=640, height=480)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda _e: self.draw_frame())

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.status_var, font=self.f_status,
                 bg=COL_PANEL, fg=COL_ACTIVE, anchor="w",
                 padx=10, pady=6).pack(fill=tk.X, padx=16, pady=(0, 10))

    def _make_btn(self, parent, text, cmd):
        b = tk.Label(parent, text=text, font=self.f_label,
                     bg=BTN_BG, fg=BTN_FG, padx=10, pady=5,
                     cursor="hand2", relief=tk.FLAT)
        b.pack(side=tk.LEFT, padx=3)
        b.bind("<Button-1>", lambda _e: cmd())
        b.bind("<Enter>",    lambda _e: b.config(bg=BTN_HOVER))
        b.bind("<Leave>",    lambda _e: b.config(bg=BTN_BG))
        return b

    def toggle_run(self):
        if self.running:
            self._stop()
        else:
            self.running = True
            self.run_btn.config(text="Pause")
            self._schedule_step(self.STEP_DELAY)

    def step_once(self):
        if not self.done:
            self._advance()

    def _schedule_step(self, delay):
        if self.running and not self.done:
            self.after_id = self.root.after(delay, self._auto_step)

    def _auto_step(self):
        if self.running and not self.done:
            self._advance()

    def _stop(self):
        self.running = False
        self.run_btn.config(text="Run")
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def mark_done(self):
        self.done = True
        self._stop()
        self.status_var.set("Complete!")
        self.draw_frame()

    def reset(self, stop=True):
        if stop:
            self._stop()
        self.step_idx = 0
        self.done     = False
        self.status_var.set("Ready")
        self.draw_frame()

    def build_ui(self):       pass
    def new_scenario(self):   raise NotImplementedError
    def load_scenario(self):  raise NotImplementedError
    def draw_frame(self):     raise NotImplementedError
    def _advance(self):       raise NotImplementedError