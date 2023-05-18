import bpy
import bmesh
import os
from typing import Dict, List, Tuple, Union
from inspect import stack
from logging import getLogger
import math
from mathutils import Vector

from editor import deselect_all

root_logger_name = os.path.splitext(os.path.basename(stack()[-2].filename))[0]
module_logger_name = f'{root_logger_name}.measurement.visualize'
module_logger = getLogger(module_logger_name)


# calculate distance v1 from v2
def distance(v1: Vector, v2: Vector) -> float:
    return math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 + (v1[2] - v2[2])**2)


# create edge object from list of vertices
def create_circular_edges(
    coords: List[Vector], name: str, threshold_distance: float
) -> bpy.types.Object:
    
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(mesh)

    verts = [bm.verts.new(coord) for coord in coords]
    connected_verts = [verts[0]]

    while len(connected_verts) < len(verts):
        current_vert = connected_verts[-1]
        min_distance = float('inf')
        closest_vert = None

        for vert in verts:
            if vert in connected_verts:
                continue

            dist = distance(current_vert.co, vert.co)
            if dist < min_distance:
                min_distance = dist
                closest_vert = vert

        # Check if the distance between the current vertex and the closest vertex is less than the threshold distance
        if min_distance <= threshold_distance:
            connected_verts.append(closest_vert)
        else:
            break

    # Connect the vertices in a circular manner
    for i in range(len(connected_verts)):
        bm.edges.new([connected_verts[i], connected_verts[(i + 1) % len(connected_verts)]])

    # Remove edges longer than the threshold distance
    for edge in bm.edges:
        if edge.calc_length() > threshold_distance:
            bm.edges.remove(edge)

    bmesh.update_edit_mesh(mesh)
    bpy.ops.object.mode_set(mode='OBJECT')

    return obj


# craete measurement tubed curve objects form landmarks dict
def create_measurement_objs_from_landmarks(
        landmarks: Dict[str, List[int|float]],
        visualize_points: Union[None, Tuple[str]],
        scale: int|float = 1,
        threshold_distance: int|float = 1,
        bevel_depth: int|float = 0.002,
) -> List[bpy.types.Object]:

    context = bpy.context
    measurement_objs = list()

    deselect_all(context)

    for point_name, coords_list in landmarks.items():

        if not coords_list:
            continue
        
        if visualize_points:
            if point_name not in visualize_points:
                continue

        # create edge object
        coords = [Vector((coord[0]*scale, -coord[2]*scale, coord[1]*scale)) for coord in coords_list]
        obj = create_circular_edges(coords, point_name, threshold_distance)

        # edge object convert to curve and tube
        obj.select_set(True)
        bpy.ops.object.convert(target='CURVE')
        context.object.data.bevel_depth = bevel_depth
        bpy.ops.object.shade_smooth()
        obj.select_set(False)
        measurement_objs.append(obj)


    return measurement_objs