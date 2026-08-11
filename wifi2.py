
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
    if i == 0:
        base.add_ring(
            target=main,
            outer_radius=R1 * 2,
            inner_radius=R1,
            depth=MAIN_THICKNESS,
            location=(x, y, 0.0),
        )

main.location = (0.0, P, 0.0)

base.add_cube(
    target=main,
    scale=(
        16.0,
        52.0,
        MAIN_THICKNESS,
    ),
)
