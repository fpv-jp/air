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

#_Airframe_TOP = bpy.data.objects.get("Airframe_TOP")
#_Airframe_MIDDLE = bpy.data.objects.get("Airframe_MIDDLE")
#_Airframe_BOTTOM = bpy.data.objects.get("Airframe_BOTTOM")

#if _Airframe_TOP:
#    _Airframe_TOP.hide_set(True)
#if _Airframe_MIDDLE:
#    _Airframe_MIDDLE.hide_set(True)
#if _Airframe_BOTTOM:
#    _Airframe_BOTTOM.hide_set(True)

base.init()

#if _Airframe_TOP:
#    _Airframe_TOP.hide_set(False)
#    _Airframe_TOP.rotation_euler[2] = math.pi / 4
#    base.cut_cube(target=_Airframe_TOP, scale=(500, 500, 500), location=(0.0, -250.0, 0.0))
#    _Airframe_TOP.rotation_euler[2] = 0
#if _Airframe_MIDDLE:
#    _Airframe_MIDDLE.hide_set(False)
#    _Airframe_MIDDLE.rotation_euler[2] = math.pi / 4
#    base.cut_cube(target=_Airframe_MIDDLE, scale=(500, 500, 500), location=(0.0, -250.0, 0.0))
#    _Airframe_MIDDLE.rotation_euler[2] = 0
#if _Airframe_BOTTOM:
#    _Airframe_BOTTOM.hide_set(False)
#    _Airframe_BOTTOM.rotation_euler[2] = math.pi / 4
#    base.cut_cube(target=_Airframe_BOTTOM, scale=(500, 500, 500), location=(0.0, -250.0, 0.0))
#    _Airframe_BOTTOM.rotation_euler[2] = 0


# ネジ(φ)
M3 = 3.2
M5 = 5.2

PROP_INCH = 6 * 25.4  # プロペラ(6inch)

adjustment = 1.47  # アームの長さ/モータ位置を調整する倍率

ARM_length = PROP_INCH / 2 * adjustment  # モータとボディのピッチ/アームの長さ
ARM_width = 12.0  # アームの幅

ARM_THICKNESS = 6.0  # アームの太さ
PLATE_THICKNESS = 3.0  # 天板/底板の厚み

MOTOR_PITCH = 19.0 / 2  # モータの取り付け穴ピッチ
FC_PITCH = 30.5 / 2  # FC/ESCの取り付けピンのピッチ

EXAMPLE = True
EXAMPLE = False


# 参考：モータ+プロペラ<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def create_dummy_motor():
    PROP_DEPTH = 9.0

    MOTOR_SIZE = 38.5

    MOTOR_Z1 = 45.30
    MOTOR_Z2 = 39.10
    MOTOR_Z3 = 16.60

    MOTOR_MAIN_DEPTH = MOTOR_Z2 - MOTOR_Z3
    MOTOR_MOUNT_DEPTH = MOTOR_Z1 - MOTOR_Z2

    # モータのステーター
    m = base.create_cylinder(
        radius=5.0 / 2,
        depth=MOTOR_Z1,
    )
    # モータの中間
    base.add_cylinder(
        target=m,
        radius=MOTOR_SIZE / 2,
        depth=MOTOR_MAIN_DEPTH,
        location=(0.0, 0.0, (MOTOR_Z1 - MOTOR_MAIN_DEPTH) / 2 - MOTOR_MOUNT_DEPTH),
    )
    # モータのマウントピン
    base.add_cylinder(
        target=m,
        radius=19.0 / 2,
        depth=MOTOR_MOUNT_DEPTH,
        location=(0.0, 0.0, (MOTOR_Z1 - MOTOR_MOUNT_DEPTH) / 2),
    )
    # プロペラ
    base.add_cylinder(
        target=m,
        radius=PROP_INCH / 2,
        depth=PROP_DEPTH,
        location=(0.0, 0.0, (MOTOR_Z1 - PROP_DEPTH) / 2 - MOTOR_MAIN_DEPTH - MOTOR_MOUNT_DEPTH),
    )

    # モータの位置調整
    m.location = (0.0, 0.0, -(MOTOR_Z1 + ARM_THICKNESS) / 2)
    # m.rotation_euler[0] = math.pi
    return m


