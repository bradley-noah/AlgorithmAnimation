import tkinter as tk
import tkinter.font as tkfont
import math
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared import BaseAnimator, BG, COL_DIM, PAD, NODE_R
from gale_shapley.gale_shapley import gale_shapley, make_random_scenario


COL_PROPOSER = "#4fc3f7"
COL_RECEIVER = "#f48fb1"
COL_ENGAGED  = "#69f0ae"
COL_PROPOSE  = "#ffe082"
RING_OUTLINE = "#ffd700"
RING_FILL    = "#b8860b"
RING_MS    = 33
RING_STEPS = 22


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

    STEP_DELAY = 300

    def __init__(self, root):
        super().__init__(root, title="Gale-Shapley  \u00b7  Stable Marriage")

        self.f_node  = tkfont.Font(family="Courier New", size=11, weight="bold")
        self.f_small = tkfont.Font(family="Courier New", size=8)

        self.proposers      = []
        self.receivers      = []
        self.proposer_prefs = {}
        self.receiver_prefs = {}

        self.engagements    = {} 
        self.past_rejected  = {}   
        self.proposal_line  = None 

        self.ring       = None
        self.ring_after = None

        self.load_scenario(DEFAULT_PROPOSER_PREFS, DEFAULT_RECEIVER_PREFS)

    def build_ui(self):
        pass

    def new_scenario(self):
        n = len(self.proposers) if self.proposers else 4
        mp, wp = make_random_scenario(n)
        self.load_scenario(mp, wp)

    def load_scenario(self, proposer_prefs, receiver_prefs):
        self.proposer_prefs = proposer_prefs
        self.receiver_prefs = receiver_prefs
        self.proposers      = list(proposer_prefs.keys())
        self.receivers      = list(receiver_prefs.keys())
        self.events, _      = gale_shapley(proposer_prefs, receiver_prefs)
        self.reset(stop=True)

    def reset(self, stop=True):
        self._cancel_ring()
        self.engagements   = {}
        self.past_rejected = {}
        self.proposal_line = None
        super().reset(stop)

    # ── Ring ──────────────────────────────────────────────────────────────────

    def _cancel_ring(self):
        if self.ring_after:
            self.root.after_cancel(self.ring_after)
            self.ring_after = None
        self.ring = None

    def _launch_ring(self, fx, fy, tx, ty, on_done):
        self._cancel_ring()
        self.ring = {"fx": fx, "fy": fy, "tx": tx, "ty": ty,
                     "frame": 0, "on_done": on_done}
        self._ring_tick()

    def _ring_tick(self):
        r = self.ring
        if r is None:
            return
        r["frame"] += 1
        self.draw_frame()
        if r["frame"] >= RING_STEPS:
            self.ring = None
            r["on_done"]()
        else:
            self.ring_after = self.root.after(RING_MS, self._ring_tick)

    def _ring_xy(self):
        r = self.ring
        if r is None:
            return None
        t = r["frame"] / RING_STEPS
        t = t * t * (3.0 - 2.0 * t)
        return (r["fx"] + (r["tx"] - r["fx"]) * t, r["fy"] + (r["ty"] - r["fy"]) * t)

    # ── Node positions ────────────────────────────────────────────────────────

    def _positions(self):
        W = self.canvas.winfo_width()  or 640
        H = self.canvas.winfo_height() or 480
        n       = len(self.proposers)
        left_x  = PAD + NODE_R
        right_x = W - PAD - NODE_R
        def yp(i):
            return PAD + (H - 2 * PAD) * i / max(n - 1, 1)
        mp = {m: (left_x,  yp(i)) for i, m in enumerate(self.proposers)}
        wp = {w: (right_x, yp(i)) for i, w in enumerate(self.receivers)}
        return mp, wp

    # ── Algorithm ─────────────────────────────────────────────────────────────

    def _advance(self):
        if self.ring is not None:
            return

        if self.step_idx >= len(self.events):
            self.mark_done()
            return
        

        ev   = self.events[self.step_idx]
        self.step_idx += 1
        kind = ev["type"]
        mp, wp = self._positions()

        if kind == "propose":
            p, r = ev["proposer"], ev["receiver"]
            self.proposal_line = (p, r)
            self.status_var.set("  {} proposes to {}".format(p, r))
            self.draw_frame()
            self._launch_ring(*mp[p], *wp[r], self._after_propose)

        elif kind == "accept":
            p, r, replaced = ev["proposer"], ev["receiver"], ev["replaced"]
            self.engagements[r] = p
            if replaced:
                self.status_var.set("  {} accepts {}, frees {}".format(r, p, replaced))
                self.past_rejected.setdefault(replaced, set()).add(r)
                self._launch_ring(*wp[r], *mp[replaced], self._after_resolution)
            else:
                self.status_var.set("  {} accepts {}".format(r, p))
                self.proposal_line = None
                self.draw_frame()
                self._after_resolution()

        elif kind == "reject":
            if ev.get("reason") == "replaced":
                self.draw_frame()
                if self.running:
                    self._schedule_step(self.STEP_DELAY)
                return
            p, r = ev["proposer"], ev["receiver"]
            self.status_var.set("  {} rejects {}".format(r, p))
            self.past_rejected.setdefault(p, set()).add(r)
            self._launch_ring(*wp[r], *mp[p], self._after_resolution)

        elif kind == "done":
            self.mark_done()

    def _after_propose(self):
        self.proposal_line = None
        self._advance()

    def _after_resolution(self):
        self.draw_frame()
        if not self.done and self.running:
            self._schedule_step(self.STEP_DELAY)

    # ── Drawing ───────────────────────────────────────────────────────────────

    def draw_frame(self):
        c = self.canvas
        c.delete("all")
        W = c.winfo_width()  or 640
        H = c.winfo_height() or 480
        mp, wp = self._positions()

        for proposer, rej_set in self.past_rejected.items():
            for receiver in rej_set:
                x1, y1 = mp[proposer]
                x2, y2 = wp[receiver]
                c.create_line(x1, y1, x2, y2, fill=COL_DIM, width=1, dash=(3, 5))

        for receiver, proposer in self.engagements.items():
            x1, y1 = mp[proposer]
            x2, y2 = wp[receiver]
            c.create_line(x1, y1, x2, y2, fill=COL_ENGAGED, width=3 if self.done else 2)

        if self.proposal_line and not self.done:
            p, r = self.proposal_line
            x1, y1 = mp[p]
            x2, y2 = wp[r]
            c.create_line(x1, y1, x2, y2, fill=COL_PROPOSE, width=2, dash=(6, 3))
            self._draw_arrowhead(c, x1, y1, x2, y2)

        for m, (x, y) in mp.items():
            engaged = any(v == m for v in self.engagements.values())
            c.create_oval(x-NODE_R, y-NODE_R, x+NODE_R, y+NODE_R,
                          fill=BG, outline=COL_ENGAGED if engaged else COL_PROPOSER,
                          width=3 if engaged else 1)
            c.create_text(x, y, text=m, fill=COL_PROPOSER, font=self.f_node)

        for w, (x, y) in wp.items():
            engaged = w in self.engagements
            c.create_oval(x-NODE_R, y-NODE_R, x+NODE_R, y+NODE_R,
                          fill=BG, outline=COL_ENGAGED if engaged else COL_RECEIVER,
                          width=3 if engaged else 1)
            c.create_text(x, y, text=w, fill=COL_RECEIVER, font=self.f_node)

        rpos = self._ring_xy()
        if rpos:
            rx, ry = rpos
            outer, hole = 13, 10
            c.create_oval(rx-outer, ry-outer, rx+outer, ry+outer,
                          outline=RING_OUTLINE, fill=RING_FILL, width=2)
            c.create_oval(rx-hole, ry-hole, rx+hole, ry+hole,
                          outline="", fill=BG)

        c.create_text(PAD + NODE_R,     PAD // 2 - 10,
                      text="PROPOSERS", fill=COL_PROPOSER, font=self.f_label)
        c.create_text(W - PAD - NODE_R, PAD // 2 - 10,
                      text="RECEIVERS", fill=COL_RECEIVER, font=self.f_label)

        self._draw_legend(c, W, H)

    def _draw_arrowhead(self, c, x1, y1, x2, y2, size=10):
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy) or 1
        ux, uy = dx / length, dy / length
        tip_x  = x2 - ux * NODE_R
        tip_y  = y2 - uy * NODE_R
        lx = tip_x - ux*size + uy*size*0.5
        ly = tip_y - uy*size - ux*size*0.5
        rx = tip_x - ux*size - uy*size*0.5
        ry = tip_y - uy*size + ux*size*0.5
        c.create_polygon(tip_x, tip_y, lx, ly, rx, ry, fill=COL_PROPOSE, outline="")

    def _draw_legend(self, c, W, H):
        items = [
            (COL_PROPOSE, "active proposal"),
            (COL_ENGAGED, "engaged / final"),
            (COL_DIM,     "past rejection"),
        ]
        item_w  = 160
        total_w = item_w * len(items) - 26
        x = (W - total_w) // 2 + 25
        y = H - 10
        for color, label in items:
            c.create_line(x, y, x + 18, y, fill=color, width=2)
            c.create_text(x + 24, y, text=label, fill=COL_DIM, font=self.f_small, anchor="w")
            x += item_w


if __name__ == "__main__":
    root = tk.Tk()
    GaleShapleyAnimator(root)
    root.mainloop()