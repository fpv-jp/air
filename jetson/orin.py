import bpy
import sys
import types
import math

text = bpy.data.texts.get("base.py")
module_name = "base"
module = types.ModuleType(module_name)
exec(text.as_string(), module.__dict__)
sys.modules[module_name] = module

import base

#assembly = bpy.data.objects.get("000_ARVALA_TLA_ASM")
#assembly.hide_set(True)
base.init()
#assembly.hide_set(False)
#assembly.location = (-46.0, -22.6, -1.6)

#base.set_color(assembly, "Red", (0.8, 0.1, 0.1))

MAIN_WIDTH = 100.0
MAIN_HEIGHT = 79.0
MAIN_DEPTH = 12.5

MAIN_THICKNESS = 2.5
MAIN_GAP = 0.2

main = base.create_cube(
    scale=(MAIN_WIDTH + MAIN_THICKNESS, MAIN_HEIGHT + MAIN_THICKNESS, MAIN_DEPTH),
)
base.cut_corners(
    target=main,
    width=MAIN_WIDTH,
    height=MAIN_HEIGHT,
    depth=MAIN_DEPTH - MAIN_THICKNESS / 2,
    thickness=MAIN_THICKNESS / 2,
)
base.cut_cube(
    target=main,
    scale=(MAIN_WIDTH + MAIN_GAP, MAIN_HEIGHT + MAIN_GAP, MAIN_DEPTH),
    location=(0, 0, -MAIN_THICKNESS / 2),
)

base.cut_holes(
    target=main,
    radius=1.3,
    depth=MAIN_DEPTH + MAIN_THICKNESS,
    positions=[
        (40.0, 35.5),
        (40.0, -22.6),
        (-46.0, 35.5),
        (-46.0, -22.6),
    ],
)

## ----------------------------------------

main.location[2] = MAIN_DEPTH / 2

## ----------------------------------------

def cut_opening(scale, x, y):
    base.cut_cube(
        target=main,
        scale=scale,
        location=(x, y, 0.0),
    )


cut_opening(scale=(59.0, 40.0, MAIN_DEPTH*2), x=-2.0, y=19.5) # CPU
cut_opening(scale=( 6.0, 51.5, MAIN_DEPTH*2), x=46.0, y= 6.5) # GPIO
cut_opening(scale=( 4.5,  3.0, MAIN_DEPTH*2), x=29.0, y=31.0) # wire
base.cut_cylinder(
    target=main,
    radius=1.5,
    depth=MAIN_DEPTH*2,
    location=(31.25, 31.0, 0.0),
)

## ----------------------------------------

def cut_top_opening(scale, x):
    base.cut_cube(
        target=main,
        scale=scale,
        location=(
            x,
            MAIN_THICKNESS - (scale[1] - MAIN_HEIGHT ) / 2, 
            scale[2] / 2
        ),
    )

cut_top_opening(scale=(30.0, 5.0, 3.0), x= -14.5)  # System PIN

## ----------------------------------------

def cut_bottom_opening(scale, x):
    base.cut_cube(
        target=main,
        scale=scale,
        location=(
            x,
            (scale[1] - MAIN_HEIGHT ) / 2 - MAIN_THICKNESS, 
            scale[2] / 2
        ),
    )

cut_bottom_opening(scale=( 9.6,  5.0, 11.2), x= -44.0)  # DC
cut_bottom_opening(scale=(18.5,  5.0,  7.0), x= -27.3)  # DP
cut_bottom_opening(scale=(14.4, 18.7, 13.0), x=  -7.4)  # USB1
cut_bottom_opening(scale=(14.4, 18.7, 13.0), x=   9.6)  # USB2
cut_bottom_opening(scale=(16.5, 22.5, 13.0), x=  27.0)  # LAN
cut_bottom_opening(scale=( 9.3,  5.0,  3.7), x=  42.0)  # USB-C

## ----------------------------------------

def cut_left_opening(scale, y):
    base.cut_cube(
        target=main,
        scale=scale,
        location=(
            (scale[0] - MAIN_WIDTH ) / 2 - MAIN_THICKNESS, 
            y,
            scale[2] / 2
        ),
    )

cut_left_opening(scale=(6.0, 17.0, 2.0), y= 18.8)
cut_left_opening(scale=(6.0, 17.0, 2.0), y= -6.1)

## ----------------------------------------

main.rotation_euler[1] = math.pi

#main.location[0] = 14
#assembly.location[0] += main.location[0]

#main.location[0] = -MAIN_WIDTH / 2.5
#assembly.location[0] += main.location[0]

#main.location[1] = -MAIN_HEIGHT / 4
#assembly.location[1] += main.location[1]

#main.location[2] = 0
