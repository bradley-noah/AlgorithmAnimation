import tkinter as tk
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared import BaseAnimator, BG, COL_DIM, COL_ACTIVE, PAD, NODE_R
from hungarian.hungarian import hungarian, make_random_cost_matrix


DEFAULT_COST_MATRIX = [
    [9, 2, 7, 8],
    [6, 4, 3, 7],
    [5, 8, 1, 8],
    [7, 6, 9, 4],
]


class HungarianAnimator(BaseAnimator):

    STEP_DELAY = 800

    def __init__(self, root):
        super().__init__(root, title="Hungarian Algorithm  //  Todo")
        self.matrix     = []
        self.original   = []
        self.assignment = []
        self.load_scenario(DEFAULT_COST_MATRIX)

    def build_ui(self):
        pass

    def new_scenario(self):
        pass

    def load_scenario(self, cost_matrix, maximize=False):
        pass

    def reset(self, stop=True):
        self.matrix     = []
        self.assignment = []
        super().reset(stop)

    def draw_frame(self):
        self.canvas.delete("all")

    def _advance(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    HungarianAnimator(root)
    root.mainloop()