# --------------------------------------
# アーム
# --------------------------------------
def create_arm_motor():

    # モータ台
    motor = base.create_cube(
        scale=(
            MOTOR_PITCH * 2.08,
            MOTOR_PITCH * 2.08,
            ARM_THICKNESS,
        )
    )

    ## 参考：dummyモータ+プロペラ<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    if EXAMPLE:
        base.modifier_apply(obj=create_dummy_motor(), target=motor, operation="UNION")

    # アーム を取り付け ----------------------------
    base.add_cube(
        target=motor,
        scale=(ARM_width, ARM_length, ARM_THICKNESS),
        location=(0.0, ARM_length / 2, 0.0),
    )
    # モータの回転軸と干渉する部分をカット ----------------------------
    base.cut_cylinder(
        target=motor, radius=M5 / 2, depth=ARM_THICKNESS * 2, location=(0.0, ARM_length, 0.0)
    )

    motor.rotation_euler[2] = math.pi / 4

    # アーム と モータ の取り付け穴 ----------------------------
    MOTOR_HOLES = [
        (MOTOR_PITCH, 0),
        (-MOTOR_PITCH, 0),
        (0, MOTOR_PITCH),
        (0, -MOTOR_PITCH),
    ]
    for i, (x, y) in enumerate(MOTOR_HOLES):
        base.add_ring(
            target=motor,
            outer_radius=M3 * 1.5,
            inner_radius=M3 / 2,
            depth=ARM_THICKNESS,
            location=(x, y, 0.0),
            vertices=64,
        )

    # 中心を変える ----------------------------
    motor.rotation_euler[2] = 0
    motor.location = (0.0, -ARM_length, 0.0)
    base.set_origin(motor, (0.0, 0.0, 0.0))

    # 45° 回転 ----------------------------
    motor.rotation_euler[2] = math.pi / 4

    # アーム と ボディプレート の取り付け穴 ----------------------------
    base.cut_cylinder(
        target=motor, radius=M3 / 2, depth=ARM_THICKNESS * 2, location=(FC_PITCH, -FC_PITCH, 0.0)
    )

    # アーム 同士が干渉する角をカット ----------------------------
    base.cut_cube(target=motor, scale=(20, 10, 10), location=(0.0, 5.0, 0.0))
    base.cut_cube(target=motor, scale=(10, 20, 10), location=(-5.0, 0.0, 0.0))
    return motor


# --------------------------------------
# センタープレート
# --------------------------------------
def create_plate():

    # 基板プレート
    body = base.create_cylinder(
        radius=24.5,
        depth=PLATE_THICKNESS,
    )

    # 中央穴(φ5)
    base.cut_cylinder(target=body, radius=M5 / 2, depth=PLATE_THICKNESS * 2)

    FC_HOLES = [
        (FC_PITCH, FC_PITCH),
        (FC_PITCH, -FC_PITCH),
        (-FC_PITCH, FC_PITCH),
        (-FC_PITCH, -FC_PITCH),
    ]

    # FCのピッチに合わせて合計8つ開ける
    for i, (x, y) in enumerate(FC_HOLES):
        base.add_ring(
            target=body,
            outer_radius=M3 * 2,
            inner_radius=M3 / 2,
            depth=PLATE_THICKNESS,
            location=(x, y, 0.0),
        )

    body.rotation_euler[2] = math.pi / 4
    for i, (x, y) in enumerate(FC_HOLES):
        base.add_ring(
            target=body,
            outer_radius=M3 * 1.25,
            inner_radius=M3 / 2,
            depth=PLATE_THICKNESS,
            location=(x, y, 0.0),
        )
    return body


# ------------------------------------------------------------------------------------
# 組み立て
# ------------------------------------------------------------------------------------

arm_motor = create_arm_motor()

# アームの出力用
#arm_motor.rotation_euler[2] = 0
#arm_motor.location = (0.0, ARM_length / 2, 0.0)
#base.set_origin(arm_motor, (0.0, 0.0, 0.0))

# 他の アーム を複製 ----------------------------
for i, (x) in enumerate([math.pi / 2, math.pi, -math.pi / 2]):
    base.copy(arm_motor, rotation=(0, 0, x))
arm_motor.rotation_euler[2] = 0

# 天板 ----------------------------
top = create_plate()
top.location = (0.0, 0.0, 3.0 + 1.5)

# 底板を複製 ----------------------------
bottom = base.copy(top, location=(0.0, 0.0, -3.0 - 1.5))

# ------------------------------------------------------------------------------------
# 参考(バッテリーx2、FC, ESC)
# ------------------------------------------------------------------------------------
if EXAMPLE:
    battery1 = base.create_cube(scale=(37, 37, 70))
    battery2 = base.copy(battery1)

    fc = base.create_cube(scale=(40, 40, 10), rotation=(0, 0, math.pi / 4))
    # esc = base.create_cube(scale=(56, 59, 10))
    esc = base.create_cube(scale=(40, 40, 10))

    battery1.location = (0.0, 0.0, 128.0)
    battery2.location = (0.0, 0.0, 54.0)

    fc.location = (0.0, 0.0, 12.0)
    esc.location = (0.0, 0.0, -12.0)

    bpy.ops.object.select_all(action="SELECT")
    bpy.context.view_layer.objects.active = next(iter(bpy.context.scene.objects))
    bpy.ops.object.join()
    bpy.context.active_object.rotation_euler[2] = math.pi / 4
    bpy.context.active_object.location.z -= 76
