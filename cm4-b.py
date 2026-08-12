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

MAIN_WIDTH = 56.2
MAIN_HEIGHT = 41.1
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

depth=2.8

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

### ----------------------------------------------------------------------------------------------------------------

main.location[2] = -MAIN_DEPTH/2

# eth
base.cut_cube(
    target=main,
    scale=(16.7, MAIN_THICKNESS*3, 5.2),
    location=(-18.45, MAIN_HEIGHT/2, 0),
)

# sd-card
base.cut_cube(
    target=main,
    scale=(11.2, MAIN_THICKNESS*3, 6.2),
    location=(20.5, MAIN_HEIGHT/2, 0),
)

# audio
base.cut_cylinder(
    target=main,
    radius=2.5,
    depth=MAIN_THICKNESS*3,
    location=(MAIN_WIDTH/2, 7.35, 2.0),
    rotation=(0, math.pi / 2, 0)
)

main.location[1] = MAIN_HEIGHT/2 + MAIN_THICKNESS
main.location[2] = 0

### ubec ----------------------------------------------------------------------------------------------------------------
### ubec ----------------------------------------------------------------------------------------------------------------
### ubec ----------------------------------------------------------------------------------------------------------------

MAIN_WIDTH = 54.0
MAIN_HEIGHT = 22.0

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
for i, (y) in enumerate([8.0, -8.0]):
    base.cut_cube(
        target=ubec,
        scale=(MAIN_THICKNESS*3, 1.8, MAIN_DEPTH),
        location=(-MAIN_WIDTH/2, y, MAIN_THICKNESS*2),
    )

# beam
X = 4.0
Y = 8.0
Z = 45.0
XP = MAIN_WIDTH/2+2.0
for i, (xp) in enumerate([XP, -XP]):
    base.add_cube(
        target=ubec,
        scale=(X, Y, Z),
        location=(xp, 0.0, (Z-MAIN_DEPTH)/2),
    )
    base.add_cube(
        target=ubec,
        scale=(X, MAIN_HEIGHT-MAIN_THICKNESS*2, MAIN_THICKNESS*2),
        location=(xp, 0.0, (MAIN_THICKNESS*2-MAIN_DEPTH)/2),
    )
    base.add_ring(
        target=ubec,
        outer_radius=Y/2,
        inner_radius=1.75,
        depth=X,
        location=(xp, 0.0, Z-Y/2),
        rotation=(0, math.pi / 2, 0),
    )

# filling
XP = (MAIN_WIDTH+MAIN_THICKNESS)/2
YP = (MAIN_HEIGHT+MAIN_THICKNESS)/2
Z = 5.0
base.add_cube(
    target=ubec,
    scale=(MAIN_THICKNESS, MAIN_THICKNESS, MAIN_DEPTH),
    location=(-XP, YP, 0),
)
base.add_cube(
    target=ubec,
    scale=(MAIN_THICKNESS, MAIN_THICKNESS, Z),
    location=(-XP, -YP, -(MAIN_DEPTH-Z)/2),
)

### ----------------------------------------------------------------------------------------------------------------

ubec.location[0] = (MAIN_WIDTH - 56.2)/2
ubec.location[1] = -MAIN_HEIGHT/2

base.modifier_apply(obj=ubec, target=main, operation="UNION")

main.location[1] += MAIN_HEIGHT + MAIN_THICKNESS/2

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

### ----------------------------------------------------------------------------------------------------------------

base.cut_cube(
    target=wifi,
    scale=(18.0, MAIN_THICKNESS*3, MAIN_DEPTH+0.1),
    location=(0, -MAIN_HEIGHT/2, 0),
)
base.cut_cube(
    target=wifi,
    scale=(MAIN_WIDTH + MAIN_THICKNESS * 3, 1.3, MAIN_DEPTH),
    location=(0, 13.8, MAIN_THICKNESS*2),
)

### ----------------------------------------------------------------------------------------------------------------

wifi.location[0] = (MAIN_WIDTH - 56.2)/2
wifi.location[1] = -(MAIN_HEIGHT+MAIN_THICKNESS)/2
wifi.location[2] = MAIN_DEPTH/2

main.location[2] = 8.6/2

base.modifier_apply(obj=wifi, target=main, operation="UNION")
