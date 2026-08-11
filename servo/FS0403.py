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

MAIN_WIDTH = 27.4
MAIN_HEIGHT = 8.0
MAIN_DEPTH = 2.0

MAIN_THICKNESS = 1.5

main = base.create_cube(
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
)

M2 = 0.95
M4 = 4.1
M5_6 = 2.3

base.add_ring(
    target=main,
    outer_radius=M4 + 2.0,
    inner_radius=M4,
    location=(10.0 - M4, 0, 0),
    depth=MAIN_DEPTH,
)
base.cut_holes(
    target=main,
    radius=M2,
    depth=MAIN_DEPTH,
    positions=[(11.0 + M2, 0), (-(11.0 + M2), 0)],
)
base.cut_holes(
    target=main,
    radius=M5_6,
    depth=MAIN_DEPTH,
    positions=[(- 0.55 + M5_6, 0)],
)
base.cut_holes(
    target=main,
    radius=M2,
    depth=MAIN_DEPTH,
    positions=[(- 3.3 + M2, 0)],
)
