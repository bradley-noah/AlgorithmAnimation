import tkinter as tk
import sys


def launch_all():
    root = tk.Tk()
    root.withdraw()

    from hungarian.hungarian_animation   import HungarianAnimator
    from gale_shapley.gale_shapley_animation import GaleShapleyAnimator
    from dinic.dinic_animation           import DinicAnimator

    for Cls in (HungarianAnimator, GaleShapleyAnimator, DinicAnimator):
        win = tk.Toplevel(root)
        Cls(win)

    root.mainloop()


def launch_one(name):
    root = tk.Tk()
    name = name.lower()

    if name == "hungarian":
        from hungarian.hungarian_animation import HungarianAnimator
        HungarianAnimator(root)
    elif name == "gale_shapley":
        from gale_shapley.gale_shapley_animation import GaleShapleyAnimator
        GaleShapleyAnimator(root)
    elif name == "dinic":
        from dinic.dinic_animation import DinicAnimator
        DinicAnimator(root)
    else:
        print("Unknown: choose hungarian | gale_shapley | dinic")
        sys.exit(1)

    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        launch_one(sys.argv[1])
    else:
        launch_all()
