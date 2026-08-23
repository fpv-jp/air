import bpy
import math
import sys
import types

text = bpy.data.texts.get("base.py")
module_name = "base"
module = types.ModuleType(module_name)
exec(text.as_string(), module.__dict__)
sys.modules[module_name] = module

import base

base.init()


WALL = 1.75

MAIN_WIDTH = 7.4
MAIN_HEIGHT = 35.2
MAIN_DEPTH = 20.0

# --------------------------------

main = base.create_cube(
    scale=(MAIN_WIDTH + WALL*2, MAIN_HEIGHT + WALL*2, MAIN_DEPTH + WALL*2),
)

base.cut_cube(
    target=main,
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH + WALL*2),
    location=(0, 0, WALL),
)

base.cut_cube(
    target=main,
    scale=(MAIN_WIDTH + WALL*3, MAIN_HEIGHT-WALL*4, MAIN_DEPTH-WALL*2),
    location=(0, 0, -WALL),
)

main.location=(0, 0, (MAIN_DEPTH + WALL)/2)

# --------------------------------

base.add_cube(
    target=main,
    scale=(64.0, 16.0, WALL),
    location=(30.0, 0.0, 0.0),
)

# --------------------------------

PITCH = 6.4 + 3.0

base.cut_cylinder(
    target=main, radius=1.5, depth=WALL*2, 
    location=(58.0, PITCH/2, 0.0)
)
base.cut_cylinder(
    target=main, radius=1.5, depth=WALL*2, 
    location=(58.0, -PITCH/2, 0.0)
)

