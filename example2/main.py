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

_test5 = bpy.data.objects.get("test5")
if _test5:
    _test5.hide_set(True)

base.init()

if _test5:
    _test5.hide_set(False)

adjustment = 1.47  # アームの長さ/モータ位置を調整する倍率

DRONE_SIZE = 6.0 * 25.4 * adjustment  # 6inch

MOTOR_PITCH = DRONE_SIZE / 2  # モータとボディのピッチ/アームの長さ

ARM_hickness = 12.0  # アームの幅
ARM_position = 55.0  # ボディに対してアームを取り付ける位置

MOTOR_radius = 38.2 / 2  # モータの半径

BODY_radius = 30.0  # ボディの半径
BODY_height = BODY_radius * 12  # ボディの高さ

WALL_hickness = 1.5  # 基本とする壁の厚み

#BUILD_TOP = True
#BUILD_TOP = False

#BUILD_MIDDLE = True
#BUILD_MIDDLE = False

#BUILD_BOTTOM = True
#BUILD_BOTTOM = False


# -------------------------------------------------------
# モータ
# -------------------------------------------------------
def create_motor(sharpen):

    # --- スピンナー(モータ直径より少し小さくする) ---
    motor = base.create_cylinder(
        radius=MOTOR_radius * 0.9 - sharpen,
        depth=MOTOR_radius * 8,
        location=(0.0, 0.0, sharpen),
        vertices=64,
    )

    # テーバをつける
    base.taper(motor, segments=64, curve="tear", power=0.75)
    return motor


# -------------------------------------------------------
# アーム
# -------------------------------------------------------
def create_arm(sharpen):

    sharpen2 = sharpen * 2

    # --- アーム 中央 ---
    arm = base.create_cube(
        scale=(
            ARM_hickness - sharpen2,
            DRONE_SIZE / 1.75,
            ARM_hickness * 3 - sharpen2,
        ),
        location=(0.0, DRONE_SIZE / 4, 0.0),
    )

    # --- アーム 上部 ---
    arm_top = base.create_tear_beam(
        depth=DRONE_SIZE / 1.75,
        width=ARM_hickness - sharpen2,
        height=ARM_hickness * 3 - sharpen2,
        power=0.75,
        location=(0.0, DRONE_SIZE / 4, -ARM_hickness * 1.2),
    )

    # --- アーム 中央 上部 結合し傾けて少し上にずらす ---
    base.modifier_apply(obj=arm_top, target=arm, operation="UNION")
    arm.rotation_euler = (math.pi / 8, 0, 0)
    arm.location = (0.0, 0.0, -ARM_hickness * 1.9)

    # --- 下を少しカット ---
    base.cut_cube(
        target=arm,
        scale=(ARM_hickness, DRONE_SIZE, ARM_hickness * 4),
        location=(0.0, DRONE_SIZE / 4, ARM_hickness * 2.21),
    )

    # --- アーム 下部 ---
    arm_bottom = base.create_tear_beam(
        depth=DRONE_SIZE / 2,
        width=ARM_hickness - sharpen2,
        height=ARM_hickness * 3 - sharpen2,
        power=0.75,
        location=(0.0, DRONE_SIZE / 4, 5.5),
    )

    # --- アーム 中央 上部 と 下部 を 結合 ---
    base.modifier_apply(obj=arm_bottom, target=arm, operation="UNION")
    
    if sharpen2 == 0:
        base.cut_cube(
            target=arm,
            scale=(100, 100, 150),
            location=(0.0, -45.0, 0.0),
        )
        base.cut_cube(
            target=arm,
            scale=(100, 100, 100),
            location=(0.0, 47.5 + DRONE_SIZE/2, 0.0),
        )

    return arm

