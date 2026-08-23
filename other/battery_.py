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

MAIN_WIDTH = 82.0
MAIN_HEIGHT = 79.2
MAIN_DEPTH = 7.0

MAIN_THICKNESS = 2.0

# --------------------------------

main = base.create_cube(
    scale=(
        MAIN_WIDTH+MAIN_THICKNESS*2, 
        MAIN_HEIGHT+MAIN_THICKNESS*2, 
        MAIN_DEPTH+MAIN_THICKNESS
    ),
)

# --------------------------------

P = 19.8
for i, (p) in enumerate([(P*1.5),(P/2),(-P/2),(-P*1.5)]):
    base.add_cube(
        target=main,
        scale=(
            6.8+6,
            MAIN_HEIGHT+10.0,
            MAIN_DEPTH+MAIN_THICKNESS,
        ),
        location=(p, 0.0, 0.0),
    )
    base.cut_cube(
        target=main,
        scale=(
            6.8,
            MAIN_HEIGHT+7.0,
            MAIN_DEPTH+MAIN_THICKNESS,
        ),
        location=(p, 0.0, MAIN_THICKNESS),
    )
    
    base.cut_cube(
        target=main,
        scale=(
            8.5,
            67.3,
            MAIN_DEPTH*2,
        ),
        location=(p, 0.0, 0.0),
    )

# --------------------------------

base.cut_cube(
    target=main,
    scale=(
        MAIN_WIDTH,
        MAIN_HEIGHT,
        MAIN_DEPTH,
    ),
    location=(0.0, 0.0, MAIN_THICKNESS/2),
)

# --------------------------------

X = (36.75+42.45)/4
Y = (53.9+59.9)/4
for i, (x, y) in enumerate([(X, Y), (X, -Y), (-X, -Y), (-X, Y)]):
    base.cut_cylinder(
        target=main,
        radius=1.9,
        depth=MAIN_DEPTH*2,
        location=(x, y, 0.0),
    )

# --------------------------------
