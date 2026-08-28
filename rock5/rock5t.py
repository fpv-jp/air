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

TOP = True
BOTTOM = True
    
# main -----------------------------------
#MAIN_WIDTH = 101.0
#MAIN_HEIGHT = 75.0
MAIN_WIDTH = 111.2
MAIN_HEIGHT = 82.4

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

BASE_X = MAIN_WIDTH / 2
BASE_Y = MAIN_HEIGHT / 2
def punch(obj):
    base.cut_holes(
        target=obj,
        radius=1.35,
        depth=MAIN_DEPTH,
        positions=[
            (BASE_X - 3.56, -BASE_Y + 3.635),
            (-BASE_X + 48.591, -BASE_Y + 3.635),
            (-BASE_X + 3.462, -BASE_Y + 3.635),
            (-BASE_X + 3.344, BASE_Y - 21.7),
            (BASE_X - 3.66, BASE_Y - 29.705),
        ],
    )
    base.cut_holes(
        target=obj,
        radius=1.6,
        depth=MAIN_DEPTH,
        positions=[
            (-BASE_X + 22.48, BASE_Y - 39.18),
            (-BASE_X + 73.88, BASE_Y - 59.18),
        ],
    )

if TOP:
    top.rotation_euler[0] = math.pi
    punch(top)

    ### --------------------------- CPU
    base.cut_cube(
        target=top,
        scale=(41.0, 41.0, MAIN_DEPTH),
        location=(
            -23.2,
            7.8,
            0
        ),
    )

    ### --------------------------- GPIO
    base.cut_cube(
        target=top,
        scale=(50.7, 5.1, MAIN_DEPTH),
        location=(
            -17.9,
            33.7,
            0
        ),
    )

    ### --------------------------- WIFI
    base.cut_cube(
        target=top,
        scale=(21.0, 21.0, MAIN_DEPTH),
        location=(
            31.3,
            8.4,
            0
        ),
    )


if BOTTOM:
    punch(bottom)

    ### --------------------------- AI
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


#def cube_cut(scale, location):
#    base.cut_cube(
#        target=top,
#        scale=scale,
#        location=location,
#    )

#base.cut_cylinder(
#    target=top,
#    radius=3.35,
#    depth=6.4,
#    location=(
#        -44.1,
#        -37.5,
#        4.2
#    ),
#    rotation=(math.pi / 2, 0, 0),
#)


#cube_cut(scale=(6.7, 15.0, 4.0),    location=(-44.1, -31.5, 1.95))   # DC
#cube_cut(scale=(3.9, 13.2, 9.01),   location=(-35.7, -32.5, 4.495))  # USB-C
#cube_cut(scale=(6.3, 22.5, 9.01),   location=(-25.9, -29.5, 4.495))  # HDMI1
#cube_cut(scale=(6.3, 22.5, 9.01),   location=(-13.2, -29.5, 4.495))  # HDMI2
#cube_cut(scale=(14.0, 16.0, 9.01),  location=(2.4, -31.0, 4.495))    # USB1
#cube_cut(scale=(14.0, 16.0, 9.01),  location=(21.1, -31.0, 4.495))   # USB2
#cube_cut(scale=(16.5, 19.5, 9.01),  location=(39.5, -29.25, 4.495))  # ETH

#################################################


#def cube_cut2(scale, location):
#    base.cut_cube(
#        target=top,
#        scale=scale,
#        location=location,
#    )


#cube_cut2(scale=(5.0, 1.5, 5.0), location=(39.7, 38.25, 2.24))  # BUTTON1
#cube_cut2(scale=(5.0, 1.5, 5.0), location=(32.8, 38.25, 2.24))  # BUTTON1
#cube_cut2(scale=(3.5, 1.5, 3.2), location=(26.8, 38.25, 1.49))  # LED
#cube_cut2(scale=(7.0, 1.5, 5.2), location=(18.9, 38.25, 2.49))  # USB-B?

##################################################

##top.rotation_euler[1] = math.pi

##################################################
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

