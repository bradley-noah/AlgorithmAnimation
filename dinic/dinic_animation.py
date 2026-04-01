import tkinter as tk
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared import BaseAnimator, BG, COL_DIM, COL_ACTIVE, COL_TEXT, PAD, NODE_R
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
        n = DEFAULT_N
        edges = make_random_graph(n, n_edges=9, max_cap=10)
        self.load_scenario(n, edges, DEFAULT_SOURCE, DEFAULT_SINK, DEFAULT_LAYOUT)
        self.reset()

    def load_scenario(self, n, edge_list, source, sink, layout):
        self.n      = n
        self.source = source
        self.sink   = sink
        self.graph  = build_graph(n, edge_list)
        self.layout = layout
        self.cap_orig = {}
        for i, edge in enumerate(edge_list):
            self.cap_orig[(edge[0], edge[1])] = edge[2]
        self.events = []

    def reset(self, stop=True):
        self.level       = []
        self.total_flow  = 0
        self.active_path = []
        self.graph       = []
        self.events      = []
        if hasattr(self, 'n') and self.n > 0:
            self.graph = build_graph(self.n, [(k[0], k[1], v) for k, v in self.cap_orig.items()])
        super().reset(stop)

    def draw_frame(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 100 or h < 100:
            return

        PAD = 60
        cx = lambda x: PAD + x * (w - 2 * PAD)
        cy = lambda y: PAD + y * (h - 2 * PAD)

        edge_flow = {}
        for i in range(len(self.graph)):
            for edge in self.graph[i]:
                if (i, edge.to) in self.cap_orig and edge.to != i:
                    edge_flow[(i, edge.to)] = self.cap_orig[(i, edge.to)] - edge.cap

        for (frm, to), flow in edge_flow.items():
            if flow > 0:
                x1, y1 = self.layout[frm]
                x2, y2 = self.layout[to]
                x1, y1, x2, y2 = cx(x1), cy(y1), cx(x2), cy(y2)
                color = COL_ACTIVE if self.level and self.level[frm] >= 0 and self.level[to] == self.level[frm] + 1 else COL_DIM
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                self.canvas.create_text(mx, my, text=f"{flow}", fill=COL_ACTIVE, font=("Courier New", 9))

        for node in range(self.n):
            x, y = self.layout[node]
            x, y = cx(x), cy(y)
            color = COL_ACTIVE if node == self.source or node == self.sink else COL_DIM
            self.canvas.create_oval(x - NODE_R, y - NODE_R, x + NODE_R, y + NODE_R,
                                    fill=BG, outline=color, width=2)
            self.canvas.create_text(x, y, text=str(node), fill=COL_TEXT, font=("Courier New", 12, "bold"))

        self.status_var.set(f"Max Flow: {self.total_flow}")

    def _advance(self):
        if self.step_idx >= len(self.events):
            self.mark_done()
            return

        event = self.events[self.step_idx]
        if event[0] == 'level':
            self.level = event[1]
        elif event[0] == 'flow':
            self.total_flow += event[3]
        elif event[0] == 'done':
            self.mark_done()
            return

        self.step_idx += 1
        self.draw_frame()


if __name__ == "__main__":
    root = tk.Tk()
    DinicAnimator(root)
    root.mainloop()
