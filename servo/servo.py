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


#Untitled = bpy.data.objects.get("Untitled")
#Untitled.location=(-5.1, 0.5, -6.4)


### ----------------------------------------------------------------------------------------------------------------

def Create_FS0403():
    MAIN_WIDTH = 27.4
    MAIN_HEIGHT = 8.0
    MAIN_DEPTH = 7.2

    main = base.create_cube(
        scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
    )

    base.add_ring(
        target=main,
        outer_radius=6.8,
        inner_radius=4.3,
        location=(5.9, 0, 0),
        depth=MAIN_DEPTH,
    )
    base.cut_holes(
        target=main,
        radius=2.3,
        depth=MAIN_DEPTH,
        positions=[
            (1.75, 0),
        ],
    )
    base.cut_holes(
        target=main,
        radius=0.95,
        depth=MAIN_DEPTH,
        positions=[
            (-2.35, 0),
        ],
    )
    base.cut_holes(
        target=main,
        radius=0.95,
        depth=MAIN_DEPTH,
        positions=[
            (11.95, 0),
            (-11.95, 0),
        ],
    )

    base.cut_cube(
        target=main,
        scale=(20.0, 20.0, 3.6),
        location=(0.3, 0, 1.8),
    )
    base.cut_cube(
        target=main,
        scale=(30.0, 20.0, 3.6),
        location=(0.0, 14.0, 1.8),
    )
    base.cut_cube(
        target=main,
        scale=(30.0, 20.0, 3.6),
        location=(0.0, -14.0, 1.8),
    )

    return main

### ----------------------------------------------------------------------------------------------------------------
def Build_FS0403():
    FS0403 = Create_FS0403()

    FS0403.rotation_euler[0] = math.pi / 2
    FS0403.rotation_euler[2] = math.pi / 2

    MAIN_WIDTH = 34.8
    MAIN_HEIGHT = 17.4
    MAIN_DEPTH = 8.0

    MAIN_THICKNESS = 3.2

    FS0403.location[0] = (MAIN_WIDTH+MAIN_THICKNESS) / 2

    main = base.create_cube(
        scale=(MAIN_WIDTH + MAIN_THICKNESS*2, MAIN_HEIGHT + MAIN_THICKNESS*2, MAIN_DEPTH),
    )
    base.cut_cube(target=main,
        scale=(MAIN_WIDTH+MAIN_THICKNESS, MAIN_HEIGHT+MAIN_THICKNESS, MAIN_DEPTH),
        location=(MAIN_THICKNESS/2, MAIN_THICKNESS, 0.0),
    )

    base.add_cube(
        target=main,
        scale=(20.0, 1.2, MAIN_DEPTH),
        location=(MAIN_WIDTH/2+MAIN_THICKNESS-10.0, -MAIN_HEIGHT/2 - MAIN_THICKNESS -0.6, 0),
    )
    def punch_hole(r,x):
        base.cut_cylinder(
            target=main,
            radius=r,
            depth=MAIN_THICKNESS*2,
            rotation=(math.pi / 2, 0, 0),
            location=(x-3.3, -(MAIN_HEIGHT+MAIN_THICKNESS)/2, 0)
        )
#        base.add_cylinder(
#            target=main,
#            radius=0.15,
#            depth=31,
#            rotation=(math.pi / 2, 0, 0),
#            location=(x-3.3, 0, 0)
#        )
    punch_hole(1.25, 0)
    punch_hole(0.7, 6)
    punch_hole(0.7, 15.7)

    main.location[1] = -5.0-MAIN_THICKNESS/2

#    base.add_cylinder(
#        target=main,
##        radius=6.5,
#        radius=0.15,
#        depth=41,
#        rotation=(0, math.pi / 2, 0),
#        location=(0, 5.9, 0),
#    )
    base.add_ring(
        target=main,
        outer_radius=4.1,
        inner_radius=1.8,
        rotation=(0, math.pi / 2, 0),
        location=(-(MAIN_WIDTH+MAIN_THICKNESS)/2, 5.9, 0),
        depth=MAIN_THICKNESS,
    )
    base.modifier_apply(obj=FS0403, target=main, operation="UNION")

    return main

FS0403 = Build_FS0403()

### ----------------------------------------------------------------------------------------------------------------
### ----------------------------------------------------------------------------------------------------------------
### ----------------------------------------------------------------------------------------------------------------
### ----------------------------------------------------------------------------------------------------------------
### ----------------------------------------------------------------------------------------------------------------

def Create_SG90():
    MAIN_WIDTH = 32.3
    MAIN_HEIGHT = 11.6
    MAIN_DEPTH = 8.3

    main = base.create_cube(
        scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
    )

    base.add_ring(
        target=main,
        outer_radius=8.5,
        inner_radius=6.1,
        location=(5.25, 0, 0),
        depth=MAIN_DEPTH,
    )
    base.cut_holes(
        target=main,
        radius=3.1,
        depth=MAIN_DEPTH,
        positions=[
            (0, 0),
        ],
    )
    base.cut_holes(
        target=main,
        radius=1.25,
        depth=MAIN_DEPTH,
        positions=[
            (13.75, 0),
            (-13.75, 0),
        ],
    )

    base.cut_cube(
        target=main,
        scale=(22.7, 22.7, MAIN_DEPTH / 2),
        location=(0, 0, MAIN_DEPTH / 4),
    )
    return main

### ----------------------------------------------------------------------------------------------------------------

def Build_SG90():
    SG90 = Create_SG90()

    MAIN_WIDTH = 26.3
    MAIN_HEIGHT = 11.6
    MAIN_DEPTH = 11.6

    MAIN_THICKNESS = 3.0

    MAIN_DEPTH2 = 8.3

    main = base.create_cube(
        scale=(MAIN_WIDTH + MAIN_THICKNESS*2, MAIN_HEIGHT, MAIN_DEPTH2),
    )
    base.cut_cube(target=main,
        scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH2+0.1),
    )

    base.cut_cylinder(
        target=main,
        radius=1.75,
        depth=35,
        rotation=(0, math.pi / 2, 0),
#        location=(0, 4.0, 0),
    )
    main.location[1] = 11.6

    base.modifier_apply(obj=SG90, target=main, operation="UNION")
    return main

#SG90 = Build_SG90()

#### ----------------------------------------------------------------------------------------------------------------

##############################

#FS0403 = Build_FS0403()

#FS0403.rotation_euler[0] = -math.pi / 2
#FS0403.location = (-3, 0, -15)

##############################

#SG90 = Build_SG90()

#SG90.rotation_euler[2] = math.pi
#SG90.location = (0, 10, 5)
