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
MAIN_THICKNESS = 1.5
M4_RADIUS = 2.0
M8_RADIUS = 4.0

MAIN_WIDTH = 119.2
MAIN_HEIGHT = 47.2
MAIN_DEPTH_TOP = 8.3
MAIN_DEPTH_BOTTOM = 9.7
MAIN_DEPTH = MAIN_DEPTH_TOP + MAIN_DEPTH_BOTTOM

main = base.create_cube(
    scale=(
        MAIN_WIDTH + MAIN_THICKNESS * 2,
        MAIN_HEIGHT + MAIN_THICKNESS * 2,
        MAIN_DEPTH + MAIN_THICKNESS * 2,
    ),
)
base.cut_corners(
    target=main,
    width=MAIN_WIDTH,
    height=MAIN_HEIGHT,
    depth=MAIN_DEPTH + MAIN_THICKNESS,
    thickness=MAIN_THICKNESS,
)
base.cut_cube(
    target=main,
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
)

RING_POSITIONS = [(54.9, 4.1), (-47.9, 4.1)]
for x, y in RING_POSITIONS:
    base.add_ring(
        target=main,
        outer_radius=M8_RADIUS,
        inner_radius=M4_RADIUS,
        depth=MAIN_DEPTH + MAIN_THICKNESS * 2,
        location=(x, y, 0),
    )

FLOOR_THICKNESS = 2.5
base.cut_cube(
    target=main,
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH - FLOOR_THICKNESS),
    location=(0, 0, FLOOR_THICKNESS / 2),
)

# TOP cut >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

main.location = (0, 0, -MAIN_DEPTH / 2 - MAIN_THICKNESS)

# CPU
base.cut_cube(
    target=main,
    scale=(29.0, 29.0, 10.0),
    location=(10.8, -6.9, 0),
    rotation=(0, 0, math.radians(1.5)),
)

# SATA PWR
base.cut_cube(
    target=main,
    scale=(9.5, 16.5, 10.0),
    location=(-54.9, -9.2, 0),
)

# SATA DATA
base.cut_cube(
    target=main,
    scale=(7.5, 14.8, 10.0),
    location=(54.5, -12.6, 0),
)

# BATTERY
base.cut_cube(
    target=main,
    scale=(23.5, 6.2, 10.0),
    location=(37.4, 10.4, 0),
)

# TOP cut <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

SIDE_CUT_DEPTH = 20.3

main.location = (59.6, -23.6, -FLOOR_THICKNESS - MAIN_THICKNESS)

# ETH
base.cut_cube(
    target=main,
    scale=(16.4, SIDE_CUT_DEPTH, 12.6),
    location=(42.4, -8.6, -2.6),
)

# USB
base.cut_cube(
    target=main,
    scale=(15.0, SIDE_CUT_DEPTH, 16.2),
    location=(23.1, -8.6, -0.6),
)

# DC
base.cut_cylinder(
    target=main,
    radius=4.2,
    depth=MAIN_THICKNESS * 3,
    location=(7.2, 0, -2.0),
    rotation=(math.pi / 2, 0, 0),
)

main.location = (-59.6, -23.6, -FLOOR_THICKNESS - MAIN_THICKNESS)

# DVI
base.cut_cube(
    target=main,
    scale=(30.9, SIDE_CUT_DEPTH, 12.7),
    location=(-25.2, 10.1, -3.1),
)

# HDMI
base.cut_cube(
    target=main,
    scale=(15.2, SIDE_CUT_DEPTH, 6.2),
    location=(-54.1, 10.1, -5.8),
)

# AUX
base.cut_cylinder(
    target=main,
    radius=2.7,
    depth=MAIN_THICKNESS * 3,
    location=(-4.3, 0, -6.0),
    rotation=(math.pi / 2, 0, 0),
)

main.location = (0, 0, 0)

# ===============================

DEPTH = MAIN_DEPTH_TOP - MAIN_DEPTH_BOTTOM + .5

# ===============================

#scale=(
#    MAIN_WIDTH + MAIN_THICKNESS * 3,
#    MAIN_HEIGHT + MAIN_THICKNESS * 3,
#    MAIN_DEPTH,
#)

#location=(
#    0, 
#    0, 
#    MAIN_DEPTH/2-DEPTH,
#)

#base.cut_cube(target=main, scale=scale, location=location)

# ===============================

#scale=(
#    MAIN_WIDTH + MAIN_THICKNESS * 3,
#    MAIN_HEIGHT + MAIN_THICKNESS * 3,
#    MAIN_DEPTH,
#)

#location=(
#    0, 
#    0, 
#    -MAIN_DEPTH/2-DEPTH,
#)

#base.cut_cube(target=main, scale=scale, location=location)
#main.rotation_euler[0] = math.pi
