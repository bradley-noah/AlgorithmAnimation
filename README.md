# Algorithm Animation
 
Three algorithms and their respective animators built with Python. Gale-Shapley and Dinic use Tkinter (no extra dependencies). The Hungarian algorithm uses Manim for rendering. Please see GroupRoles.txt for a complete list of our group members.
 
---

## Project Structure
```
AlgorithmAnimation/
├── main.py                                 # launcher – opens all three windows
│
├── GroupRoles.txt  
│
├── shared/
│   ├── __init__.py
│   └── animation.py                        # BaseAnimator, colors
│
├── hungarian/                              # Each algorithm has a seperate file for
│   ├── hungarian.py                        # algorithm implementation
│   ├── hungarian_animation.py              # animator
│   ├── hungarian_testing.py                # correctness tests
│   └── HungarianAlgorithmDemo_6x6.mp4      # video demo
│
├── gale_shapley/                   
│   ├── gale_shapely.py             
│   ├── gale_shapley_animation.py   
│   ├── gale_shapley_testing.py    
│   └── GaleShapleyDemo.mp4       
│
└── dinic/
    ├── dinic.py
    ├── dinic_animation.py
    ├── dinic_testing.py 
    └── DinicDemo.mp4
```   

---

## Running 

```bash

# All three windows at once
python main.py

# One at a time
python main.py gale_shapley
python main.py hungarian
python main.py dinic

# Animation without main
python -m dinic.dinic_animation

# Algorithm without main
python dinic/dinic.py

# Testing without main
python dinic/dinic_testing.py


```
**Note**: If on Windows and have the Windows Python package installed, the 'python' command may need to be replaced with 'python.exe' to ensure dependencies are included natively.

---
 
## Dependencies
 
Gale-Shapley and Dinic require no installation beyond Python's standard library.
 
Hungarian requires Manim and its dependencies:
 
```bash
pip install manim numpy
```
 
FFmpeg is also required for Manim to render video:
 
```bash
# macOS
brew install ffmpeg
 
# Windows
winget install --id Gyan.FFmpeg -e
```