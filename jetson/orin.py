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

bpy.data.objects.get("000_ARVALA_TLA_ASM").hide_set(True)
base.init()
bpy.data.objects.get("000_ARVALA_TLA_ASM").hide_set(False)
#bpy.data.objects.get("000_ARVALA_TLA_ASM").location=(-46.0, -22.6, -7.8)
bpy.data.objects.get("000_ARVALA_TLA_ASM").location=(-46.0, -22.6, -1.6)

MAIN_WIDTH = 100.0
MAIN_HEIGHT = 79.0
MAIN_DEPTH = 12.0

MAIN_THICKNESS = 2.0
MAIN_GAP = 0.15

main = base.create_cube(
    scale=(MAIN_WIDTH + MAIN_THICKNESS, MAIN_HEIGHT + MAIN_THICKNESS, MAIN_DEPTH),
)
base.cut_corners(
    target=main,
    width=MAIN_WIDTH,
    height=MAIN_HEIGHT,
    depth=MAIN_DEPTH - MAIN_THICKNESS/2,
    thickness=MAIN_THICKNESS/2,
)
base.cut_cube(
    target=main,
    scale=(MAIN_WIDTH + MAIN_GAP, MAIN_HEIGHT + MAIN_GAP, MAIN_DEPTH),
    location=(0, 0, -MAIN_THICKNESS/2),
)

M2 = 1.25

x = 43
y = 29

x2 = -3
y2 = 7

base.cut_holes(
    target=main,
    radius=M2,
    depth=MAIN_DEPTH + MAIN_THICKNESS,
    positions=[
        (x + x2, y + y2),
        (x + x2, -y + y2),
        (-x + x2, y + y2),
        (-x + x2, -y + y2),
    ],
)

## ---------------------------------------

BASE_X = MAIN_WIDTH / 2
BASE_Y = MAIN_HEIGHT / 2


def cube_cut(scale, pos):
    y = -BASE_Y + scale[1] / 2 - 2
    z = (scale[2] - MAIN_DEPTH - MAIN_THICKNESS) / 2
    base.cut_cube(
        target=main,
        scale=scale,
        location=(pos, y, z),
    )


H = 5

cube_cut(scale=(9.5, H, 12.2), pos=-BASE_X + 6)  # DC
cube_cut(scale=(18.7, H, 7.9), pos=-BASE_X + 22.8)  # DP
cube_cut(scale=(14.4, 18.7, 18.5), pos=-BASE_X + 42.6)  # USB1
cube_cut(scale=(14.4, 18.7, 18.5), pos=-BASE_X + 59.6)  # USB2
cube_cut(scale=(16.5, 22.5, 15.1), pos=-BASE_X + 76.9)  # LAN
cube_cut(scale=(9.3, H, 4.7), pos=-BASE_X + 91.9)  # USB-C

## ---------------------------------------

def cube_cut2(scale, posx, posy):
    z = (scale[2] - MAIN_DEPTH - MAIN_THICKNESS) / 2
    base.cut_cube(
        target=main,
        scale=scale,
        location=(posx, posy, z),
    )


cube_cut2(scale=(59.0, 40.0, 25.3), posx=-BASE_X + 48, posy=BASE_Y - 20.0)
cube_cut2(scale=(5.8, 51.0, 25.3), posx=BASE_X - 4.2, posy=BASE_Y - 32.5)
cube_cut2(scale=(6.8, 3.0, 25.3), posx=BASE_X - 19.2, posy=BASE_Y - 8.5)

## ---------------------------------------
main.location[2] = MAIN_DEPTH/2
#main.rotation_euler = (math.radians(180), 0, 0)
