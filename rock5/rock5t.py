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

#bpy.data.objects.get("5T_PCBA_X1_0_20250110_ASM").hide_set(True)
base.init()
#bpy.data.objects.get("5T_PCBA_X1_0_20250110_ASM").hide_set(False)


TOP = True
TOP = False
BOTTOM = True
#BOTTOM = False
    
# main -----------------------------------
MAIN_WIDTH = 111.2
MAIN_HEIGHT = 83.0

MAIN_DEPTH1 = 9.6
MAIN_DEPTH2 = 8.2
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
            ( 52.0, -37.6),
            ( -6.8, -37.6),
            (-52.0, -37.6),
            (-52.0,  19.5),
            ( 52.0,  11.5),
        ],
    )
    base.cut_holes(
        target=obj,
        radius=1.6,
        depth=MAIN_DEPTH,
        positions=[
            (-32.6, 2.0),
            (18.9, -18.0),
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
            1.2,
            -10.6,
            0
        ),
    )

    ### --------------------------- M.2
    base.cut_cube(
        target=top,
        scale=(23.3, 7.2, MAIN_DEPTH),
        location=(
            39.9,
            -28.6,
            0
        ),
    )
    base.cut_cylinder(
        target=top,
        radius=2.7,
        depth=MAIN_DEPTH,
        location=(39.9, 11.7, 0),
    )

    ### --------------------------- GPIO
    base.cut_cube(
        target=top,
        scale=(51.2, 5.6, MAIN_DEPTH),
        location=(
            22.3,
            -37.6,
            0
        ),
    )

    ### --------------------------- WIFI sink
    base.cut_cube(
        target=top,
        scale=(16.0, 21.0, MAIN_DEPTH),
        location=(
            -41.2,
            -15.4,
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
            6.0,
            11.5,
            0
        ),
        rotation=(0, 0, math.pi/4),
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

H = 15.0

if TOP:
    ### --------------------------- 
    
    cut_Y(scale=(10.6, 12.3, H), x= 49.2) # DC
    cut_Y(scale=(14.4, 16.7, H), x= 34.8) # USB1
    cut_Y(scale=(14.4, 16.7, H), x= 16.8) # USB2
    cut_Y(scale=( 6.1, 21.8, H), x=  1.1) # HDMI1
    cut_Y(scale=( 6.1, 21.8, H), x=-12.8) # HDMI2
    cut_Y(scale=(16.4, 20.4, H), x=-26.8) # LAN1
    cut_Y(scale=(16.4, 20.4, H), x=-45.9) # LAN2

    ### --------------------------- 

    cut_Y(scale=(3.0, 2.6, 4.5), x=-44.4, r=True)  # PW switch
    cut_Y(scale=(6.5, 2.6, 4.1), x=-35.9, r=True)  # Audio Jack
    base.cut_cylinder(
        target=top,
        radius=6.5/2,
        depth=3.2,
        location=(-35.9, -MAIN_HEIGHT / 2, 4.1),
        rotation=(math.pi/2, 0, 0),
    )
    cut_Y(scale=(9.4, 2.6, 5.0), x=-21.8, r=True)  # USB-C
    cut_Y(scale=(2.7, 2.6, 3.0), x=-12.5, r=True)  # SPI


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

if TOP:
    ### --------------------------- 

    cut_X(scale=(3.0,  3.0, 4.8), y= 20.3) # Maskrom BTN
    cut_X(scale=(3.0, 15.6, 8.0), y=-0.5)  # HDMI
    cut_X(scale=(3.0,  3.0, 4.8), y=-13.6) # Recovery BTN

    ### --------------------------- 
    cut_X(scale=(3.0, 10.0, 3.2), y=-28.8, r=True) # Digital Mic
    cut_X(scale=(3.0, 12.8, 3.2), y=-16.0, r=True) # MIPI DSI
    cut_X(scale=(3.0, 10.0, 3.2), y= -2.2, r=True) # MIPI CSI
    cut_X(scale=(3.0, 10.0, 3.2), y= 10.0, r=True) # MIPI CSI


#################################################

def cut_X2(scale, y, r=False):
    x = MAIN_WIDTH / 2 - scale[0]/2 + MAIN_THICKNESS + 0.001
    z = scale[2]/2 - 0.001
    if r:
        x = -x
    base.cut_cube(
        target=bottom,
        scale=scale,
        location=(x, y, -z),
    )

if BOTTOM:
    ### --------------------------- 

    cut_X2(scale=(3.0, 12.2, 2.6), y= -27.0) # SIM
    cut_X2(scale=(3.0, 4.6, 3.8), y= -14.9) # RTC BAT
    cut_X2(scale=(3.0, 11.8, 2.6), y= -0.6) # microSD

# ##################################################
if TOP:
    top.location[0] = 8.1
    top.location[1] = 1.3
    top.location[2] = MAIN_DEPTH1/2
#    top.rotation_euler[1] = math.pi

# ##################################################
if BOTTOM:
    bottom.location[0] = 8.1
    bottom.location[1] = 1.3
#    bottom.location[2] = MAIN_DEPTH2/2-1.5

# base.cut_cube(
#     target=top,
#     scale=(MAIN_WIDTH*1.2, MAIN_HEIGHT*1.2, MAIN_DEPTH1),
#     location=(0, 0, MAIN_THICKNESS+MAIN_DEPTH1/2),
# )
