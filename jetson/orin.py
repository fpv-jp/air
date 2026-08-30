import bpy
import sys
import types

text = bpy.data.texts.get("base.py")
module_name = "base"
module = types.ModuleType(module_name)
exec(text.as_string(), module.__dict__)
sys.modules[module_name] = module

import base

assembly = bpy.data.objects.get("000_ARVALA_TLA_ASM")
assembly.hide_set(True)
base.init()
assembly.hide_set(False)
assembly.location = (-46.0, -22.6, -1.6)

base.set_color(assembly, "Red", (0.8, 0.1, 0.1))

MAIN_WIDTH = 100.0
MAIN_HEIGHT = 79.0
MAIN_DEPTH = 12.0

MAIN_THICKNESS = 2.0
MAIN_GAP = 0.2

main = base.create_cube(
    scale=(MAIN_WIDTH + MAIN_THICKNESS, MAIN_HEIGHT + MAIN_THICKNESS, MAIN_DEPTH),
)
base.cut_corners(
    target=main,
    width=MAIN_WIDTH,
    height=MAIN_HEIGHT,
    depth=MAIN_DEPTH - MAIN_THICKNESS / 2,
    thickness=MAIN_THICKNESS / 2,
)
base.cut_cube(
    target=main,
    scale=(MAIN_WIDTH + MAIN_GAP, MAIN_HEIGHT + MAIN_GAP, MAIN_DEPTH),
    location=(0, 0, -MAIN_THICKNESS / 2),
)

base.cut_holes(
    target=main,
    radius=1.3,
    depth=MAIN_DEPTH + MAIN_THICKNESS,
    positions=[
        (40.0, 35.5),
        (40.0, -22.6),
        (-46.0, 35.5),
        (-46.0, -22.6),
    ],
)

## ----------------------------------------

#main.location[0] = -MAIN_WIDTH / 2
#assembly.location[0] += main.location[0]

#main.location[1] = -MAIN_HEIGHT / 2
#assembly.location[1] += main.location[1]

main.location[2] = -MAIN_DEPTH / 2 +1


#def cut_bottom_opening(scale, x):
#    y = (scale[1] - MAIN_HEIGHT ) / 2 - MAIN_THICKNESS
#    base.cut_cube(
#        target=main,
#        scale=scale,
#        location=(x, y, scale[2] / 2),
#    )


#OPENING_DEPTH = 5.0

#cut_bottom_opening(scale=(9.5, 5.0, 12.2), x=-44.0)  # DC
#cut_bottom_opening(scale=(18.7, 5.0, 7.9), x=-27.2)  # DP
#cut_bottom_opening(scale=(14.6, 18.7, 18.5), x=-7.4)  # USB1
#cut_bottom_opening(scale=(14.6, 18.7, 18.5), x=9.6)  # USB2
#cut_bottom_opening(scale=(16.5, 22.5, 15.1), x=26.9)  # LAN
#cut_bottom_opening(scale=(9.3, 5.0, 4.7), x=42.0)  # USB-C

## ----------------------------------------


##def cut_opening(scale, x, y):
##    base.cut_cube(
##        target=main,
##        scale=scale,
##        location=(x, y, scale[2] / 2),
##    )


##cut_opening(scale=(59.0, 40.0, 25.3), x=-2.0, y=19.5)
##cut_opening(scale=(5.8, 51.0, 25.3), x=45.8, y=7.0)
##cut_opening(scale=(6.8, 3.0, 25.3), x=30.8, y=31.0)


## ----------------------------------------




##def cut_opening2(scale, x, y):
##    z = (scale[2] - MAIN_DEPTH - MAIN_THICKNESS) / 2
##base.cut_cube(
##    target=main,
##    scale=(6.8, 3.0, 25.3),
##    location=(
##        x, 
##        y, 
##        (scale[2] - MAIN_DEPTH - MAIN_THICKNESS) / 2
##    ),
##)



