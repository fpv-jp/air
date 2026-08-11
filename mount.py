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

# main -----------------------------------

MAIN_WIDTH = 72.0
MAIN_HEIGHT = 100.0
MAIN_DEPTH = 2.5

WALL = 8.0

main = base.create_cube(
    scale=(
        MAIN_WIDTH ,
        MAIN_HEIGHT,
        MAIN_DEPTH,
    ),
)

# -----------------------------------

S = 30

base.cut_cylinder(
    target=main,
    radius=1.75,
    depth=MAIN_DEPTH,
    location=((MAIN_WIDTH-WALL)/2, S-WALL/2, 0),
)
base.cut_cylinder(
    target=main,
    radius=1.75,
    depth=MAIN_DEPTH,
    location=((MAIN_WIDTH-WALL)/2, 0, 0),
)

base.cut_cylinder(
    target=main,
    radius=1.75,
    depth=MAIN_DEPTH,
    location=(-(MAIN_WIDTH-WALL)/2, MAIN_HEIGHT/4, 0),
)
base.cut_cylinder(
    target=main,
    radius=1.75,
    depth=MAIN_DEPTH,
    location=(-(MAIN_WIDTH-WALL)/2, -MAIN_HEIGHT/4, 0),
)

# -----------------------------------

base.cut_cube(
    target=main,
    scale=(
        MAIN_WIDTH -WALL*2,
        MAIN_HEIGHT -WALL*2,
        MAIN_DEPTH,
    ),
    location=(0, MAIN_HEIGHT/2-WALL, 0),
)


base.cut_cube(
    target=main,
    scale=(
        MAIN_WIDTH,
        MAIN_HEIGHT,
        MAIN_DEPTH,
    ),
    location=(WALL, -MAIN_HEIGHT/2-WALL, 0),
)

#base.add_cube(
#    target=main,
#    scale=(
#        S,
#        S,
#        MAIN_DEPTH,
#    ),
#    location=((MAIN_WIDTH-S)/2-WALL, S/2, 0),
#)

base.cut_cube(
    target=main,
    scale=(
        MAIN_WIDTH,
        MAIN_HEIGHT,
        MAIN_DEPTH,
    ),
    location=(WALL, MAIN_HEIGHT/2+S, 0),
)

# -----------------------------------
