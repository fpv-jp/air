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

    # モータ の取り付け穴 ----------------------------
    MOTOR_PITCH = 19.0 / 2  # モータの取り付け穴ピッチ
    MOTOR_HOLES = [
        (MOTOR_PITCH, 0),
        (-MOTOR_PITCH, 0),
        (0, MOTOR_PITCH),
        (0, -MOTOR_PITCH),
    ]
    for i, (x, y) in enumerate(MOTOR_HOLES):
        base.cut_cylinder(
            target=motor,
            radius=4.0,
            depth=53.0,
            location=(x, y, 0.0),
        )
    motor.rotation_euler[2] = math.pi / 4

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
            ARM_width - sharpen2,
            DRONE_SIZE / 1.75,
            ARM_width * 3 - sharpen2,
        ),
        location=(0.0, DRONE_SIZE / 4, 0.0),
    )

    # --- アーム 上部 ---
    arm_top = base.create_tear_beam(
        depth=DRONE_SIZE / 1.75,
        width=ARM_width - sharpen2,
        height=ARM_width * 3 - sharpen2,
        power=0.75,
        location=(0.0, DRONE_SIZE / 4, -ARM_width * 1.2),
    )

    # --- アーム 中央 上部 結合し傾けて少し上にずらす ---
    base.modifier_apply(obj=arm_top, target=arm, operation="UNION")
    arm.rotation_euler = (math.pi / 8, 0, 0)
    arm.location = (0.0, 0.0, -ARM_width * 1.9)

    # --- 下を少しカット ---
    base.cut_cube(
        target=arm,
        scale=(ARM_width, DRONE_SIZE, ARM_width * 4),
        location=(0.0, DRONE_SIZE / 4, ARM_width * 1.75),
    )

    # --- アーム 下部 ---
    arm_bottom = base.create_tear_beam(
        depth=DRONE_SIZE / 2,
        width=ARM_width - sharpen2,
        height=ARM_width * 3 - sharpen2,
        power=0.75,
        location=(0.0, DRONE_SIZE / 4, 5.5),
    )

    # --- アーム 中央 上部 と 下部 を 結合 ---
    base.modifier_apply(obj=arm_bottom, target=arm, operation="UNION")

    return arm


# -------------------------------------------------------
# アーム + モータ
# -------------------------------------------------------
def create_motor_arm():

    # --- アーム
    arm = create_arm(0)
    # --- アーム(中をくり抜く) ---
    # arm_inner = create_arm(WALL_hickness)
    # base.modifier_apply(obj=arm_inner, target=arm, operation="DIFFERENCE")

    location = (0, MOTOR_PITCH, 16.0)  # アーム に対して モータ を取り付ける位置

    if BUILD_MIDDLE:
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
        # motor_inner = create_motor(WALL_hickness)
        # motor_inner.location = location
        # base.modifier_apply(obj=motor_inner, target=arm, operation="DIFFERENCE")

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

    CENTER_BODY_height = BODY_height / 2.5

    # --- ボディ 中央 ---
    body = base.create_cylinder(
        radius=BODY_radius - 0.1 - sharpen,
        depth=CENTER_BODY_height,
        location=(0.0, 0.0, (11.0) if sharpen > 0 else (11.1)),
        vertices=64,
    )

    if BUILD_TOP or BUILD_MIDDLE:
        # --- ボディ 上部 ---
        body_top = base.create_tear_body(
            radius=BODY_radius - sharpen, depth=BODY_height, power=0.66, smooth=False
        )
        body_top.location = (0.0, 0.0, sharpen)

    if BUILD_BOTTOM or BUILD_MIDDLE:
        # --- ボディ 下部 ---
        body_bottom = base.create_tear_body(
            radius=BODY_radius - sharpen, depth=BODY_height, power=0.66, peak=0.75, smooth=False
        )
        body_bottom.location = (0.0, 0.0, -sharpen)

    # --- ボディ を結合 ---
    if BUILD_TOP or BUILD_MIDDLE:
        base.modifier_apply(obj=body_top, target=body, operation="UNION")
    if BUILD_BOTTOM or BUILD_MIDDLE:
        base.modifier_apply(obj=body_bottom, target=body, operation="UNION")

    # パーツに分けた時の止め合わせを追加
    if sharpen != 0:
        W = 3.0
        D = 5.5
        H = 15.0

        H2 = H * 2.0

        X = 8.0
        Y = 28.0

        TOP = -11.0
        BOTTOM = 65.0

        if BUILD_TOP:
            for i, (y) in enumerate([BODY_radius, -BODY_radius]):
                # ボディ 中央との取り付け部分
                base.cut_cube(
                    target=body,
                    scale=(Y, X, H * 2),
                    location=(0.0, y, TOP),
                )
                # 取り付け部分の凹
                base.add_cube(
                    target=body,
                    scale=(W + 0.2, D + 0.2, H2),
                    location=(0.0, y, TOP + H / 2),
                )

        if BUILD_MIDDLE:
            # ボディ 上部との凸
            for i, (y) in enumerate([BODY_radius, -BODY_radius]):
                base.cut_cube(
                    target=body,
                    scale=(W, D, H - 3),
                    location=(0.0, y, TOP),
                )
            # ボディ 下部との凸
            body.rotation_euler = (0, 0, math.pi / 4)
            for i, (x) in enumerate([BODY_radius, -BODY_radius]):
                base.cut_cube(
                    target=body,
                    scale=(D, W, H - 3),
                    location=(x, 0.0, BOTTOM),
                )
            body.rotation_euler = (0, 0, 0)

        if BUILD_BOTTOM:
            body.rotation_euler = (0, 0, math.pi / 4)
            for i, (x) in enumerate([BODY_radius, -BODY_radius]):
                # ボディ 中央との取り付け部分
                base.cut_cube(
                    target=body,
                    scale=(X, Y, H * 2),
                    location=(x, 0.0, BOTTOM),
                )
                # 取り付け部分の凹
                base.add_cube(
                    target=body,
                    scale=(D + 0.2, W + 0.2, H2),
                    location=(x, 0.0, BOTTOM - H2 / 4),
                )
            body.rotation_euler = (0, 0, 0)
    return body


