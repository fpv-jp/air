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

MAIN_WIDTH = 47.3
MAIN_HEIGHT = 10.7
MAIN_DEPTH = 5.0

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

base.cut_cube(
    target=main,
    scale=(
        2.3,
        MAIN_HEIGHT*2,
        4.0,
    ),
    location=(0.0, 0.0, MAIN_DEPTH/2),
)

# --------------------------------

X = (33+40)/4
for i, (x, y) in enumerate([(X, 0), (-X, 0)]):
    base.cut_cylinder(
        target=main,
        radius=1.9,
        depth=MAIN_DEPTH*2,
        location=(x, y, 0.0),
    )

# --------------------------------
