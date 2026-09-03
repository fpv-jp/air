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
M4 = 2.0
M8 = 4.0

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
    thickness=MAIN_THICKNESS
)
base.cut_cube(
    target=main,
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
)

X = (MAIN_WIDTH - M4) / 2
Y = MAIN_HEIGHT / 2 - 17.0 - M4 / 2 - MAIN_THICKNESS
holes = [(X - 2.2 - MAIN_THICKNESS, Y), (-X + 10.0 + MAIN_THICKNESS / 2, Y)]
for i, (x, y) in enumerate(holes):
    base.add_ring(
        target=main,
        outer_radius=M8,
        inner_radius=M4,
        depth=MAIN_DEPTH + MAIN_THICKNESS * 2,
        location=(x, y, 0),
    )

H = 2.5
base.cut_cube(
    target=main,
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH-H),
    location=(0, 0, H/2),
)

# TOP cut >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

main.location = (0, 0, -MAIN_DEPTH/2 - MAIN_THICKNESS)

# CPU
x = 29.0
y = 29.0
location = ((MAIN_WIDTH - x) / 2 - 34.3, -(MAIN_HEIGHT - y) / 2 + 2.2, 0)
base.cut_cube(target=main, scale=(x, y, 10), location=location, rotation=(0, 0, math.radians(1.5)))

# SATA PWR
x = 9.5
y = 16.5
location = (-(MAIN_WIDTH - x) / 2, -(MAIN_HEIGHT - y) / 2 + 6.2, 0)
base.cut_cube(target=main, scale=(x, y, 10), location=location)

# SATA DATA
x = 7.5
y = 14.8
location = ((MAIN_WIDTH - x) / 2 - 1.4, -(MAIN_HEIGHT - y) / 2 + 3.6, 0)
base.cut_cube(target=main, scale=(x, y, 10), location=location)

# BATTERY
x = 23.5
y = 6.2
location = ((MAIN_WIDTH - x) / 2 - 10.5, (MAIN_HEIGHT - y) / 2 - 10.15, 0)
base.cut_cube(target=main, scale=(x, y, 10), location=location)

# TOP cut <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

y = 20.25
pos_z = 18.85

main.location = (MAIN_WIDTH / 2, -MAIN_HEIGHT / 2, -H-MAIN_THICKNESS)
pos = [
#   (9.2, 1.8, 11.1),    # DC
#    (15.0, 15.6, 16.2),  # USB
    (16.4, 34.2, 12.6),  # ETH
]
for i, (x, p, z) in enumerate(pos):
    base.cut_cube(
        target=main,
        scale=(x, y, z),
        location=(x / 2 + p, -y / 2 + MAIN_THICKNESS, (z - pos_z) / 2+0.5),
    )
pos = [
#   (9.2, 1.8, 11.1),    # DC
    (15.0, 15.6, 16.2),  # USB
#    (16.4, 34.2, 12.6),  # ETH
]
for i, (x, p, z) in enumerate(pos):
    base.cut_cube(
        target=main,
        scale=(x, y, z),
        location=(x / 2 + p, -y / 2 + MAIN_THICKNESS, (z - pos_z) / 2+0.75),
    )
# DC
base.cut_cylinder(
    target=main,
    radius=4.2,
    depth=MAIN_THICKNESS*3,
    location=(4.2+3.0, 0, -1.7),
    rotation=(math.pi / 2, 0, 0),
)

main.location = (-MAIN_WIDTH / 2, -MAIN_HEIGHT / 2, -H-MAIN_THICKNESS)
pos = [
#    (15.2, 46.5, 6.2),  # HDMI
    (30.9, 9.7, 12.7),  # DVI
#   (5.4, 1.7, 5.7),    # AUX
]
for i, (x, p, z) in enumerate(pos):
    base.cut_cube(
        target=main,
        scale=(x, y, z),
        location=(-x / 2 - p, y / 2, (z - pos_z) / 2),
    )
pos = [
    (15.2, 46.5, 6.2),  # HDMI
#    (30.9, 9.7, 12.7),  # DVI
#   (5.4, 1.7, 5.7),    # AUX
]
for i, (x, p, z) in enumerate(pos):
    base.cut_cube(
        target=main,
        scale=(x, y, z),
        location=(-x / 2 - p, y / 2, (z - pos_z) / 2+ 0.5),
    )
    
# AUX
base.cut_cylinder(
    target=main,
    radius=2.7,
    depth=MAIN_THICKNESS*3,
    location=(-4.3, 0, -6),
    rotation=(math.pi / 2, 0, 0),
)

main.location = (0, 0, 0)

# ===============================

#scale=(
#    MAIN_WIDTH + MAIN_THICKNESS * 3,
#    MAIN_HEIGHT + MAIN_THICKNESS * 3,
#    MAIN_DEPTH_TOP+MAIN_THICKNESS,
#)

#location=(
#    0, 
#    0, 
#    (MAIN_DEPTH-MAIN_DEPTH_TOP+MAIN_THICKNESS)/2,
#)

#base.cut_cube(target=main, scale=scale, location=location)

# ===============================

#scale=(
#    MAIN_WIDTH + MAIN_THICKNESS * 3,
#    MAIN_HEIGHT + MAIN_THICKNESS * 3,
#    MAIN_DEPTH_BOTTOM+MAIN_THICKNESS,
#)

#location=(
#    0, 
#    0, 
#    (-MAIN_DEPTH+MAIN_DEPTH_BOTTOM-MAIN_THICKNESS)/2,
#)

#base.cut_cube(target=main, scale=scale, location=location)
#main.rotation_euler[1] = math.pi
