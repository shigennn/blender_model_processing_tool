import bpy
import os, sys
from inspect import stack
from logging import getLogger
from typing import Tuple, List, Dict

root_logger_name = os.path.splitext(os.path.basename(stack()[-2].filename))[0]
module_logger_name = f'{root_logger_name}.human.avatar'
module_logger = getLogger(module_logger_name)

from editor import (
    clean,
    reset_transform_all,
    armature_exists,
    multiple_armatures_exist,
    limit_vertex_weight_total,
    root_bone,
    editmode,
    objectmode,
    posemode,
)


class Avatar:
    def __init__(self, context: bpy.types.Context, data: bpy.types.BlendData) -> None:
        self._logger_name = f'{root_logger_name}.{self.__module__}'
        self._logger = getLogger(self._logger_name)
        
        clean(data)
        reset_transform_all(context)

        # set armature
        self.armature = single_armature(context)

        # get bounds size
        mesh_objects = [obj for obj in context.scene.objects if obj.type == 'MESH']
        self.bounds_size = combined_bounds_size(mesh_objects)

        # adjust number of vertex weight all meshes
        for mesh in mesh_objects:
            limit_vertex_weight_total(context, mesh, 4)

        # reset to rest pose
        self.reset_pose()

        return

    def reset_pose(self, frame: int|float = 0, bake_needs: bool = False) -> None:
        posemode(self.armature)

        bpy.context.scene.frame_set(frame)

        for posebone in self.armature.pose.bones:
            posebone.location = (0, 0, 0)
            posebone.rotation_quaternion = (1, 0, 0, 0)
            posebone.scale = (1, 1, 1)

        objectmode(self.armature)

        return 
    

    def normalize_bone_axis(self):
        # editbones
        editmode(self.armature)
        bones = self.armature.data.edit_bones

        # disconnect all editbones
        for bone in bones:
            bone.use_connect = False
        # normalize
        for bone in bones:
            head = bone.head
            tail_pos = (head[0], head[1], head[2] + 0.1)
            bone.tail = tail_pos
            bone.roll = 0.0

        objectmode(self.armature)
        return


    def adapt_actions(self, actions: bpy.types.bpy_prop_collection) -> None:
        if not actions:
            self._logger.debug(f'No Actions. Adapt actions canceled.')
            return

        if not _is_actions(actions):
            self._logger.error(f'Collection must be "Actions". | collection: {actions}')
            return

        for action in actions:
            # for artem unity animation tool
            if 'Mesh' in action.name or 'mesh' in action.name:
                actions.remove(action)
            else:
                _clean_human_action(self.armature, action)
                _pushdown_action(self.armature, action)

        return


def single_armature(context: bpy.types.Context) -> bpy.types.Object:
    if not armature_exists(context):
        module_logger.error("Armature does not exist.")
        sys.exit()

    if multiple_armatures_exist(context):
        module_logger.error("Multiple armature exist.")
        sys.exit()

    armatures = [obj for obj in context.scene.objects if obj.type == 'ARMATURE']

    return armatures[0]


def combined_bounds_size(mesh_objects: List[bpy.types.Object]) -> Dict[str, int|float]:
    bboxes = [obj.bound_box for obj in mesh_objects]

    combined_bounds = []
    combined_bounds.append([min([bbox[i][0] for bbox in bboxes for i in range(8)]),
                                min([bbox[i][1] for bbox in bboxes for i in range(8)]),
                                min([bbox[i][2] for bbox in bboxes for i in range(8)])])
    combined_bounds.append([max([bbox[i][0] for bbox in bboxes for i in range(8)]),
                                max([bbox[i][1] for bbox in bboxes for i in range(8)]),
                                max([bbox[i][2] for bbox in bboxes for i in range(8)])])

    size = {
        "width": combined_bounds[1][0] - combined_bounds[0][0],
        "depth": combined_bounds[1][1] - combined_bounds[0][1],
        "height": combined_bounds[1][2] - combined_bounds[0][2],
    }
    
    return size


def _is_actions(collection: bpy.types.bpy_prop_collection) -> bool:
    return all(isinstance(data, bpy.types.Action) for data in collection)


def _clean_human_action(armature: bpy.types.Object, action: bpy.types.Action) -> None:
    root_bone_name = root_bone(armature).name  
    for fcurve in action.fcurves:
        if fcurve.data_path.endswith('rotation_quaternion') or fcurve.data_path.endswith(f'[{root_bone_name}].location'):
            continue
        action.fcurves.remove(fcurve)
    return


def _pushdown_action(armature: bpy.types.Object, action: bpy.types.Action) -> None:
    track = armature.animation_data.nla_tracks.new()
    track.strips.new(action.name, int(action.frame_range[0]), action)
    return