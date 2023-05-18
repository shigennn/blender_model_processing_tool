import os
import bpy
import mathutils
from inspect import stack
from logging import getLogger

from editor import posemode, objectmode
from human import Avatar, HumanoidAnimation
from vrm import Vrm

root_logger_name = os.path.splitext(os.path.basename(stack()[-2].filename))[0]
# module_logger_name = f'{root_logger_name}.vrm.normalized'
# module_logger = getLogger(module_logger_name)

class NormalizedVrm(Avatar):
    def __init__(self, vrm: Vrm) -> None:
        self._logger_name = f'{root_logger_name}.{self.__module__}'
        self._logger = getLogger(self._logger_name)

        if not vrm.is_bonemapped:
            self._logger.error(f'Bone normalized failed. VRM bone mapping is not completed.')
            return
        
        self.armature = vrm.armature
        self.reset_pose()
        self.normalize_bone_axis()

        self.human_bones = self.armature.data.vrm_addon_extension.vrm0.humanoid.human_bones
        
        return
    

    def set_pose(self, humanoid_animation: HumanoidAnimation, frame :int = 0) -> None:
        self._logger.debug(f'Set normalized pose start. | animation name: {humanoid_animation.clip["name"]}, farme: {frame}')

        bone_animations = humanoid_animation.clip["boneAnimations"]
        hips_position = humanoid_animation.clip["hipsPosAnimation"]["keys"][0][1:]
        root_position = humanoid_animation.clip["rootPosition"]["keys"][0][1:]
        root_rotation = humanoid_animation.clip["rootRotation"]["keys"][0][1:]

        # set armature
        self.armature.location = root_position
        self.armature.rotation_mode = 'QUATERNION'
        self.armature.rotation_quaternion = root_rotation

        # set bones pose
        posemode(self.armature)
        for bone_animation in bone_animations:
            humanoid_bone_name = bone_animation["name"]
            keys = bone_animation["keys"]

            for key in keys:
                if key[0] != frame:
                    continue

                pose_rotation_quaternion = key[1:]
            
                for human_bone in self.human_bones:
                    if human_bone.bone != humanoid_bone_name:
                        continue

                    bpy_bone_name = human_bone.node.value
                    posebone = self.armature.pose.bones[bpy_bone_name]
                    posebone.rotation_mode = 'QUATERNION'
                    posebone.rotation_quaternion = pose_rotation_quaternion

                    if human_bone.bone == "hips":
                        posebone.location = hips_position

        objectmode(self.armature)
        self._logger.debug(f'Set normalized pose end. | animation name: {humanoid_animation.clip["name"]}, farme: {frame}')

        return


    def set_motion(self, humanoid_animation: HumanoidAnimation) -> None:
        self._logger.debug(f'Set normalized motion start. | animation name: {humanoid_animation.clip["name"]}')

        action_name = humanoid_animation.clip["name"]
        bone_animations = humanoid_animation.clip["boneAnimations"]
        hips_position = humanoid_animation.clip["hipsPosAnimation"]["keys"]
        root_position = humanoid_animation.clip["rootPosition"]["keys"][0][1:]
        root_rotation = humanoid_animation.clip["rootRotation"]["keys"][0][1:]

        # Create animation data and action
        if not self.armature.animation_data:
            self.armature.animation_data_create()
        action = bpy.data.actions.new(action_name)
        self._logger.info(f'{self.armature.animation_data},{type(self.armature.animation_data)}')
        self.armature.animation_data.action = action

        # set armature animation keyframe
        self.armature.location = root_position
        self.armature.rotation_quaternion = root_rotation
        self.armature.keyframe_insert(data_path="location", frame=0)
        self.armature.keyframe_insert(data_path="rotation_quaternion", frame=0)

        # set bones pose
        posemode(self.armature)
        for bone_animation in bone_animations:
            humanoid_bone_name = bone_animation["name"]
            keys = bone_animation["keys"]

            for index, key in enumerate(keys):
                frame = key[0]
                rotation_quaternion = mathutils.Quaternion(key[1:])

                for human_bone in self.human_bones:
                    if human_bone.bone != humanoid_bone_name:
                        continue

                    bpy_bone_name = human_bone.node.value
                    posebone = self.armature.pose.bones[bpy_bone_name]

                    # Set bone rotation and insert keyframe for each component of the rotation quaternion
                    posebone.rotation_quaternion = rotation_quaternion
                    for i in range(4):
                        fcurve_data_path = f'pose.bones["{bpy_bone_name}"].rotation_quaternion'
                        self.armature.keyframe_insert(data_path=fcurve_data_path, frame=frame, index=i)

                    # Set hips locatin and insert keyframe
                    if human_bone.bone == 'hips':
                        posebone.location = hips_position[index][1:]

                        for i in range(3):
                            fcurve_data_path = f'pose.bones["{bpy_bone_name}"].location'
                            self.armature.keyframe_insert(data_path=fcurve_data_path, frame=frame, index=i)


        objectmode(self.armature)
        self._logger.debug(f'Set normalized motion end. | animation name: {humanoid_animation.clip["name"]}')

        return