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

_main = bpy.data.objects.get("main_fixed")
if _main:
    _main.hide_set(True)

base.init()

if _main:
    _main.hide_set(False)

adjustment = 1.47  # アームの長さ/モータ位置を調整する倍率

DRONE_SIZE = 6.0 * 25.4 * adjustment  # 6inch

MOTOR_PITCH = DRONE_SIZE / 2  # モータとボディのピッチ/アームの長さ

ARM_width = 12.0  # アームの幅
ARM_position = 55.0  # ボディに対してアームを取り付ける位置

MOTOR_radius = 38.2 / 2  # モータの半径

BODY_radius = 30.0  # ボディの半径
BODY_height = BODY_radius * 12  # ボディの高さ

WALL_hickness = 1.5  # 基本とする壁の厚み

BUILD_TOP = True
BUILD_TOP = False

BUILD_MIDDLE = True
BUILD_MIDDLE = False

BUILD_BOTTOM = True
BUILD_BOTTOM = False

H = 280
R = 140

L_TOP = 43
L_BOTTOM = -73

def screw(pos):
    for i, (z) in enumerate([(math.pi / 4),(-math.pi / 4)]):
        for i, (p) in enumerate([(pos+6),(pos-6)]):
            base.cut_cylinder(
                target=_main,
                radius=1.5,
                depth=BODY_radius*3,
                location=(0.0, 0.0, p),
                rotation=(math.pi / 2, 0, z),
            )

screw(L_TOP)
screw(L_BOTTOM)

# -------------------------------------------------------
# BUILD_TOP
# -------------------------------------------------------
if BUILD_TOP:
    base.cut_cylinder(
        target=_main, radius=R, depth=H,
        location=(0.0, 0.0, -H / 2 + L_TOP),
    )
    base.cut_cylinder(
        target=_main, 
        radius=7.5, depth=12,
        rotation=(-math.pi / 5, 0, 0),
        location=(0.0, 12.0, 160.0),
    )

# -------------------------------------------------------
# BUILD_MIDDLE
# -------------------------------------------------------
if BUILD_MIDDLE:
    base.cut_cylinder(
        target=_main, radius=R, depth=H,
        location=(0.0, 0.0, H / 2 + L_TOP),
    )
    base.cut_cylinder(
        target=_main, radius=R, depth=H,
        location=(0.0, 0.0, -H / 2 + L_BOTTOM),
    )
    # そのままだと3Dプリンタのサイズを超えるので調整
    _main.rotation_euler = (0, 0, math.pi / 4)

# -------------------------------------------------------
# BUILD_BOTTOM
# -------------------------------------------------------
if BUILD_BOTTOM:
    base.cut_cylinder(
        target=_main, radius=R, depth=H,
        location=(0.0, 0.0, H / 2 + L_BOTTOM),
    )
    
    # アームのボディが重なる部分をカット
    location = (0.0, 0.0, -21.0 - ARM_position)
    x = ARM_width + 0.1
    y = DRONE_SIZE
    base.cut_cube(target=_main, scale=(x, y, 6.1), location=(location))
    base.cut_cube(target=_main, scale=(y, x, 6.1), location=(location))

    # モータとESCのワイヤを通す穴
    for i, (x, y) in enumerate([(math.pi / 2, 0), (0, math.pi / 2)]):
        base.cut_cylinder(
            target=_main,
            radius=3.5,
            depth=DRONE_SIZE,
            location=(0.0, 0.0, -28.5 - ARM_position),
            rotation=(x, y, 0),
        )
    # そのままだと3Dプリンタのサイズを超えるので調整
    _main.rotation_euler = (0, 0, math.pi / 4)
