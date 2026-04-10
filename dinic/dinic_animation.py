import tkinter as tk
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared import BaseAnimator, BG, COL_DIM, COL_ACTIVE, PAD, NODE_R
from dinic.dinic import build_graph, dinic, make_random_graph

COL_EDGE = "#546e7a"
COL_LEVEL_EDGE = "#4fc3f7"
COL_ACTIVE = "#ffca28"
COL_NODE = "#263238"
COL_SOURCE = "#2ecc71"
COL_SINK = "#e74c3c"
COL_TEXT = "#e0f7fa"
COL_FLOW_BG = "#1a1d26"

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
        super().__init__(root, title="Dinic's Algorithm")
        self.n           = 0
        self.source      = 0
        self.sink        = 0
        self.total_flow  = 0
        self.step_idx = 0
        self.level       = None
        self.active_edge = None
        self.graph       = []
        self.events = []
        self.layout      = {}
        self.cap_orig    = {}
        self.load_scenario(DEFAULT_N, DEFAULT_EDGES, DEFAULT_SOURCE,
                           DEFAULT_SINK, DEFAULT_LAYOUT)

    def build_ui(self):
        super().build_ui()

    def new_scenario(self):
        edges = make_random_graph(DEFAULT_N, 9, 10)
        self.load_scenario(DEFAULT_N, edges, DEFAULT_SOURCE, DEFAULT_SINK, DEFAULT_LAYOUT)

    def load_scenario(self, n, edge_list, source, sink, layout):
        self.n = n
        self.source = source
        self.sink = sink
        self.layout = layout
        self.graph = build_graph(n, edge_list)
        self.cap_orig = {}

        for u in range(n):
            for e in self.graph[u]:
                self.cap_orig[(u, e.to)] = e.cap
        
        graph_copy = build_graph(n, edge_list)
        self.events, _ = dinic(graph_copy, source, sink)
        
        self.reset(stop = False)

    def reset(self, stop=True):
        super().reset(stop)

        self.level = None
        self.total_flow  = 0
        self.active_edge = None
        self.step_idx = 0

        self.status_var.set("Ready")
        self.draw_frame()

    def _pos(self, u, w, h):
        px, py = self.layout[u]
        return int(px * w), int(py * h)

    def draw_frame(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        for u in range(self.n):
            x1, y1 = self._pos(u, w, h)

            for e in self.graph[u]:
                v = e.to
                x2, y2 = self._pos(v, w, h)

                color = COL_EDGE
                width = 1

                if self.level and self.level[u] != -1:
                    if self.level[v] == self.level[u] + 1:
                        color = COL_LEVEL_EDGE
                        width = 2

                if self.active_edge == (u, v):
                    color = COL_ACTIVE
                    width = 4

                cap_orig = self.cap_orig.get((u, v), e.cap)
                flow_used = cap_orig - e.cap

                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=color,
                    width=width,
                    arrow=tk.LAST
                )
                
                mx, my = (x1 + x2) // 2, (y1 + y2) // 2

                self.canvas.create_rectangle(
                    mx - 18, my - 10,
                    mx + 18, my + 10,
                    fill=COL_FLOW_BG,
                    outline=""
                )

                self.canvas.create_text(
                    mx, my,
                    text=f"{flow_used}/{cap_orig}",
                    fill=COL_TEXT,
                    font=("Courier New", 9, "bold")
                )

        for u in range(self.n):
            x, y = self._pos(u, w, h)

            fill = COL_NODE
            if u == self.source:
                fill = COL_SOURCE
            elif u == self.sink:
                fill = COL_SINK

            self.canvas.create_oval(
                x - NODE_R, y - NODE_R,
                x + NODE_R, y + NODE_R,
                fill=fill,
                outline="#90a4ae",
                width=2
            )

            self.canvas.create_text(
                x, y - 6,
                text=str(u),
                fill="white",
                font=("Courier New", 11, "bold")
            )

            if self.level:
                self.canvas.create_text(
                    x, y + 10,
                    text=f"L{self.level[u]}",
                    fill="#90caf9",
                    font=("Courier New", 8)
            )

        self.canvas.create_rectangle(5, 5, 160, 35, fill=COL_FLOW_BG, outline="")
        self.canvas.create_text(
            12, 18,
            anchor="w",
            text=f"Flow: {self.total_flow}",
            fill="#81c784",
            font=("Courier New", 12, "bold")
        )

    def _advance(self):
        if self.step_idx >= len(self.events):
            self.mark_done()
            return

        event = self.events[self.step_idx]
        self.step_idx += 1

        etype = event[0]

        if etype == "level":
            self.level = event[1]
            self.active_edge = None
            self.status_var.set("BFS: Building level graph")

        elif etype == "flow":
            _, u, v, f = event

            for e in self.graph[u]:
                if e.to == v:
                    e.cap -= f
                    break

            for e in self.graph[v]:
                if e.to == u:
                    e.cap += f
                    break

            self.active_edge = (u, v)
            self.status_var.set(f"DFS: {u} -> {v} ({f})")

        elif etype == "path":
            _, total = event
            self.total_flow = total
            self.active_edge = None
            self.status_var.set(f"Augmented path -> {total}")
        
        elif etype == "done":
            self.total_flow = event[1]
            self.active_edge = None
            self.mark_done()
            return

        self.draw_frame()

        if self.running:
            self._schedule_step(self.STEP_DELAY)


if __name__ == "__main__":
    root = tk.Tk()
    DinicAnimator(root)
    root.mainloop()
