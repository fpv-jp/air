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
MAIN_WIDTH = 100.5
MAIN_HEIGHT = 74.6

MAIN_DEPTH1 = 8.0
MAIN_DEPTH2 = 4.5
MAIN_DEPTH = MAIN_DEPTH1 + MAIN_DEPTH2

MAIN_THICKNESS = 1.5

BASE_X = MAIN_WIDTH / 2
BASE_Y = MAIN_HEIGHT / 2

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

#bottom = create_case(MAIN_DEPTH2)


def punch(obj):
    
    M3 = 1.75

    P_X = -BASE_X + 3.5
    P_Y = BASE_Y - 3.6

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

    P_X = -BASE_X + 8.3 + M3
    P_X2 = -BASE_X + 62.2 + M3
    P_X3 = BASE_X - 37.3 - M3

    P_Y = BASE_Y - 17.8 - M3
    P_Y2 = BASE_Y - 50.8 - M3
    P_Y3 = BASE_Y - 37.8 - M3

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

#punch(bottom)

# --------------------------- CPU

base.cut_cube(
    target=top,
    scale=(41.0, 41.0, MAIN_DEPTH + MAIN_THICKNESS),
    location=(-BASE_X + 27.3, -BASE_Y + 39.9, 0),
)

## --------------------------- GPIO

GIPO_X = 50.7
GIPO_Y = 5.1

base.cut_cube(
    target=top,
    scale=(GIPO_X, GIPO_Y, MAIN_DEPTH),
    location=(-BASE_X + 32.6, BASE_Y - 3.8, 0),
)

## --------------------------- GPIO(4pin)

GIPO_X = 5.0
GIPO_Y = 5.1

base.cut_cube(
    target=top,
    scale=(GIPO_X, GIPO_Y, MAIN_DEPTH),
    location=(BASE_X - 36.2 - GIPO_X / 2, BASE_Y - 8.2 - GIPO_Y / 2, 0),
)

## --------------------------- WIFI

WIFI_X = 21.0
WIFI_Y = 21.0

base.cut_cube(
    target=top,
    scale=(WIFI_X, WIFI_Y, MAIN_DEPTH + MAIN_THICKNESS),
    location=(BASE_X - 8.2 - WIFI_X / 2, BASE_Y - 18.1 - WIFI_Y / 2, 0),
)

################################################

top.location[2] = MAIN_DEPTH1/2
#bottom.location[2] = -MAIN_DEPTH2/2

################################################


def cube_cut(scale, pos):
    z = (scale[2] - MAIN_DEPTH - MAIN_THICKNESS) / 2
    base.cut_cube(
        target=top,
        scale=scale,
        location=(pos, -BASE_Y + scale[1] / 2 - 2, z),
    )


H = 15

GAP = 0.5

base.cut_cylinder(
    target=top,
    radius=3.15 + GAP / 2,
    depth=5,
    location=(-BASE_X + 6.4, -BASE_Y + 5 / 2 - 2, 2),
    rotation=(math.pi / 2, 0, 0),
)


cube_cut(scale=(6.3 + GAP, H, 9.0), pos=-BASE_X + 6.4)  # DC
cube_cut(scale=(3.4 + GAP, 13.0, H), pos=-BASE_X + 14.8)  # USB-C
cube_cut(scale=(5.6 + GAP, 19.0, H), pos=-BASE_X + 24.6)  # HDMI1
cube_cut(scale=(5.6 + GAP, 19.0, H), pos=-BASE_X + 37.3)  # HDMI2
cube_cut(scale=(13.0 + GAP, 16.0, H), pos=-BASE_X + 52.9)  # USB1
cube_cut(scale=(13.0 + GAP, 16.0, H), pos=-BASE_X + 71.6)  # USB2
cube_cut(scale=(16.0 + GAP, 19.5, H), pos=-BASE_X + 90.0)  # ETH

################################################


def cube_cut2(scale, pos):
    base.cut_cube(
        target=top,
        scale=scale,
        location=(pos, BASE_Y - scale[1] / 2 + 2, 0),
    )


cube_cut2(scale=(4.5 + GAP, 3.5, 7.0), pos=BASE_X - 10.8)  # BUTTON1
cube_cut2(scale=(4.5 + GAP, 3.5, 7.0), pos=BASE_X - 17.7)  # BUTTON1
cube_cut2(scale=(3.0 + GAP, 3.5, 4.0), pos=BASE_X - 23.7)  # LED
cube_cut2(scale=(6.5 + GAP, 3.5, 8.0), pos=BASE_X - 31.6)  # USB-B?

#top.rotation_euler[0] = math.radians(180)

################################################


#base.cut_cube(
#    target=top,
#        scale=(
#            MAIN_WIDTH + MAIN_THICKNESS * 3,
#            MAIN_HEIGHT + MAIN_THICKNESS * 3,
#            MAIN_DEPTH1,
#        ),
#    location=(0, 0, MAIN_DEPTH1/2-MAIN_THICKNESS),
#)

