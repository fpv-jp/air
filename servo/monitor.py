import bpy
import bmesh
import math
import sys
import types

text = bpy.data.texts.get("base.py")
module_name = "base"
module = types.ModuleType(module_name)
exec(text.as_string(), module.__dict__)
sys.modules[module_name] = module

import base

# 初期化
base.init()

MAIN_WIDTH = 106
MAIN_HEIGHT = 68
MAIN_DEPTH = 9

MAIN_THICKNESS = 2.5

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
    location=(0, 0, 1),
)

base.cut_cube(
    target=main,
    scale=(
        MAIN_WIDTH-9,
        MAIN_HEIGHT-7,
        MAIN_DEPTH,
    ),
)

############################

M = 6.8
D = 1.75

X = MAIN_WIDTH/2+MAIN_THICKNESS/2
Y = MAIN_HEIGHT/2.75


for i, (x) in enumerate([X, -X]):
    base.add_cube(
        target=main,
        scale=(
            D,
            M * 2,
            MAIN_DEPTH,
        ),
        location=(x, Y, MAIN_DEPTH/2),
    )
    base.add_ring(
        target=main,
        outer_radius=M,
        inner_radius=M/2,
        depth=D,
        location=(x, Y, MAIN_DEPTH),
        rotation=(0, math.pi / 2, 0),
    )
