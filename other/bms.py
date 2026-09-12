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

MAIN_WIDTH = 65.2 
MAIN_HEIGHT = 45.3

MAIN_THICKNESS = 2.0
MAIN_DEPTH = 3.3 + MAIN_THICKNESS

# --------------------------------
main = base.create_cube(
    scale=(
        MAIN_WIDTH + MAIN_THICKNESS * 2,
        MAIN_HEIGHT + MAIN_THICKNESS * 2,
        MAIN_DEPTH,
    ),
)

base.cut_corners(
    target=main,
    width=MAIN_WIDTH,
    height=MAIN_HEIGHT,
    depth=MAIN_DEPTH - MAIN_THICKNESS,
    thickness=MAIN_THICKNESS,
)

base.cut_cube(
    target=main,
    scale=(
        MAIN_WIDTH,
        MAIN_HEIGHT,
        MAIN_DEPTH,
    ),
    location=(0.0, 0.0, MAIN_THICKNESS),
)

#===================================================

M3 = 3.0
X = (36.75+42.45)/4
Y = (53.9+59.9)/4
Z = (MAIN_THICKNESS-MAIN_DEPTH)/2

for i, (x) in enumerate([(X), (-X)]):
    base.add_cube(
        target=main,
        scale=(
            M3*2,
            Y*2,
            MAIN_THICKNESS,
        ),
        location=(x, 0.0, Z),
    )

for i, (x, y) in enumerate([(X, Y), (X, -Y), (-X, -Y), (-X, Y)]):
        base.add_ring(
            target=main,
            outer_radius=M3,
            inner_radius=M3 / 2,
            depth=MAIN_THICKNESS,
            location=(x, y, Z),
        )

#===================================================

W = 6.0
def cut(x, y):
    base.cut_cube(
        target=main,
        scale=(
            W,
            W,
            MAIN_DEPTH*2,
        ),
        location=(x, y, 0.0),
    )

BASE_X = MAIN_WIDTH/2-W/2 - 0.5
BASE_Y = MAIN_HEIGHT/2-W/2 - 0.5
BASE_W = W/2+1

cut(BASE_X, BASE_W)
cut(BASE_X, -BASE_W)

cut(BASE_X, BASE_Y)
cut(BASE_X, -BASE_Y)

cut(5-BASE_X, BASE_Y)
cut(5-BASE_X, -BASE_Y)

W = 3.0
cut(3.5-BASE_X, -W/2)

base.cut_cube(
    target=main,
    scale=(
        35.0,
        12.5,
        MAIN_DEPTH,
    ),
    location=(0.0, -12.5/2 - 3, 0.0),
)
