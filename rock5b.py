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

base.init()

# main -----------------------------------
MAIN_WIDTH = 101.0
MAIN_HEIGHT = 75.0

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


top = create_case(MAIN_DEPTH1)

bottom = create_case(MAIN_DEPTH2)


def punch(obj):
    
    M3 = 1.75

    P_X = -47.0
    P_Y = 33.9

    G_X = 93.15
    G_Y = 49.0
    G_X2 = 58.5

    base.cut_holes(
        target=obj,
        radius=M3,
        depth=MAIN_DEPTH,
        positions=[
            (P_X, P_Y),
            (P_X + G_X, P_Y),
            (P_X, P_Y - G_Y),
            (P_X + G_X, P_Y - G_Y),
            (P_X + G_X2, P_Y),
        ],
    )

    M3 = 1.6

    P_X = -40.6
    P_X2 = 13.3
    P_X3 = 11.6

    P_Y = 18.1
    P_Y2 = -14.9
    P_Y3 = -1.9

    base.cut_holes(
        target=obj,
        radius=M3,
        depth=MAIN_DEPTH,
        positions=[
            (P_X, P_Y),
            (P_X, P_Y2),
            (P_X2, P_Y),
            (P_X2, P_Y2),
            (P_X3, P_Y3),
        ],
    )


top.rotation_euler[0] = math.pi
punch(top)

punch(bottom)

# --------------------------- CPU

base.cut_cube(
    target=top,
    scale=(41.0, 41.0, 34.0),
    location=(
        -23.2,
        7.8,
        0
    ),
)

## --------------------------- GPIO

GIPO_X = 50.7
GIPO_Y = 5.1

base.cut_cube(
    target=top,
    scale=(GIPO_X, GIPO_Y, 17.01),
    location=(
        -17.9,
        33.7,
        0
    ),
)

## --------------------------- GPIO(4pin)

GIPO_X = 5.0
GIPO_Y = 5.1

base.cut_cube(
    target=top,
    scale=(GIPO_X, GIPO_Y, 17.01),
    location=(
        11.8,
        26.75,
        0
    ),
)

## --------------------------- WIFI

WIFI_X = 21.0
WIFI_Y = 21.0

base.cut_cube(
    target=top,
    scale=(WIFI_X, WIFI_Y, 17.01),
    location=(
        31.3,
        8.4,
        0
    ),
)

################################################

top.location[2] = 4.5
bottom.location[2] = -MAIN_DEPTH2/2

################################################


def cube_cut(scale, location):
    base.cut_cube(
        target=top,
        scale=scale,
        location=location,
    )

base.cut_cylinder(
    target=top,
    radius=3.35,
    depth=6.4,
    location=(
        -44.1,
        -37.5,
        4.2
    ),
    rotation=(math.pi / 2, 0, 0),
)


cube_cut(scale=(6.7, 15.0, 4.0),    location=(-44.1, -31.5, 1.95))   # DC
cube_cut(scale=(3.9, 13.2, 9.01),   location=(-35.7, -32.5, 4.495))  # USB-C
cube_cut(scale=(6.3, 22.5, 9.01),   location=(-25.9, -29.5, 4.495))  # HDMI1
cube_cut(scale=(6.3, 22.5, 9.01),   location=(-13.2, -29.5, 4.495))  # HDMI2
cube_cut(scale=(14.0, 16.0, 9.01),  location=(2.4, -31.0, 4.495))    # USB1
cube_cut(scale=(14.0, 16.0, 9.01),  location=(21.1, -31.0, 4.495))   # USB2
cube_cut(scale=(16.5, 19.5, 9.01),  location=(39.5, -29.25, 4.495))  # ETH

################################################


def cube_cut2(scale, location):
    base.cut_cube(
        target=top,
        scale=scale,
        location=location,
    )


cube_cut2(scale=(5.0, 1.5, 5.0), location=(39.7, 38.25, 2.24))  # BUTTON1
cube_cut2(scale=(5.0, 1.5, 5.0), location=(32.8, 38.25, 2.24))  # BUTTON1
cube_cut2(scale=(3.5, 1.5, 3.2), location=(26.8, 38.25, 1.49))  # LED
cube_cut2(scale=(7.0, 1.5, 5.2), location=(18.9, 38.25, 2.49))  # USB-B?

#################################################

#top.rotation_euler[1] = math.pi

#################################################
