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

MAIN_WIDTH = 55.6
MAIN_HEIGHT = 40.1
MAIN_DEPTH = 8.6

MAIN_THICKNESS = 1.25

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

base.cut_cube(
    target=main,
    scale=(44.2, 29.1, MAIN_DEPTH+0.1),
)

main.location[2] = MAIN_DEPTH/2

### ----------------------------------------------------------------------------------------------------------------

depth=3.1

mounts_pins = [
    (23.85, 16.4),
    (23.85, -16.4),
    (-23.85, 16.4),
    (-23.85, -16.4)
]
for i, (x, y) in enumerate(mounts_pins):
    base.add_ring(
        target=main,
        outer_radius=2.75,
        inner_radius=1.5,
        depth=depth,
        location=(x, y, depth/2),
    )

### ----------------------------------------------------------------------------------------------------------------

triangles = [
    (-22.25, 15.0),
    (22.25, 15.0),
    (22.25, -15.0,),
    (-22.25, -15.0)
]
for i, (x, y) in enumerate(triangles):
    base.add_triangle(
        target=main,
        verts=[(3.5, 0, 0), (0, 3.5, 0), (0, 0, 0)],
        depth=MAIN_THICKNESS,
        location=(x, y, 0),
        rotation=(0, 0, math.radians(270 -i*90)),
    )

### ubec ----------------------------------------------------------------------------------------------------------------
### ubec ----------------------------------------------------------------------------------------------------------------
### ubec ----------------------------------------------------------------------------------------------------------------

MAIN_WIDTH = 21.8
MAIN_HEIGHT = 43.0

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
base.cut_inner_corners(
    target=ubec,
    width=MAIN_WIDTH-10,
    height=MAIN_HEIGHT-10,
    depth=MAIN_DEPTH+10,
    thickness=MAIN_THICKNESS,
)

### ----------------------------------------------------------------------------------------------------------------

# wire
for i, (x) in enumerate([8.0, -8.0]):
    base.cut_cube(
        target=ubec,
        scale=(1.8, MAIN_HEIGHT+MAIN_THICKNESS*3, MAIN_DEPTH),
        location=(x, 0, MAIN_THICKNESS*2),
    )

# beam

#X = 8.0
#Y = 4.0
#Z = 45.0
#YP = MAIN_HEIGHT/2+2.0
#for i, (yp) in enumerate([YP, -YP]):
#    base.add_cube(
#        target=ubec,
#        scale=(X, Y, Z),
#        location=(0, yp, (Z-MAIN_DEPTH)/2),
#    )
#    base.add_cube(
#        target=ubec,
#        scale=(MAIN_WIDTH-MAIN_THICKNESS, Y, MAIN_THICKNESS*2),
#        location=(0, yp,  (MAIN_THICKNESS*2-MAIN_DEPTH)/2),
#    )
#    base.add_ring(
#        target=ubec,
#        outer_radius=X/2,
#        inner_radius=1.75,
#        depth=Y,
#        location=(0, yp, Z-X/2),
#        rotation=(math.pi / 2, 0, 0),
#    )

### ----------------------------------------------------------------------------------------------------------------
ubec.location[0] = -56.2/2-MAIN_WIDTH/2-MAIN_THICKNESS
ubec.location[2] = MAIN_DEPTH/2

main.location[0] = 0
main.location[1] = 0
main.location[2] = 8.6/2

base.modifier_apply(obj=ubec, target=main, operation="UNION")

### wifi ----------------------------------------------------------------------------------------------------------------
### wifi ----------------------------------------------------------------------------------------------------------------
### wifi ----------------------------------------------------------------------------------------------------------------

MAIN_WIDTH = 32.15
MAIN_HEIGHT = 32.15

MAIN_DEPTH = 5.0

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
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH+0.1),
    location=(0.0, 0.0, MAIN_THICKNESS),
)
base.cut_inner_corners(
    target=wifi,
    width=MAIN_WIDTH-10,
    height=MAIN_HEIGHT-10,
    depth=MAIN_DEPTH+10,
    thickness=MAIN_THICKNESS,
)

#### ----------------------------------------------------------------------------------------------------------------

base.cut_cube(
    target=wifi,
    scale=(MAIN_THICKNESS*3, 18.0, MAIN_DEPTH+0.1),
    location=(-MAIN_WIDTH/2, 0, 0),
)
base.cut_cube(
    target=wifi,
    scale=(1.3, MAIN_HEIGHT + MAIN_THICKNESS * 3, MAIN_DEPTH),
    location=(13.3, 0, MAIN_THICKNESS*2),
)

#### ----------------------------------------------------------------------------------------------------------------

wifi.location[0] = -(56.2+MAIN_WIDTH)/2 - MAIN_THICKNESS * 2
wifi.location[2] = MAIN_DEPTH/2

main.location[0] += 21.8

base.modifier_apply(obj=wifi, target=main, operation="UNION")
