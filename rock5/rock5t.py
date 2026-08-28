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

bpy.data.objects.get("5T_PCBA_X1_0_20250110_ASM").hide_set(True)
base.init()
bpy.data.objects.get("5T_PCBA_X1_0_20250110_ASM").hide_set(False)


TOP = True
BOTTOM = True
BOTTOM = False
    
# main -----------------------------------
MAIN_WIDTH = 111.2
MAIN_HEIGHT = 83.0

MAIN_DEPTH = 9.0
MAIN_DEPTH1 = 9.0
MAIN_DEPTH2 = 7.2
MAIN_DEPTH = MAIN_DEPTH1 + MAIN_DEPTH2

MAIN_THICKNESS = 1.5

# X/Y coordinates use the board center as origin.

def create_case(depth):
    main = base.create_cube(
        scale=(
            MAIN_WIDTH + MAIN_THICKNESS * 2,
            MAIN_HEIGHT + MAIN_THICKNESS * 2,
            depth,
        ),
    )
    base.cut_corners(
        target=main,
        width=MAIN_WIDTH,
        height=MAIN_HEIGHT,
        depth=depth - MAIN_THICKNESS,
        thickness=MAIN_THICKNESS,
    )
    base.cut_inner_corners(
        target=main,
        width=MAIN_WIDTH,
        height=MAIN_HEIGHT,
        depth=depth,
        thickness=MAIN_THICKNESS,
    )
    return main

if TOP:
    top = create_case(MAIN_DEPTH1)

if BOTTOM:
    bottom = create_case(MAIN_DEPTH2)

def punch(obj):
    base.cut_holes(
        target=obj,
        radius=1.6,
        depth=MAIN_DEPTH,
        positions=[
            (52.0, -37.6),
            (-7.0, -37.6),
            (-52.1, -37.6),
            (-52.3, 19.5),
            (51.9, 11.5),
        ],
    )
    base.cut_holes(
        target=obj,
        radius=1.6,
        depth=MAIN_DEPTH,
        positions=[
            (-33.1, 2.0),
            (18.3, -18.0),
        ],
    )

if TOP:
    top.rotation_euler[0] = math.pi
    punch(top)

    ### --------------------------- CPU sink
    base.cut_cube(
        target=top,
        scale=(41.0, 41.0, MAIN_DEPTH),
        location=(
            -6.2,
            -3.8,
            0
        ),
    )

    ### --------------------------- M.2
    base.cut_cube(
        target=top,
        scale=(23.0, 7.0, MAIN_DEPTH),
        location=(
            38.2,
            -26.0,
            0
        ),
    )

    ### --------------------------- GPIO
    base.cut_cube(
        target=top,
        scale=(50.7, 5.1, MAIN_DEPTH),
        location=(
            23.0,
            -37.6,
            0
        ),
    )

    ### --------------------------- WIFI sink
    base.cut_cube(
        target=top,
        scale=(16.0, 21.0, MAIN_DEPTH),
        location=(
            -42.3,
            -18.4,
            0
        ),
    )


if BOTTOM:
    punch(bottom)

    ### --------------------------- AI sink
    base.cut_cube(
        target=bottom,
        scale=(41.0, 41.0, MAIN_DEPTH),
        location=(
            -23.2,
            7.8,
            0
        ),
    )

#################################################

if TOP:
    top.location[2] = MAIN_DEPTH1/2

if BOTTOM:
    bottom.location[2] = -MAIN_DEPTH2/2

#################################################


def cut_Y(scale, x, r=False):
    y = MAIN_HEIGHT / 2 - scale[1]/2 + MAIN_THICKNESS + 0.001
    z = scale[2]/2 - 0.001
    if r:
        y = -y
    base.cut_cube(
        target=top,
        scale=scale,
        location=(x, y, z),
    )

### --------------------------- 

H = 15.0
cut_Y(scale=(10.6, 12.6, H), x=  49.2) # DC
cut_Y(scale=(14.4, 16.9, H), x=  34.8) # USB1
cut_Y(scale=(14.4, 16.9, H), x=  16.8) # USB2
cut_Y(scale=( 5.9, 21.7, H), x=  1.1)  # HDMI1
cut_Y(scale=( 5.9, 21.7, H), x=-12.8)  # HDMI2
cut_Y(scale=(16.4, 20.4, H), x=-26.8)  # LAN1
cut_Y(scale=(16.4, 20.4, H), x=-45.9)  # LAN2

### --------------------------- 

cut_Y(scale=(2.7, 2.6, 3.5), x=-45.0, r=True)  # PW switch
cut_Y(scale=(6.5, 2.6, 5.2), x=-36.3, r=True)  # Audio Jack
cut_Y(scale=(9.2, 2.6, 3.0), x=-22.3, r=True)  # SPI
cut_Y(scale=(2.7, 2.6, 1.5), x=-13.0, r=True)  # USB-C


#################################################

def cut_X(scale, y, r=False):
    x = MAIN_WIDTH / 2 - scale[0]/2 + MAIN_THICKNESS + 0.001
    z = scale[2]/2 - 0.001
    if r:
        x = -x
    base.cut_cube(
        target=top,
        scale=scale,
        location=(x, y, z),
    )

### --------------------------- 

cut_X(scale=(8.5, 15.7, 5.6), y=-0.4)  # Maskrom BTN
cut_X(scale=(2.7, 2.6, 3.5), y=20.3)   # HDMI
cut_X(scale=(2.7, 2.6, 3.5), y=-14.0)  # Recovery BTN

### --------------------------- 

cut_X(scale=(6.7, 15.0, 4.0), y=3.0, r=True)


# ##################################################
if TOP:
    top.location[0] = 8.1
    top.location[1] = 1.3

# top.rotation_euler[1] = math.pi

# ##################################################

# base.cut_cube(
#     target=top,
#     scale=(MAIN_WIDTH*1.2, MAIN_HEIGHT*1.2, MAIN_DEPTH1),
#     location=(0, 0, MAIN_THICKNESS+MAIN_DEPTH1/2),
# )
