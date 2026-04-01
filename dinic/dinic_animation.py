import tkinter as tk
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared import BaseAnimator, BG, COL_DIM, COL_ACTIVE, PAD, NODE_R
from dinic.dinic import Edge, build_graph, dinic, make_random_graph


DEFAULT_N      = 6
DEFAULT_SOURCE = 0
DEFAULT_SINK   = 5
DEFAULT_EDGES  = [
    (0, 1, 10), (0, 2, 10),
    (1, 3, 4),  (1, 4, 8), (1, 2, 2),
    (2, 4, 9),
    (3, 5, 10), (4, 3, 6), (4, 5, 10),
]
DEFAULT_LAYOUT = {
    0: (0.08, 0.50),
    1: (0.33, 0.20),
    2: (0.33, 0.80),
    3: (0.60, 0.20),
    4: (0.60, 0.80),
    5: (0.92, 0.50),
}


class DinicAnimator(BaseAnimator):

    STEP_DELAY = 900

    def __init__(self, root):
        super().__init__(root, title="Dinic's Algorithm  //  Todo")
        self.n           = 0
        self.source      = 0
        self.sink        = 0
        self.graph       = []
        self.level       = []
        self.total_flow  = 0
        self.active_path = []
        self.layout      = {}
        self.cap_orig    = {}
        self.load_scenario(DEFAULT_N, DEFAULT_EDGES, DEFAULT_SOURCE,
                           DEFAULT_SINK, DEFAULT_LAYOUT)

    def build_ui(self):
        pass

    def new_scenario(self):
        pass

    def load_scenario(self, n, edge_list, source, sink, layout):
        pass

    def reset(self, stop=True):
        self.level       = []
        self.total_flow  = 0
        self.active_path = []
        self.graph       = []
        super().reset(stop)

    def draw_frame(self):
        self.canvas.delete("all")

    def _advance(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    DinicAnimator(root)
    root.mainloop()
