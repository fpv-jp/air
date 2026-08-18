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

MAIN_THICKNESS = 1.25

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
        scale=(1.8, MAIN_HEIGHT+MAIN_THICKNESS*3, MAIN_DEPTH),
        location=(x, 0, MAIN_THICKNESS*2),
    )

ubec.location = (0.0, 0.0, (MAIN_DEPTH - MAIN_THICKNESS) / 2)

M = 1.7

X = 30.5/2
Y = 30.5/2
pos = [
    (X, Y),
    (-X, Y),
    (X, -Y),
    (-X, -Y),
]
for i, (x, y) in enumerate(pos):
    if x > 0:
        base.add_cube(
            target=ubec,
            scale=(
                x*2,
                M*4,
                MAIN_THICKNESS,
            ),
            location=(0.0, y, 0.0),
        )
    base.add_ring(
        target=ubec,
        outer_radius=M*2,
        inner_radius=M,
        depth=MAIN_THICKNESS,
        location=(x, y, 0.0),
    )

# USB-A

X = 18.5
Y = 6.0
pos = [
    (X, Y),
    (-X, Y),
    (X, -Y),
    (-X, -Y),
]
for i, (x, y) in enumerate(pos):
    if x > 0:
        base.add_cube(
            target=ubec,
            scale=(
                x*2,
                M*4,
                MAIN_THICKNESS,
            ),
            location=(0.0, y, 0.0),
        )
    base.add_ring(
        target=ubec,
        outer_radius=M*2,
        inner_radius=M,
        depth=MAIN_THICKNESS,
        location=(x, y, 0.0),
    )

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

##### wifi ----------------------------------------------------------------------------------------------------------------
##### wifi ----------------------------------------------------------------------------------------------------------------
##### wifi ----------------------------------------------------------------------------------------------------------------

#MAIN_WIDTH = 32.15
#MAIN_HEIGHT = 32.15
#MAIN_DEPTH = 3.5

#wifi = base.create_cube(
#    scale=(
#        MAIN_WIDTH + MAIN_THICKNESS * 2,
#        MAIN_HEIGHT + MAIN_THICKNESS * 2,
#        MAIN_DEPTH,
#    ),
#)

#base.cut_corners(
#    target=wifi,
#    width=MAIN_WIDTH,
#    height=MAIN_HEIGHT,
#    depth=MAIN_DEPTH - MAIN_THICKNESS,
#    thickness=MAIN_THICKNESS,
#)


#M = 1.7

#base.add_cube(
#    target=wifi,
#    scale=(MAIN_WIDTH*1.13+M*4, M*4, MAIN_THICKNESS),
#    location=(0, 0, -MAIN_DEPTH/2+MAIN_THICKNESS/2),
#)
#A=MAIN_HEIGHT*1.13+M*4
#base.add_cube(
#    target=wifi,
#    scale=(M*4, A/2, MAIN_THICKNESS),
#    location=(0, A/4, -MAIN_DEPTH/2+MAIN_THICKNESS/2),
#)

#base.cut_cube(
#    target=wifi,
#    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH+0.1),
#    location=(0.0, 0.0, MAIN_THICKNESS),
#)
#base.cut_inner_corners(
#    target=wifi,
#    width=MAIN_WIDTH-10,
#    height=MAIN_HEIGHT-10,
#    depth=MAIN_DEPTH+10,
#    thickness=MAIN_THICKNESS,
#)

###### ----------------------------------------------------------------------------------------------------------------

#base.cut_cube(
#    target=wifi,
#    scale=(18.0, MAIN_THICKNESS*3, MAIN_DEPTH+0.1),
#    location=(0, -MAIN_HEIGHT/2, 0),
#)

#base.cut_cube(
#    target=wifi,
#    scale=(MAIN_WIDTH + MAIN_THICKNESS * 3, 1.3, MAIN_DEPTH),
#    location=(0, 13.3, MAIN_THICKNESS*2),
#)

###### ----------------------------------------------------------------------------------------------------------------
#wifi.rotation_euler[2] = math.pi / 4

#X = 30.5/2
#Y = 30.5/2
#pos = [
#    (X, Y),
#    (-X, Y),
##    (X, -Y),
#    (-X, -Y),
#]
#for i, (x, y) in enumerate(pos):
#    base.add_ring(
#        target=wifi,
#        outer_radius=M*2,
#        inner_radius=M,
#        depth=MAIN_THICKNESS,
#        location=(x, y, -MAIN_DEPTH/2+MAIN_THICKNESS/2),
#    )
