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
BASE_PLATE_WIDTH = 42
BASE_PLATE_HEIGHT = 32
BASE_PLATE_THICKNESS = 3.5
CORNER_CUT_SIZE = 6.5

def create_hexagonal_plate():

    hexagonal_mesh = bpy.data.meshes.new("HexagonalPlate")
    hexagonal_plate = bpy.data.objects.new("HexagonalPlate", hexagonal_mesh)
    bpy.context.collection.objects.link(hexagonal_plate)
    bmesh_obj = bmesh.new()

    half_width = BASE_PLATE_WIDTH / 2
    half_height = BASE_PLATE_HEIGHT / 2

    hexagon_vertices = [
        # 上辺
        (-half_width + CORNER_CUT_SIZE, half_height, 0),
        (half_width - CORNER_CUT_SIZE, half_height, 0),
        # 右辺
        (half_width, half_height / 2 - CORNER_CUT_SIZE, 0),
        (half_width, -half_height / 2 + CORNER_CUT_SIZE, 0),
        # 下辺
        (half_width - CORNER_CUT_SIZE, -half_height, 0),
        (-half_width + CORNER_CUT_SIZE, -half_height, 0),
        # 左辺
        (-half_width, -half_height / 2 + CORNER_CUT_SIZE, 0),
        (-half_width, half_height / 2 - CORNER_CUT_SIZE, 0),
    ]

    bmesh_vertices = []
    for vertex in hexagon_vertices:
        bmesh_vertices.append(bmesh_obj.verts.new(vertex))

    bmesh_obj.faces.new(bmesh_vertices)
    extruded_geometry = bmesh.ops.extrude_face_region(bmesh_obj, geom=bmesh_obj.faces[:])
    bmesh.ops.translate(
        bmesh_obj,
        vec=(0, 0, BASE_PLATE_THICKNESS),
        verts=[v for v in extruded_geometry["geom"] if isinstance(v, bmesh.types.BMVert)],
    )

    bmesh_obj.normal_update()
    bmesh_obj.faces.ensure_lookup_table()
    bmesh_obj.to_mesh(hexagonal_mesh)
    bmesh_obj.free()
    return hexagonal_plate

### ----------------------------------------------------------------------------------------------------------------
CM4_WIDTH = 24.0
CM4_HEIGHT = 14.0
CM4_DEPTH = 33

def create_support(x1, x2, x3):
    
    support = base.create_cube(scale=(CM4_WIDTH, CM4_HEIGHT, CM4_DEPTH))

    base.cut_cube(
       target=support,
       scale=(CM4_WIDTH, 6, CM4_DEPTH),
       location=(x1, 0, 2),
    )

    base.cut_cube(
       target=support,
       scale=(CM4_WIDTH, CM4_HEIGHT, CM4_DEPTH),
       location=(x1 + x2, CM4_HEIGHT/2, 10),
    )
    
    support.rotation_euler[0] = math.radians(25)
    support.location[0] = x3
    support.location[1] = -5.0
    support.location[2] = CM4_DEPTH/2 - 1
    
    return support


def create_support2():
    support = base.create_cube(
       scale=(BASE_PLATE_WIDTH/3, BASE_PLATE_HEIGHT*1.75, 20),
       location=(0, -BASE_PLATE_HEIGHT, 10),
    )
    base.cut_cube(
       target=support,
       scale=(BASE_PLATE_WIDTH/3-6.0, BASE_PLATE_HEIGHT*1.75, 20),
       location=(0, -BASE_PLATE_HEIGHT, 10 + 3.5),
    )
    base.cut_cube(
       target=support,
       scale=(CM4_WIDTH, 10, CM4_DEPTH*2),
       location=(0, 0, 2),
       rotation = (math.radians(25), 0, 0)
    )
    base.cut_cube(
       target=support,
       scale=(CM4_WIDTH, 20, 80),
       location=(0, -BASE_PLATE_HEIGHT, 24),
       rotation = (math.radians(-75), 0, 0)
    )
    return support

#### ----------------------------------------------------------------------------------------------------------------

main = base.create_cube(scale=(248, 16, 3.5), location=(0, 0, 3.5/2))

X = 248/2 - 7.5

### ----------------------------------------------------------------------------------------------------------------

base.join(target=main, obj=create_support(4, 7.5, -X))
base.join(target=main, obj=create_support(-4, -7.5, X))
base.cut_cube(
   target=main,
   scale=(348, 16, 3.5),
   location=(0, 0, -3.5/2)
)

### ----------------------------------------------------------------------------------------------------------------

for i, (x) in enumerate([X, -X]):
    plate = create_hexagonal_plate()
    plate.location[0] = x
    base.join(target=main, obj=plate)
    support = create_support2()
    support.location[0] = x
    base.join(target=main, obj=support)

main.rotation_euler[2] = math.radians(-45)
