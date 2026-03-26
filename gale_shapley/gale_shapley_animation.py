import tkinter as tk
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared import BaseAnimator, BG, COL_DIM, COL_ACTIVE, PAD, NODE_R
from gale_shapley.gale_shapley import gale_shapley, make_random_scenario


DEFAULT_PROPOSER_PREFS = {
    "M1": ["W3", "W1", "W4", "W2"],
    "M2": ["W2", "W4", "W1", "W3"],
    "M3": ["W1", "W3", "W2", "W4"],
    "M4": ["W4", "W2", "W3", "W1"],
}
DEFAULT_RECEIVER_PREFS = {
    "W1": ["M3", "M1", "M2", "M4"],
    "W2": ["M2", "M4", "M1", "M3"],
    "W3": ["M1", "M3", "M4", "M2"],
    "W4": ["M4", "M2", "M3", "M1"],
}


class GaleShapleyAnimator(BaseAnimator):

    STEP_DELAY = 700

    def __init__(self, root):
        super().__init__(root, title="Gale-Shapley  //  Todo")
        self.proposers      = []
        self.receivers      = []
        self.proposer_prefs = {}
        self.receiver_prefs = {}
        self.engagements    = {}
        self.load_scenario(DEFAULT_PROPOSER_PREFS, DEFAULT_RECEIVER_PREFS)

    def build_ui(self):
        pass

    def new_scenario(self):
        pass

    def load_scenario(self, proposer_prefs, receiver_prefs):
        pass

    def reset(self, stop=True):
        self.engagements = {}
        super().reset(stop)

    def draw_frame(self):
        self.canvas.delete("all")

    def _advance(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    GaleShapleyAnimator(root)
    root.mainloop()