# -------------------------------------------------------
# アーム + モータ
# -------------------------------------------------------
def create_motor_arm():

    # --- アーム
    arm = create_arm(0)
    
    # --- アーム(中をくり抜く) ---
    arm_inner = create_arm(WALL_hickness)
    base.modifier_apply(obj=arm_inner, target=arm, operation="DIFFERENCE")

    location = (0, MOTOR_PITCH, 16.0)  # アーム に対して モータ を取り付ける位置

    # --- モータ ---
    motor = create_motor(0)
    motor.location = location

    base.cut_cylinder(
        target=arm,
        radius=MOTOR_radius - 5,
        depth=100.0,
        location=(0.0, MOTOR_PITCH, 0.0),
    )

    # --- アーム と モータ を結合 ---
    base.modifier_apply(obj=motor, target=arm, operation="UNION")

    # --- モータの 中をくり抜く ---
    motor_inner = create_motor(WALL_hickness)
    motor_inner.location = location
    base.modifier_apply(obj=motor_inner, target=arm, operation="DIFFERENCE")

    # --- モータ の下部をカット ---
    base.cut_cylinder(
        target=arm,
        radius=MOTOR_radius + WALL_hickness,
        depth=100.0,
        location=(0.0, MOTOR_PITCH, 50.0 - 4.85),
        vertices=64,
    )

    return arm

# -------------------------------------------------------
# ボディ
# -------------------------------------------------------

def create_body(sharpen):
    
    BODY_radius_center = BODY_radius - .1 - sharpen
    BODY_radius_top = BODY_radius + .1 - sharpen
    BODY_radius_bottom = BODY_radius - sharpen
    
    # --- ボディ 中央 ---
    body = base.create_cylinder(
        radius=BODY_radius_center, depth=BODY_height / 2.5, location=(0.0, 0.0, 11.0), vertices=64
    )

    # --- ボディ 上部 ---
    body_top = base.create_tear_body(
        radius=BODY_radius_top, depth=BODY_height, power=0.66, smooth=False
    )
    base.cut_cylinder(target=body_top, radius=BODY_radius_top, depth=300.0, location=(0.0, 0.0, 150.0))
    body_top.location = (0.0, 0.0, sharpen)

    # --- ボディ 下部 ---
    body_bottom = base.create_tear_body(
        radius=BODY_radius_bottom, depth=BODY_height, power=0.66, peak=0.75, smooth=False
    )
    base.cut_cylinder(target=body_bottom, radius=BODY_radius_bottom, depth=300.0, location=(0.0, 0.0, -150.0))
    body_bottom.location = (0.0, 0.0, -sharpen)

    # --- ボディ を結合 ---
    base.modifier_apply(obj=body_top, target=body, operation="UNION")
    base.modifier_apply(obj=body_bottom, target=body, operation="UNION")
    return body


## --------------------------------------------
## --- アッセンブリ ---------------------------
## --------------------------------------------

# アーム + モータ
motor_arm1 = create_motor_arm()
motor_arm1.location[2] = ARM_position  # ボディに対して取り付ける位置を調整

# 他の アーム + モータ をコピー
motor_arm2 = base.copy(motor_arm1, rotation=(math.pi / 8, 0, math.pi))
motor_arm3 = base.copy(motor_arm1, rotation=(math.pi / 8, 0, math.pi / 2))
motor_arm4 = base.copy(motor_arm1, rotation=(math.pi / 8, 0, -math.pi / 2))

# --- ボディ ---
body = create_body(0)

# --- ボディ の下部をカット ---
base.cut_cylinder(
    target=body,
    radius=BODY_radius,
    depth=100.0,
    location=(0.0, 0.0, 190.0),
)

# --- ボディ に腕を結合 ---
base.modifier_apply(obj=motor_arm1, target=body, operation="UNION")
base.modifier_apply(obj=motor_arm2, target=body, operation="UNION")
base.modifier_apply(obj=motor_arm3, target=body, operation="UNION")
base.modifier_apply(obj=motor_arm4, target=body, operation="UNION")

# --- ボディ を中空化 ---
body_inner = create_body(WALL_hickness)
base.modifier_apply(obj=body_inner, target=body, operation="DIFFERENCE")
