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

MAIN_WIDTH = 42.0
MAIN_HEIGHT = 41.5
MAIN_DEPTH = 2.0

main = base.create_cube(
    scale=(
        MAIN_WIDTH,
        MAIN_HEIGHT,
        MAIN_DEPTH
    ),
)

X = 35.75/2
holes = [(X,-X), (-X,-X), (-X,X), (X,X)]
for i, (x, y) in enumerate(holes):
    base.cut_cylinder(
        target=main,
        radius=1.25,
        depth=MAIN_DEPTH + 1,
        location=(x, y, 0.0),
    )
#    base.add_ring(
#        target=main,
#        outer_radius=2,
#        inner_radius=1,
#        depth=MAIN_DEPTH + 1,
#        location=(x, y, 0),
#    )

H = 2.5
base.cut_cube(
    target=main,
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH-H),
#    location=(0, 0, H/2),
)
