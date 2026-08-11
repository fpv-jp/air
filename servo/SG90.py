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

MAIN_WIDTH = 32.3
MAIN_HEIGHT = 11.6
MAIN_DEPTH = 2.0

main = base.create_cube(
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
)

M2 = 1.25
M11_5 = 6.0
M5_6 = 3.0

base.add_ring(
    target=main,
    outer_radius=M11_5 + 2.5,
    inner_radius=M11_5,
    location=(22.5 / 2 - M11_5, 0, 0),
    depth=MAIN_DEPTH,
)

base.cut_holes(
    target=main,
    radius=M2,
    depth=MAIN_DEPTH,
    positions=[(12.5 + M2, 0), (-(12.5 + M2), 0)],
)
base.cut_holes(
    target=main,
    radius=M5_6,
    depth=MAIN_DEPTH,
    positions=[(0, 0)],
)
