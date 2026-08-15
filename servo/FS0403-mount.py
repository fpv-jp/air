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

M2 = 1.2
X = 10.5
Y = 6.25

MAIN_WIDTH = X*2 + M2*3.1
MAIN_HEIGHT = Y*2 + M2*3.1
MAIN_DEPTH = 1.5

main = base.create_cube(
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
)

base.cut_cube(
    target=main,
    scale=(MAIN_WIDTH-M2*5.25, MAIN_HEIGHT-M2*5.25, MAIN_DEPTH + 0.1),
)

holes = [(X, Y), (X, -Y), (-X, Y), (-X, -Y)]
for i, (x, y) in enumerate(holes):
    base.add_ring(
        target=main,
        outer_radius=M2 * 2.25,
        inner_radius=M2,
        location=(x, y, 0),
        depth=MAIN_DEPTH,
    )

################################################################

M1_3 = 0.75

P = 11.525

MAIN_WIDTH2 = 8.0
MAIN_HEIGHT2 = 26.0

P2 = MAIN_WIDTH2/2

left = base.create_cube(
    scale=(MAIN_WIDTH2, MAIN_HEIGHT2, MAIN_DEPTH),
)

holes = [(P2, 0), (P2, P), (P2, -P)]
for i, (x, y) in enumerate(holes):
    base.add_ring(
        target=left,
        outer_radius=M1_3 * 2.75,
        inner_radius=M1_3,
        location=(x-M1_3, y, 0),
        depth=MAIN_DEPTH,
    )

left.rotation_euler[1] = -math.pi / 2

left.location[0] = MAIN_WIDTH/2 + 1.25
left.location[1] = MAIN_HEIGHT/2 - 2.0
left.location[2] = MAIN_WIDTH2/2 - MAIN_DEPTH/2

base.modifier_apply(obj=left, target=main, operation="UNION")


left2 = base.create_cube(
    scale=(1, 6, MAIN_DEPTH),
)
left2.location[0] = MAIN_WIDTH/2

base.modifier_apply(obj=left2, target=main, operation="UNION")


#################################################################

#MAIN_HEIGHT3 = 1.5 * 4
M = 1.5

right = base.create_cube(
    scale=(MAIN_WIDTH2, M*4, MAIN_DEPTH),
)
base.add_ring(
    target=right,
    outer_radius=M*2,
    inner_radius=M,
    location=(MAIN_WIDTH2/2, 0, 0),
    depth=MAIN_DEPTH,
)
base.add_cube(
    target=right,
    scale=(MAIN_DEPTH, M*4, MAIN_DEPTH+1),
    location=(MAIN_DEPTH/2-MAIN_WIDTH2/2, 0.5, 0.5),
)

right.rotation_euler[1] = -math.pi / 2
right.rotation_euler[2] = math.pi

right.location[0] = -MAIN_WIDTH/2 - 1.25
right.location[1] = MAIN_HEIGHT/2 - 2.0
right.location[2] = MAIN_WIDTH2/2 - MAIN_DEPTH/2

base.modifier_apply(obj=right, target=main, operation="UNION")
