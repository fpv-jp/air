import bpy
import bmesh
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

### ----------------------------------------------------------------------------------------------------------------

MAIN_THICKNESS = 1.25

MAIN_WIDTH = (36.75+42.45)/1.65
MAIN_HEIGHT = (53.9+59.9)/1.75

MAIN_DEPTH = 3.5

main = base.create_cube(
    scale=(
        MAIN_WIDTH + MAIN_THICKNESS * 2,
        MAIN_HEIGHT + MAIN_THICKNESS * 2,
        MAIN_DEPTH,
    ),
)

base.cut_corners(
    target=main,
    width=MAIN_WIDTH,
    height=MAIN_HEIGHT,
    depth=MAIN_DEPTH - MAIN_THICKNESS,
    thickness=MAIN_THICKNESS,
)
base.cut_inner_corners(
    target=main,
    width=MAIN_WIDTH-15,
    height=MAIN_HEIGHT-15,
    depth=MAIN_DEPTH+10,
    thickness=MAIN_THICKNESS,
)

X = (36.75+42.45)/4
Y = (53.9+59.9)/4
for i, (x, y) in enumerate([(X, Y), (X, -Y), (-X, -Y), (-X, Y)]):
    base.cut_cylinder(
        target=main,
        radius=1.9,
        depth=MAIN_DEPTH*2,
        location=(x, y, 0.0),
    )


main.location=(0.0, -MAIN_HEIGHT/2, 0.0)

### ----------------------------------------------------------------------------------------------------------------

BASE_PLATE_WIDTH = 40
BASE_PLATE_HEIGHT = 30
BASE_PLATE_DEPTH = 3.5

CORNER_CUT_SIZE = 6.5

MESH1 = bpy.data.meshes.new("HexagonalPlate")
PLATE2 = bpy.data.objects.new("HexagonalPlate", MESH1)
bpy.context.collection.objects.link(PLATE2)


HW = BASE_PLATE_WIDTH / 2
HH = BASE_PLATE_HEIGHT / 2

hexagon_vertices = [
    # 上辺
    (-HW + CORNER_CUT_SIZE, HH, 0),
    (HW - CORNER_CUT_SIZE, HH, 0),
    # 右辺
    (HW, HH / 2 - CORNER_CUT_SIZE, 0),
    (HW, -HH / 2 + CORNER_CUT_SIZE, 0),
    # 下辺
    (HW - CORNER_CUT_SIZE, -HH, 0),
    (-HW + CORNER_CUT_SIZE, -HH, 0),
    # 左辺
    (-HW, -HH / 2 + CORNER_CUT_SIZE, 0),
    (-HW, HH / 2 - CORNER_CUT_SIZE, 0),
]

OBJ3 = bmesh.new()

bmesh_vertices = []
for vertex in hexagon_vertices:
    bmesh_vertices.append(OBJ3.verts.new(vertex))

OBJ3.faces.new(bmesh_vertices)
extruded_geometry = bmesh.ops.extrude_face_region(OBJ3, geom=OBJ3.faces[:])
bmesh.ops.translate(
    OBJ3,
    vec=(0, 0, BASE_PLATE_DEPTH),
    verts=[v for v in extruded_geometry["geom"] if isinstance(v, bmesh.types.BMVert)],
)

OBJ3.normal_update()
OBJ3.faces.ensure_lookup_table()
OBJ3.to_mesh(MESH1)
OBJ3.free()

base.cut_holes(
    target=PLATE2,
    radius=1.75,
    depth=15,
    positions=[(15.25, 0), (-15.25, 0)],
)

base.cut_cylinder(
    target=PLATE2,
    radius=9.5,
    depth=BASE_PLATE_DEPTH*2,
)

PLATE2.location=(0.0, MAIN_HEIGHT/2, -BASE_PLATE_DEPTH/2)

### ----------------------------------------------------------------------------------------------------------------

main2 = base.create_cube(
    scale=(29, 20, MAIN_DEPTH),
)
base.add_cube(
    target=main2,
    scale=(106.5, 8.0, MAIN_DEPTH),
#    location=(0.0, 0.0, -MAIN_DEPTH/2+1.7/2)
)
base.cut_cube(
    target=main2,
    scale=(13, 20, MAIN_DEPTH),
)
base.add_ring(
    target=main2,
    outer_radius=8,
    inner_radius=3.3,
    depth=1.7,
    location=(60, 0, -MAIN_DEPTH/2+1.7/2),
)
base.add_ring(
    target=main2,
    outer_radius=8,
    inner_radius=3.3,
    depth=1.7,
    location=(-60, 0, -MAIN_DEPTH/2+1.7/2),
)
main2.location=(0.0, 10.0, 0.0)

base.modifier_apply(obj=main2, target=main, operation="UNION")
base.modifier_apply(obj=PLATE2, target=main, operation="UNION")
