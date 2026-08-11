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

# main -----------------------------------

MAIN_WIDTH = 40.0
MAIN_HEIGHT = 55.0
MAIN_DEPTH = 8.0

WALL = 3.0

main = base.create_cube(
    scale=(
        MAIN_WIDTH ,
        MAIN_HEIGHT,
        MAIN_DEPTH,
    ),
)
base.cut_cube(
    target=main,
    scale=(
        MAIN_WIDTH -WALL*2,
        MAIN_HEIGHT,
        MAIN_DEPTH,
    ),
    location=(0, 0, WALL),
)
base.cut_cube(
    target=main,
    scale=(
        MAIN_WIDTH -MAIN_DEPTH*2,
        MAIN_HEIGHT -MAIN_DEPTH*2,
        MAIN_DEPTH,
    ),
)

# -----------------------------------

def bar():
    MAIN_WIDTH = 60.0
    MAIN_HEIGHT = 8.0
    MAIN_DEPTH = 3.0

    main = base.create_cube(
        scale=(
            MAIN_WIDTH ,
            MAIN_HEIGHT,
            MAIN_DEPTH,
        ),
    )

    base.cut_cylinder(
        target=main,
        radius=1.75,
        depth=MAIN_HEIGHT+1,
        location=(25, 0, 0),
    )
    base.cut_cylinder(
        target=main,
        radius=1.75,
        depth=MAIN_HEIGHT+1,
        location=(-25, 0, 0),
    )
    main.rotation_euler = (math.pi / 2, 0, 0)
    return main

a = bar()
a.location[1] = (MAIN_HEIGHT+WALL)/2
b = bar()
b.location[1] = -(MAIN_HEIGHT+WALL)/2

# -----------------------------------

base.modifier_apply(obj=a, target=main, operation="UNION")
base.modifier_apply(obj=b, target=main, operation="UNION")
