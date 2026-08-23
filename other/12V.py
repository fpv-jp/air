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



MAIN_WIDTH = 68.2
MAIN_HEIGHT = 17.3
MAIN_DEPTH = 12.5

MAIN_THICKNESS = 3.0

# --------------------------------

main = base.create_cube(
    scale=(
        MAIN_WIDTH, 
        MAIN_HEIGHT+MAIN_THICKNESS*2, 
        MAIN_DEPTH+MAIN_THICKNESS),
)
base.cut_cube(
    target=main,
    scale=(
        MAIN_WIDTH+MAIN_THICKNESS,
        MAIN_HEIGHT,
        MAIN_DEPTH,
    ),
    location=(0.0, 0.0, MAIN_THICKNESS/2),
)

W1 = 12.5
base.cut_cube(
    target=main,
    scale=(
        W1,
        MAIN_HEIGHT+MAIN_THICKNESS*3,
        MAIN_DEPTH,
    ),
    location=(
        -MAIN_WIDTH/2+W1/2+2.8, 
        0.0, 
        MAIN_THICKNESS/2
    ),
)

W2 = 2.5
base.cut_cube(
    target=main,
    scale=(
        W2,
        MAIN_HEIGHT+MAIN_THICKNESS*3,
        MAIN_DEPTH,
    ),
    location=(
        -MAIN_WIDTH/2+W2/2+20.8, 
        0.0, 
        MAIN_THICKNESS/2
    ),
)

# --------------------------------

base.add_cube(
    target=main,
    scale=(
        MAIN_WIDTH/2,
        MAIN_HEIGHT,
        MAIN_DEPTH,
    ),
    location=(MAIN_WIDTH/4, 0.0, MAIN_THICKNESS/2),
)

base.cut_cube(
    target=main,
    scale=(
        MAIN_WIDTH/2,
        11.0,
        MAIN_DEPTH,
    ),
    location=(MAIN_WIDTH/4, -MAIN_HEIGHT/2+11.0/2, MAIN_THICKNESS/2),
)
