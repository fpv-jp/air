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

base.init()

MAIN_WIDTH = 18.0
MAIN_HEIGHT = 26.0
MAIN_DEPTH = 4.5

MAIN_THICKNESS = 1.75

POSX = 18.0 / 2
POSY = 26.0 / 2

# --------------------------------

R1 = 3.25 / 2
P = 82.5 / 2

main = base.create_cube(
    scale=(
        R1 * 4,
        P * 2,
        MAIN_THICKNESS,
    ),
)

positions = [
    (0.0, P),
    (0.0, -P),
]
for i, (x, y) in enumerate(positions):
    base.add_ring(
        target=main,
        outer_radius=R1 * 2,
        inner_radius=R1,
        depth=MAIN_THICKNESS,
        location=(x, y, 0.0),
    )


R = 1.25

# -------------------------------- wif

MAIN_WIDTH = 33.1
MAIN_HEIGHT = 33.1
MAIN_DEPTH = 5.3

main.location = (
    -MAIN_WIDTH / 2 - R1 * 2 - MAIN_THICKNESS / 2,
    0.0,
    MAIN_THICKNESS / 2,
)

wifi = base.create_cube(
    scale=(
        MAIN_WIDTH + MAIN_THICKNESS,
        MAIN_HEIGHT + MAIN_THICKNESS,
        MAIN_DEPTH,
    ),
)

base.cut_cube(
    target=wifi,
    scale=(
        MAIN_WIDTH - MAIN_THICKNESS / 2,
        MAIN_HEIGHT - MAIN_THICKNESS / 2,
        MAIN_DEPTH,
    ),
    location=(0.0, 0.0, MAIN_THICKNESS),
)

X2 = MAIN_HEIGHT / 2

for i, (y) in enumerate([X2, -X2]):
    base.cut_cube(
        target=wifi,
        scale=(
            6.0,
            6.0,
            MAIN_THICKNESS * 2,
        ),
        location=(-MAIN_WIDTH / 2, y, MAIN_THICKNESS),
    )

wifi.location = (0.0, 0.0, MAIN_DEPTH / 2)
base.modifier_apply(obj=wifi, target=main, operation="UNION")


# --------------------------------

#X = 44.0
base.cut_cube(
    target=main,
    scale=(
        32.0,
        18.0,
        12.0,
    ),
    location=(5.0, 0.0, 0.0),
)
