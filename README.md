# Algorithm Animation Project

Three algorithms and their respective animators built with Python + Tkinter (no extra dependencies).

---
# Project Structure
```
AlgorithmAnimation/
├── main.py                          # launcher – opens all three windows
│
├── GroupRoles.txt  
│
├── shared/
│   ├── __init__.py
│   └── animation.py                 # BaseAnimator, colors
│
├── hungarian/
│   ├── hungarian.py
│   └── hungarian_animation.py   
│
├── gale_shapley/
│   ├── gale_shapely.py
│   └── gale_shapley_animation.py       
│
└── dinic/
    ├── dinic.py
    └── dinic_animation.py 
```        
```

# Running 

# All three windows at once
python main.py

# One at a time
python main.py gale
python main.py hungarian
python main.py dinic

# Animation without main
python -m dinic.dinic_animation

# Algorithm without main
python dinic/dinic.py

# Testing without main
python gale_shapley/gale_shapley_testing.py


```
**Note**: If on Windows and have the Windows Python package installed, the 'python' command may need to be replaced with 'python.exe' to ensure dependencies are included natively.


