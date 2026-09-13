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

#main = bpy.data.objects.get("battery__fixed")
#if main:
#    main.hide_set(True)

base.init()

#if main:
#    main.hide_set(False)

MAIN_WIDTH = 82.0
MAIN_HEIGHT = 79.2
MAIN_DEPTH = 7.0

MAIN_THICKNESS = 1.75

P = 19.8

# --------------------------------

main = base.create_cube(
    scale=(
        MAIN_WIDTH+MAIN_THICKNESS*2, 
        MAIN_HEIGHT+MAIN_THICKNESS*2, 
        MAIN_DEPTH+MAIN_THICKNESS
    ),
)

base.cut_corners(
    target=main,
    width=MAIN_WIDTH,
    height=MAIN_HEIGHT,
    depth=MAIN_DEPTH,
    thickness=MAIN_THICKNESS,
)

## --------------------------------

def create_main2():
    X = 6.8
    Y = MAIN_HEIGHT + 7.0
    main2 = base.create_cube(
        scale=(
            X + MAIN_THICKNESS * 2,
            Y + MAIN_THICKNESS * 2,
            MAIN_DEPTH+MAIN_THICKNESS,
        ),
    )
    base.cut_corners(
        target=main2,
        width=X,
        height=Y,
        depth=MAIN_DEPTH,
        thickness=MAIN_THICKNESS,
    )
    return main2

main2_1 = create_main2()
main2_2 = base.copy(main2_1)
main2_3 = base.copy(main2_1)
main2_4 = base.copy(main2_1)
main2_1.location=(P*1.5, 0.0, 0.0)
main2_2.location=(-P*1.5, 0.0, 0.0)
main2_3.location=(P/2, 0.0, 0.0)
main2_4.location=(-P/2, 0.0, 0.0)
base.modifier_apply(obj=main2_2, target=main, operation="UNION")
base.modifier_apply(obj=main2_3, target=main, operation="UNION")
base.modifier_apply(obj=main2_4, target=main, operation="UNION")
base.modifier_apply(obj=main2_1, target=main, operation="UNION")

## --------------------------------

base.cut_cube(
    target=main,
    scale=(
        MAIN_WIDTH,
        MAIN_HEIGHT,
        MAIN_DEPTH+0.01,
    ),
    location=(0.0, 0.0, MAIN_THICKNESS/2),
)

## --------------------------------

for i, (p) in enumerate([(P*1.5),(P/2),(-P/2),(-P*1.5)]):
    X = 6.8
    Y = MAIN_HEIGHT + 7.0
    
    base.cut_cube(
        target=main,
        scale=(
            X,
            Y,
            MAIN_DEPTH+MAIN_THICKNESS,
        ),
        location=(p, 0.0, MAIN_THICKNESS)
    )

    base.cut_cube(
        target=main,
        scale=(
            8.5,
            67.3,
            MAIN_DEPTH*2,
        ),
        location=(p, 0.0, 0.0),
    )
    
    base.cut_cylinder(
        target=main,
        radius=1.35,
        depth=MAIN_DEPTH*2,
        location=(p, MAIN_WIDTH/2, 0.0),
    )
    base.cut_cylinder(
        target=main,
        radius=1.35,
        depth=MAIN_DEPTH*2,
        location=(p, -MAIN_WIDTH/2, 0.0),
    )
    
## --------------------------------

X = (36.75+42.45)/4
Y = (53.9+59.9)/4
for i, (x, y) in enumerate([(X, Y), (X, -Y), (-X, -Y), (-X, Y)]):
    base.cut_cylinder(
        target=main,
        radius=1.9,
        depth=MAIN_DEPTH*2,
        location=(x, y, 0.0),
    )

## --------------------------------
