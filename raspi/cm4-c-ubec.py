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
        CM4_WIDTH+M * 3,
        CM4_HEIGHT,
        CM4_DEPTH,
    ),
)

base.cut_cube(
    target=main,
    scale=(CM4_WIDTH - M * 4, CM4_HEIGHT +1, CM4_DEPTH+1),
)

X = CM4_WIDTH / 2
Y = CM4_HEIGHT / 2

for i, (x, y) in enumerate([(X, Y), (X, -Y), (-X, Y), (-X, -Y)]):
    base.add_ring(
        target=main,
        outer_radius=M * 2.5,
        inner_radius=M,
        depth=CM4_DEPTH,
        location=(x, y, 0.0),
    )

#### ubec ----------------------------------------------------------------------------------------------------------------
#### ubec ----------------------------------------------------------------------------------------------------------------
#### ubec ----------------------------------------------------------------------------------------------------------------


MAIN_THICKNESS = 1.5

MAIN_WIDTH = 21.6
MAIN_HEIGHT = 42.8
MAIN_DEPTH = 9.6

ubec = base.create_cube(
    scale=(
        MAIN_WIDTH + MAIN_THICKNESS * 2,
        MAIN_HEIGHT + MAIN_THICKNESS * 2,
        MAIN_DEPTH,
    ),
)

base.cut_corners(
    target=ubec,
    width=MAIN_WIDTH,
    height=MAIN_HEIGHT,
    depth=MAIN_DEPTH - MAIN_THICKNESS,
    thickness=MAIN_THICKNESS,
)
base.cut_inner_corners(
    target=ubec,
    width=MAIN_WIDTH,
    height=MAIN_HEIGHT,
    depth=MAIN_DEPTH,
    thickness=MAIN_THICKNESS,
)

### ----------------------------------------------------------------------------------------------------------------

# wire
for i, (x) in enumerate([8.0, -8.0]):
    base.cut_cube(
        target=ubec,
        scale=(1.8, MAIN_HEIGHT, MAIN_DEPTH),
        location=(x, MAIN_HEIGHT/2, MAIN_THICKNESS*2),
    )
    
for i, (x) in enumerate([6.0, -6.0]):
    base.cut_cube(
        target=ubec,
        scale=(1.8, MAIN_HEIGHT, MAIN_DEPTH),
        location=(x, -MAIN_HEIGHT/2, MAIN_THICKNESS*2),
    )

ubec.location = (0.0, 0.0, (MAIN_DEPTH - MAIN_THICKNESS) / 2)

# USB-HUB

M = 1.3

X = 17.2/2
Y = 24.8/2
pos = [
    (X, -Y),
    (-X, -Y),
    (0, Y),
]
for i, (x, y) in enumerate(pos):
    base.add_ring(
        target=ubec,
        outer_radius=M*2,
        inner_radius=M,
        depth=MAIN_THICKNESS,
        location=(x, y, 0.0),
    )

### ----------------------------------------------------------------------------------------------------------------

base.cut_cylinder(
    target=ubec,
    radius=7.5,
    depth=MAIN_THICKNESS,
)

####### ----------------------------------------------------------------------------------------------------------------
ubec.location[2] = MAIN_DEPTH/2-MAIN_THICKNESS/2

ubec.rotation_euler[2] = math.pi / 2

base.modifier_apply(obj=ubec, target=main, operation="UNION")
