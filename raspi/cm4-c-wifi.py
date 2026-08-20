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

CM4_WIDTH = 47.7
CM4_HEIGHT = 32.8
CM4_DEPTH = 1.5

M = 1.4

main = base.create_cube(
    scale=(
        CM4_WIDTH,
        CM4_HEIGHT+M * 3,
        CM4_DEPTH,
    ),
)

base.cut_cube(
    target=main,
    scale=(CM4_WIDTH + M * 5, CM4_HEIGHT - M *3, CM4_DEPTH+1),
)

X = CM4_WIDTH / 2
Y = CM4_HEIGHT / 2

for i, (x, y) in enumerate([(-X, Y), (-X, -Y)]):
    base.add_ring(
        target=main,
        outer_radius=M * 2.5,
        inner_radius=M,
        depth=CM4_DEPTH,
        location=(x, y, 0.0),
    )
for i, (x, y) in enumerate([(X, Y), (X, -Y)]):
    base.add_ring(
        target=main,
        outer_radius=M * 2.5,
        inner_radius=M,
        depth=CM4_DEPTH+3.5,
        location=(x, y, 3.5/2),
    )

#### wifi ----------------------------------------------------------------------------------------------------------------
#### wifi ----------------------------------------------------------------------------------------------------------------
#### wifi ----------------------------------------------------------------------------------------------------------------

MAIN_WIDTH = 32.15
MAIN_HEIGHT = 32.15
MAIN_DEPTH = 3.8

MAIN_THICKNESS = 1.5

wifi = base.create_cube(
    scale=(
        MAIN_WIDTH + MAIN_THICKNESS * 2,
        MAIN_HEIGHT + MAIN_THICKNESS * 2,
        MAIN_DEPTH,
    ),
)

base.cut_corners(
    target=wifi,
    width=MAIN_WIDTH,
    height=MAIN_HEIGHT,
    depth=MAIN_DEPTH - MAIN_THICKNESS,
    thickness=MAIN_THICKNESS,
)

base.cut_cube(
    target=wifi,
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
    location=(0.0, 0.0, MAIN_THICKNESS),
)
base.cut_inner_corners(
    target=wifi,
    width=MAIN_WIDTH-10,
    height=MAIN_HEIGHT-10,
    depth=MAIN_DEPTH+10,
    thickness=MAIN_THICKNESS,
)

###### ----------------------------------------------------------------------------------------------------------------

base.cut_cube(
    target=wifi,
    scale=(18.0, MAIN_THICKNESS*3, MAIN_DEPTH+0.1),
    location=(0, -MAIN_HEIGHT/2, 0),
)

base.cut_cube(
    target=wifi,
    scale=(MAIN_WIDTH + MAIN_THICKNESS * 3, 1.3, MAIN_DEPTH),
    location=(0, 13.3, MAIN_THICKNESS*2),
)

###### ----------------------------------------------------------------------------------------------------------------
wifi.location[2] = MAIN_DEPTH/2-MAIN_THICKNESS/2

wifi.rotation_euler[2] = math.pi / 2

base.modifier_apply(obj=wifi, target=main, operation="UNION")
