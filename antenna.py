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

MAIN_WIDTH = 34
MAIN_HEIGHT = 18
MAIN_DEPTH = 11.6

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

base.cut_inner_corners(
    target=main,
    width=MAIN_WIDTH,
    height=MAIN_HEIGHT,
    depth=MAIN_DEPTH,
    thickness=MAIN_THICKNESS,
)

#############################################################################

MAIN_WIDTH2 = 21.3
MAIN_HEIGHT2 = 8.0

main2 = base.create_cube(
    scale=(MAIN_WIDTH2 + MAIN_THICKNESS*2, MAIN_HEIGHT2, MAIN_DEPTH),
)
base.cut_cube(target=main2,
    scale=(MAIN_WIDTH2, MAIN_HEIGHT2, MAIN_DEPTH+0.1),
)
base.cut_cylinder(
    target=main2,
    radius=1.75,
    depth=35,
    rotation=(0, math.pi / 2, 0),
#    location=(0, 0.1, 0),
)

main2.location=(0, (MAIN_HEIGHT+MAIN_HEIGHT2)/2+MAIN_THICKNESS, 0)

base.modifier_apply(obj=main2, target=main, operation="UNION")

#############################################################################

main.location=(0, 0, MAIN_DEPTH/2 - MAIN_THICKNESS/2)

MAIN_WIDTH = 44

M = 3.25

X = MAIN_WIDTH/2+M

base.add_cube(
    target=main,
    scale=(
        MAIN_WIDTH + M * 2,
        M * 4,
        MAIN_THICKNESS,
    ),
)
for i, (x) in enumerate([X, -X]):
    base.add_ring(
        target=main,
        outer_radius=M * 2,
        inner_radius=M,
        depth=MAIN_THICKNESS,
        location=(x, 0, 0),
    )