TOP = True
BOTTOM = True
    
# main -----------------------------------
MAIN_WIDTH = 111.2
MAIN_HEIGHT = 82.4

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

BASE_X = MAIN_WIDTH / 2
BASE_Y = MAIN_HEIGHT / 2
def punch(obj):
    base.cut_holes(
        target=obj,
        radius=1.35,
        depth=MAIN_DEPTH,
        positions=[
            (BASE_X - 3.56, -BASE_Y + 3.635),
            (-BASE_X + 48.591, -BASE_Y + 3.635),
            (-BASE_X + 3.462, -BASE_Y + 3.635),
            (-BASE_X + 3.344, BASE_Y - 21.7),
            (BASE_X - 3.66, BASE_Y - 29.705),
        ],
    )
    base.cut_holes(
        target=obj,
        radius=1.6,
        depth=MAIN_DEPTH,
        positions=[
            (-BASE_X + 22.48, BASE_Y - 39.18),
            (-BASE_X + 73.88, BASE_Y - 59.18),
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
            -23.2,
            -3.8,
            0
        ),
    )

    ### --------------------------- M.2
    base.cut_cube(
        target=top,
        scale=(23.0, 46.0, MAIN_DEPTH),
        location=(
            38.2,
            -3.8,
            0
        ),
    )

    ### --------------------------- GPIO
    base.cut_cube(
        target=top,
        scale=(50.7, 5.1, MAIN_DEPTH),
        location=(
            20.9,
            -33.7,
            0
        ),
    )

    ### --------------------------- WIFI sink
    base.cut_cube(
        target=top,
        scale=(21.0, 21.0, MAIN_DEPTH),
        location=(
            -31.3,
            -28.4,
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
    y = BASE_Y - scale[1]/2 + MAIN_THICKNESS + 0.001
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
cut_Y(scale=(10.7, 14.1, H), x= BASE_X - 5.968)  # DC
cut_Y(scale=(13.5, 18.2, H), x= BASE_X - 20.44)  # USB1
cut_Y(scale=(13.5, 18.2, H), x= BASE_X - 37.38)  # USB2
cut_Y(scale=( 6.2, 22.7, H), x=-BASE_X + 56.16)  # HDMI1
cut_Y(scale=( 6.2, 22.7, H), x=-BASE_X + 42.31)  # HDMI2
cut_Y(scale=(16.9, 21.6, H), x=-BASE_X + 28.115) # LAN1
cut_Y(scale=(16.9, 21.6, H), x=-BASE_X + 9.091)  # LAN2

### --------------------------- 

cut_Y(scale=(2.72, 2.626, 3.5), x=-BASE_X + 10.64, r=True)
cut_Y(scale=(6.50, 2.626, 5.2), x=-BASE_X + 19.35, r=True)
cut_Y(scale=(9.21, 2.626, 3.0), x=-BASE_X + (28.67 + 9.21 / 2), r=True)
cut_Y(scale=(2.72, 2.626, 1.5), x=-BASE_X + 42.647, r=True)


#################################################

def cut_X(scale, y, r=False):
    x = BASE_X - scale[0]/2  + MAIN_THICKNESS + 0.001
    z = scale[2]/2 - 0.001
    if r:
        x = -x
    base.cut_cube(
        target=top,
        scale=scale,
        location=(x, y, z),
    )

### --------------------------- 

#cut_X(scale=(6.7, 15.0, 4.0), y=3)
cube_cut2(scale=(8.52, 15.687, 5.6), posx=BASE_X - 1.59, posy=BASE_Y - (33.784 + 15.687 / 2))
cube_cut2(scale=(2.72, 2.583, 3.5), posx=BASE_X, posy=BASE_Y - 20.946)
cube_cut2(scale=(2.72, 2.626, 3.5), posx=BASE_X, posy=BASE_Y - 55.171)


### --------------------------- 

#cut_X(scale=(6.7, 15.0, 4.0), y=3.0, r=True)


##################################################

##top.rotation_euler[1] = math.pi

##################################################