# --------------------------------------------
# --- アッセンブリ ---------------------------
# --------------------------------------------

if BUILD_BOTTOM or BUILD_MIDDLE:
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

if BUILD_BOTTOM or BUILD_MIDDLE:
    # --- ボディ に腕を結合 ---
    base.modifier_apply(obj=motor_arm1, target=body, operation="UNION")
    base.modifier_apply(obj=motor_arm2, target=body, operation="UNION")
    base.modifier_apply(obj=motor_arm3, target=body, operation="UNION")
    base.modifier_apply(obj=motor_arm4, target=body, operation="UNION")

# --- ボディ を中空化 ---
body_inner = create_body(WALL_hickness)
base.modifier_apply(obj=body_inner, target=body, operation="DIFFERENCE")


if BUILD_TOP or BUILD_MIDDLE:
    # --- ボディ 中央と上部の共通ネジ穴
    base.cut_cylinder(
        target=body,
        radius=1.6,
        depth=BODY_radius * 2.1,
        location=(0.0, 0.0, -3.0),
        rotation=(math.pi / 2, 0, 0),
    )


if BUILD_BOTTOM or BUILD_MIDDLE:
    # --- ボディ 中央と下部の共通ネジ穴
    body.rotation_euler = (0, 0, math.pi / 4)
    base.cut_cylinder(
        target=body,
        radius=1.6,
        depth=BODY_radius * 2.1,
        location=(0.0, 0.0, 57.0),
        rotation=(0, math.pi / 2, 0),
    )

    body.rotation_euler = (0, 0, 0)

    # アームのボディが重なる部分をカット
    location = (0.0, 0.0, 21.0 + ARM_position)
    x = ARM_width + 0.1
    y = DRONE_SIZE
    base.cut_cube(target=body, scale=(x, y, 6.1), location=(location))
    base.cut_cube(target=body, scale=(y, x, 6.1), location=(location))

    # モータとESCのワイヤを通す穴
    for i, (x, y) in enumerate([(math.pi / 2, 0), (0, math.pi / 2)]):
        base.cut_cylinder(
            target=body,
            radius=4.0,
            depth=DRONE_SIZE,
            location=(0.0, 0.0, 29.5 + ARM_position),
            rotation=(x, y, 0),
        )

# --- 確認のため前面カット ---
#base.bisect(body, plane_co=(0, 0, 0), plane_no=(0, 1, 0), clear_outer=True)

# そのままだと3Dプリンタのサイズを超えるので調整
body.rotation_euler = (math.pi, 0, math.pi / 4)

# -------------------------------------------------------
# BUILD_TOP
# -------------------------------------------------------

if BUILD_TOP:
    # 不要な下部をカット
    H = 190.0
    base.cut_cylinder(
        target=body,
        radius=BODY_radius + 1,
        depth=6 + H,
        location=(0.0, 0.0, -H / 2 - 35.0),
    )

    # 不要な外壁をカット
    depth = 54
    location = (0.0, 0.0, -8.0)
    body_inner = base.create_cylinder(
        radius=BODY_radius,
        depth=depth,
        location=location,
        vertices=64,
    )
    base.cut_cylinder(
        target=body_inner,
        radius=BODY_radius - 0.15 - WALL_hickness,
        depth=depth,
        location=location,
        vertices=64,
    )
    base.modifier_apply(obj=body_inner, target=body, operation="DIFFERENCE")


# -------------------------------------------------------
# BUILD_MIDDLE
# -------------------------------------------------------

if BUILD_MIDDLE:
    # 不要な上部をカット
    H = 80.0
    base.cut_cylinder(
        target=body,
        radius=93.5,
        depth=6 + H,
        location=(0.0, 0.0, -76.0 - H / 2),
    )

    # 不要な下部をカット
    H = 170.0
    base.cut_cylinder(
        target=body,
        radius=BODY_radius + 1,
        depth=6 + H,
        location=(0.0, 0.0, H / 2 + 22.0),
    )


# -------------------------------------------------------
# BUILD_BOTTOM
# -------------------------------------------------------

if BUILD_BOTTOM:
    # 不要な上部をカット
    H = 200.0
    base.cut_cylinder(
        target=body,
        radius=BODY_radius + 1,
        depth=6 + H,
        location=(0.0, 0.0, H / 2 - 19.0),
    )

    # 不要な外壁をカット
    depth = 54
    location = (0.0, 0.0, -46.0)
    body_inner = base.create_cylinder(
        radius=BODY_radius,
        depth=depth,
        location=location,
        vertices=64,
    )
    base.cut_cylinder(
        target=body_inner,
        radius=BODY_radius - 0.15 - WALL_hickness,
        depth=depth,
        location=location,
        vertices=64,
    )
    base.modifier_apply(obj=body_inner, target=body, operation="DIFFERENCE")

    # アーム上部をカット
    for i, (r) in enumerate([math.pi / 4, -math.pi / 4]):
        base.cut_cube(
            target=body,
            scale=(12.1, DRONE_SIZE * 1.1, 45.0),
            location=(0.0, 0.0, -54.0),
            rotation=(0, 0, r),
        )
