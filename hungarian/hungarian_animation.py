from __future__ import annotations

import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
import shutil
import tempfile
from typing import Sequence, cast

import numpy as np
from manim import BLUE, DOWN, GREEN, LEFT, Line, ORANGE, RED, UP, YELLOW, Create, FadeIn, FadeOut, Group, Integer, LaggedStart, Scene, Square, SurroundingRectangle, Text, Transform, VGroup, VMobject, Write

from hungarian.hungarian import hungarian

DEMO_COST_MATRIX: list[list[int]] = [
    [1, 3, 28, 7, 20, 13],
    [5, 21, 9, 12, 20, 12],
    [16, 4, 4, 28, 16, 15],
    [16, 16, 10, 3, 5, 4],
    [24, 11, 24, 9, 16, 27],
    [23, 6, 17, 1, 7, 17],
]


class MatrixBoard(VGroup):
    def __init__(
        self,
        matrix: Sequence[Sequence[int]],
        cell_size: float = 0.8,
        font_size: int = 28,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.matrix = [row[:] for row in matrix]
        self.n = len(matrix)
        self.cell_size = cell_size
        self.font_size = font_size

        self.boxes = VGroup()
        self.labels = VGroup()
        self.row_tags = VGroup()
        self.col_tags = VGroup()

        for i in range(self.n):
            for j in range(self.n):
                box = Square(side_length=cell_size, stroke_width=2)
                box.move_to(np.array([
                    (j - (self.n - 1) / 2) * cell_size,
                    ((self.n - 1) / 2 - i) * cell_size,
                    0,
                ]))
                label = Integer(matrix[i][j], font_size=font_size)
                label.move_to(box.get_center())
                self.boxes.add(box)
                self.labels.add(label)

        for i in range(self.n):
            tag = Text(f"R{i}", font_size=22)
            tag.next_to(self.boxes[i * self.n], LEFT, buff=0.25)
            self.row_tags.add(tag)

        for j in range(self.n):
            tag = Text(f"C{j}", font_size=22)
            tag.next_to(self.boxes[j], UP, buff=0.25)
            self.col_tags.add(tag)

        self.add(self.boxes, self.labels, self.row_tags, self.col_tags)

    def idx(self, i: int, j: int) -> int:
        return i * self.n + j

    def box_at(self, i: int, j: int) -> VMobject:
        return cast(VMobject, self.boxes[self.idx(i, j)])

    def label_at(self, i: int, j: int) -> VMobject:
        return cast(VMobject, self.labels[self.idx(i, j)])

    def animate_to_matrix(self, new_matrix: Sequence[Sequence[int]]) -> list[Transform]:
        anims: list[Transform] = []
        for i in range(self.n):
            for j in range(self.n):
                new_label = Integer(new_matrix[i][j], font_size=self.font_size)
                new_label.move_to(self.label_at(i, j).get_center())
                anims.append(Transform(self.label_at(i, j), new_label))
        self.matrix = [row[:] for row in new_matrix]
        return anims

    def matching_marks(self, matching: Sequence[tuple[int, int]], color=YELLOW) -> VGroup:
        marks = VGroup()
        for i, j in matching:
            marks.add(SurroundingRectangle(self.box_at(i, j), color=color, buff=0.03, stroke_width=4))
        return marks

    def cover_marks(self, row_covered: Sequence[bool], col_covered: Sequence[bool]) -> VGroup:
        marks = VGroup()
        x_left = self.box_at(0, 0).get_left()[0] - 0.04
        x_right = self.box_at(0, self.n - 1).get_right()[0] + 0.04
        y_top = self.box_at(0, 0).get_top()[1] + 0.04
        y_bottom = self.box_at(self.n - 1, 0).get_bottom()[1] - 0.04

        for i, covered in enumerate(row_covered):
            if covered:
                y = self.box_at(i, 0).get_center()[1]
                marks.add(
                    Line(
                        np.array([x_left, y, 0]),
                        np.array([x_right, y, 0]),
                        color=BLUE,
                        stroke_width=3,
                    )
                )

        for j, covered in enumerate(col_covered):
            if covered:
                x = self.box_at(0, j).get_center()[0]
                marks.add(
                    Line(
                        np.array([x, y_bottom, 0]),
                        np.array([x, y_top, 0]),
                        color=GREEN,
                        stroke_width=3,
                    )
                )
        return marks

    def uncovered_marks(self, row_covered: Sequence[bool], col_covered: Sequence[bool]) -> VGroup:
        marks = VGroup()
        for i in range(self.n):
            for j in range(self.n):
                if not row_covered[i] and not col_covered[j]:
                    marks.add(SurroundingRectangle(self.box_at(i, j), color=RED, buff=0.03, stroke_width=2))
        return marks


class HungarianAlgorithmDemo(Scene):
    PLAYBACK_SLOWDOWN = 2.4

    def _t(self, seconds: float) -> float:
        return seconds * self.PLAYBACK_SLOWDOWN

    def construct(self):
        cost_matrix = DEMO_COST_MATRIX

        events, _assignment, _total_cost = hungarian(cost_matrix)

        title = Text("Hungarian Algorithm", font_size=42)
        title.to_edge(UP)

        caption = Text("Initial cost matrix (6x6)", font_size=28)
        caption.next_to(title, DOWN, buff=0.3)

        board = MatrixBoard(events[0]["matrix"])
        board.next_to(caption, DOWN, buff=0.5)

        self.play(Write(title), FadeIn(caption), Create(board), run_time=self._t(1.6))
        self.wait(self._t(0.6))

        active_matching = VGroup()
        active_cover = VGroup()
        active_uncovered = VGroup()

        for k, event in enumerate(events[1:], start=1):
            event_type = event["type"]

            if event_type == "row_reduce":
                new_caption = Text("Subtract each row minimum", font_size=28)
                new_caption.move_to(caption)
                self.play(Transform(caption, new_caption), run_time=self._t(0.9))

                row_glow = VGroup(*[
                    SurroundingRectangle(Group(*[board.box_at(i, j) for j in range(board.n)]), color=BLUE, buff=0.05)
                    for i in range(board.n)
                ])
                self.play(LaggedStart(*[Create(g) for g in row_glow], lag_ratio=0.15), run_time=self._t(1.0))
                self.play(*board.animate_to_matrix(event["matrix"]), run_time=self._t(1.4))
                self.play(FadeOut(row_glow), run_time=self._t(0.7))
                self.wait(self._t(0.45))

            elif event_type == "col_reduce":
                new_caption = Text("Subtract each column minimum", font_size=28)
                new_caption.move_to(caption)
                self.play(Transform(caption, new_caption), run_time=self._t(0.9))

                col_glow = VGroup(*[
                    SurroundingRectangle(Group(*[board.box_at(i, j) for i in range(board.n)]), color=GREEN, buff=0.05)
                    for j in range(board.n)
                ])
                self.play(LaggedStart(*[Create(g) for g in col_glow], lag_ratio=0.15), run_time=self._t(1.0))
                self.play(*board.animate_to_matrix(event["matrix"]), run_time=self._t(1.4))
                self.play(FadeOut(col_glow), run_time=self._t(0.7))
                self.wait(self._t(0.45))

            elif event_type == "match":
                new_caption = Text(
                    f"Find a maximum matching among zero entries (size = {event['cover_count']})",
                    font_size=24,
                )
                new_caption.move_to(caption)
                new_matching = board.matching_marks(event["matching"])
                self.play(
                    Transform(caption, new_caption),
                    FadeOut(active_matching),
                    FadeIn(new_matching),
                    run_time=self._t(1.0),
                )
                active_matching = new_matching
                self.wait(self._t(0.55))

            elif event_type == "cover":
                new_caption = Text("Cover all zeros with the minimum number of lines", font_size=26)
                new_caption.move_to(caption)
                new_cover = board.cover_marks(event["row_covered"], event["col_covered"])
                self.play(
                    Transform(caption, new_caption),
                    FadeOut(active_cover),
                    FadeIn(new_cover),
                    run_time=self._t(1.0),
                )
                active_cover = new_cover
                self.wait(self._t(0.55))

            elif event_type == "adjust":
                new_caption = Text(
                    f"Adjust uncovered entries by the minimum uncovered value = {event['min_val']}",
                    font_size=24,
                )
                new_caption.move_to(caption)
                prev_event = events[k - 1]
                row_covered = prev_event["row_covered"]
                col_covered = prev_event["col_covered"]
                new_uncovered = board.uncovered_marks(row_covered, col_covered)
                self.play(Transform(caption, new_caption), FadeIn(new_uncovered), run_time=self._t(1.0))
                active_uncovered = new_uncovered
                self.play(*board.animate_to_matrix(event["matrix"]), run_time=self._t(1.4))
                self.play(FadeOut(active_uncovered), FadeOut(active_cover), run_time=self._t(0.8))
                active_uncovered = VGroup()
                active_cover = VGroup()
                self.wait(self._t(0.45))

            elif event_type == "done":
                final_marks = board.matching_marks(event["assignment"], color=ORANGE)
                result = Text(
                    f"Optimal assignment cost = {event['total_cost']}",
                    font_size=30,
                )
                result.next_to(board, DOWN, buff=0.5)
                new_caption = Text("Done: one assignment per row and column", font_size=28)
                new_caption.move_to(caption)
                self.play(
                    Transform(caption, new_caption),
                    FadeOut(active_matching),
                    FadeIn(final_marks),
                    Write(result),
                    run_time=self._t(1.3),
                )
                self.wait(self._t(2.2))


class HungarianAnimator:
    """
    Tk-compatible launcher used by main.py.
    It keeps the existing Manim scene and opens it via the current Python env.
    """

    def __init__(self, root: tk.Tk | tk.Toplevel):
        self.root = root
        self.root.title("Hungarian Algorithm (Manim)")
        self.root.configure(bg="#0f1117")
        self._worker: threading.Thread | None = None

        frame = tk.Frame(self.root, bg="#0f1117", padx=16, pady=14)
        frame.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(
            frame,
            text="Hungarian Algorithm",
            bg="#0f1117",
            fg="#eceff1",
            font=("Courier New", 14, "bold"),
        )
        title.pack(anchor="w")

        self.status = tk.StringVar(value="Launching Manim preview...")
        status_label = tk.Label(
            frame,
            textvariable=self.status,
            bg="#0f1117",
            fg="#ffe082",
            justify="left",
            font=("Courier New", 10),
            wraplength=540,
        )
        status_label.pack(anchor="w", pady=(8, 10))

        btn_row = tk.Frame(frame, bg="#0f1117")
        btn_row.pack(anchor="w")
        tk.Button(
            btn_row,
            text="Render Again",
            command=self.launch_preview,
            bg="#4a5568",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=10,
            pady=4,
        ).pack(side=tk.LEFT)

        self.launch_preview()

    def launch_preview(self) -> None:
        if self._worker and self._worker.is_alive():
            self.status.set("Render already running...")
            return

        self.status.set("Rendering video only (4K)...")
        self._worker = threading.Thread(target=self._render_preview, daemon=True)
        self._worker.start()

    def _set_status(self, text: str) -> None:
        self.root.after(0, lambda: self.status.set(text))

    def _resolve_python(self, project_root: Path) -> Path:
        venv_python = project_root / ".venv" / "Scripts" / "python.exe"
        if venv_python.exists():
            return venv_python
        return Path(sys.executable)

    def _render_preview(self) -> None:
        scene_file = Path(__file__).resolve()
        project_root = scene_file.parent.parent
        python_exe = self._resolve_python(project_root)
        output_name = "HungarianAlgorithmDemo_6x6.mp4"
        try:
            with tempfile.TemporaryDirectory(prefix="manim_hungarian_") as temp_media:
                cmd = [
                    str(python_exe),
                    "-m",
                    "manim",
                    "-qh",
                    "--disable_caching",
                    "--media_dir",
                    temp_media,
                    "--resolution",
                    "3840,2160",
                    "-o",
                    output_name,
                    str(scene_file),
                    "HungarianAlgorithmDemo",
                ]
                result = subprocess.run(
                    cmd,
                    cwd=str(project_root),
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    candidates = list(Path(temp_media).rglob(output_name))
                    if not candidates:
                        self._set_status("Render failed: video file not found after render.")
                        return

                    src_file = max(candidates, key=lambda p: p.stat().st_mtime)
                    out_file = project_root / output_name
                    shutil.copy2(src_file, out_file)
                    self._set_status(f"Render complete. Saved: {out_file}")
                    return

                combined = "\n".join(
                    part for part in [result.stdout.strip(), result.stderr.strip()] if part
                )
                lines = [line for line in combined.splitlines() if line.strip()]
                detail = lines[-1] if lines else f"Exit code {result.returncode}"

                if "No module named manim" in combined:
                    detail = (
                        f"Manim not installed in {python_exe}. "
                        "Run: .\\.venv\\Scripts\\Activate.ps1 ; python -m pip install manim numpy"
                    )
                elif "ffmpeg" in combined.lower():
                    detail = "ffmpeg missing. Run: winget install --id Gyan.FFmpeg -e"

                self._set_status(f"Render failed: {detail}")
        except Exception as exc:
            self._set_status(f"Failed to launch Manim: {exc}")


class HungarianAnimation(HungarianAnimator):
    pass


# Render with:
# manim -pqh hungarian/hungarian_animation.py HungarianAlgorithmDemo
