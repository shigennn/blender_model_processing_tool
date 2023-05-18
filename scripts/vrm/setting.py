import bpy
import os, json
from typing import Set, List
from inspect import stack
from logging import getLogger

from human import HumanoidBoneName, Avatar
from editor import has_blendshape, get_mesh_obj_by_name

root_logger_name = os.path.splitext(os.path.basename(stack()[-2].filename))[0]
# module_logger_name = f'{root_logger_name}.vrm.setting'
# module_logger = getLogger(module_logger_name)


LOOK_AT_TYPE = (
    'Bone',
    'BlendShape',
)

class Vrm:
    def __init__(self, avatar: Avatar) -> None:
        self._logger_name = f'{root_logger_name}.{self.__module__}'
        self._logger = getLogger(self._logger_name)

        if not isinstance(avatar, Avatar):
            self._logger.error(f'Args avatar should be class Avatar. | type: {type(avatar)}')

        self.avatar: Avatar = avatar
        self.armature: bpy.types.Object = self.avatar.armature
        self.title: str = 'title'
        self.version: str = '1.0'
        self.author: str = 'author'
        self.allowed_user_name: str = 'OnlyAuthor'
        self.violent_ussage_name: str = 'Disallow'
        self.sexual_ussage_name: str = 'Disallow'
        self.commercial_ussage_name: str = 'Disallow'
        self.license_name: str = 'Redistribution_Prohibited'
        self.first_person_bone: str = HumanoidBoneName.HEAD
        self.first_person_offset: List[int] = [0, 0, 0]
        self.look_at_type: str = 'BlendShape'

        self.vrm_version: str = '0.0'
        self.armature.data.vrm_addon_extension.spec_version = self.vrm_version
        self.vrm0 = self.armature.data.vrm_addon_extension.vrm0

        # set humanoid_bone
        for humanoid_bone in HumanoidBoneName:
            human_bone0 = self.vrm0.humanoid.human_bones.add()
            human_bone0.bone = humanoid_bone.value
        
        self.is_bonemapped = False


    """ set vrm meta from setting dict """
    def set_meta(self, vrm_setting: dict) -> None:
        title = vrm_setting.get('title')
        version = vrm_setting.get('version')
        author = vrm_setting.get('author')
        first_person_bone = vrm_setting.get('first_person_bone')
        first_person_offset = vrm_setting.get('first_person_offset')
        look_at_type = vrm_setting.get('look_at_type')

        # set title
        if isinstance(title, str):
            self.title = title
        else:
            self._logger.warning(f'Set VRM meta title canceled. VRM meta title must be string. | title: {title}')
        self.vrm0.meta.title = self.title

        # set version
        if isinstance(version, str):
            self.version = version
        else:
            self._logger.warning(f'Set VRM meta version canceled. VRM meta version must be string. | version: {version}')
        self.vrm0.meta.version = self.version

        # set author
        if isinstance(author, str):
            self.author = author
        else:
            self._logger.warning(f'Set VRM meta author canceled. VRM meta author must be string. | author: {author}')
        self.vrm0.meta.author = self.author

        # set rights
        self.vrm0.meta.allowed_user_name = self.allowed_user_name
        self.vrm0.meta.violent_ussage_name = self.violent_ussage_name
        self.vrm0.meta.sexual_ussage_name = self.sexual_ussage_name
        self.vrm0.meta.commercial_ussage_name = self.commercial_ussage_name
        self.vrm0.meta.license_name = self.license_name

        # first person bone
        if HumanoidBoneName.match_humanoid_bone_name(first_person_bone):
            self.first_person_bone = first_person_bone
        else:
            self._logger.warning(f'Set VRM first person bone canceled. VRM first person bone must be HumanoidBoneName. | first_person_bone: {first_person_bone}')
        self.vrm0.first_person.first_person_bone.value = self.first_person_bone

        # first person offset
        is_correct = True
        if not isinstance(first_person_offset, list) and is_correct:
            msg = f'Set VRM meta first_person_offset canceled. first_person_offset must be List[float, float, float]. | first_person_offset: {first_person_offset}'
            is_correct = False
        if not len(first_person_offset) == 3 and is_correct:
            msg = f'Set VRM meta first_person_offset canceled. first_person_offset must be List[float, float, float]. | first_person_offset: {first_person_offset}'
            is_correct = False
        if not all([isinstance(x, float) for x in first_person_offset]) and is_correct:
            msg = f'Set VRM meta first_person_offset canceled. first_person_offset must be List[float, float, float]. | first_person_offset: {first_person_offset}'
            is_correct = False

        if is_correct:
            self.first_person_offset = first_person_offset
        else:
            self._logger.warning(msg)

        self.vrm0.first_person.first_person_bone_offset = self.first_person_offset

        # set look at type
        if look_at_type in LOOK_AT_TYPE:
            self.look_at_type = look_at_type
        else:
            self._logger.warning(f'Set VRM look_at_type canceled. look_at_type must be {[x for x in LOOK_AT_TYPE]}. | look_at_type: {look_at_type}')
        
        self.vrm0.first_person.look_at_type_name = self.look_at_type

        return


    """ vrm humanoid bone mapping """
    def bone_mapping(self, filepath: str) -> Set[str]:
        if not os.path.exists(filepath):
            self._logger.warning(f'File does not exist. | filepath: {filepath}')
            return

        with open(filepath, "rb") as file:
            mapper = json.load(file)
        if not isinstance(mapper, dict):
            self._logger.warning(f'File mest be JSON. | filepath: {filepath}')
            return

        for human_bone_name, bpy_bone_name in mapper.items():
            if human_bone_name not in [hb.value for hb in HumanoidBoneName]:
                continue

            found = False
            for human_bone in self.vrm0.humanoid.human_bones:
                if human_bone.bone == human_bone_name:
                    human_bone.node.value = bpy_bone_name
                    found = True
                    break
            if found:
                continue

            human_bone = self.vrm0.humanoid.human_bones.add()
            human_bone.bone = human_bone_name
            human_bone.node.value = bpy_bone_name
        
        self.is_bonemapped = True
        self._logger.debug(f'VRM humanoid bone mapping end.')
        
        return


    """ vrm blendshape setting """
    def set_blendshape(self, context: bpy.types.Context, mesh_name: str, settings: dict) -> None:
        mesh = get_mesh_obj_by_name(context, mesh_name)
        if not mesh:
            self._logger.error(f'MESH type Object does not exist. | object name: {mesh_name}')
            return
        if not has_blendshape(mesh):
            self._logger.error(f'Object does not have blendshape. | object name: {mesh_name}')
            return

        for preset, bsname in settings.items():
            group = self.vrm0.blend_shape_master.blend_shape_groups.add()
            bind = group.binds.add()
            bind.weight = 1
            group.name = preset

            try:
                group.preset_name = preset
            except TypeError:
                self._logger.warning(f'VRM blendshape preset not found. | preset name: {preset}')
                continue

            bind.mesh.value = mesh_name

            data_mesh = context.scene.objects[mesh_name].data
            shape_keys = data_mesh.shape_keys.key_blocks.keys()
            if bsname in shape_keys:
                bind.index = bsname
            else:
                self._logger.warning(f'Shapekey not found. | preset name: {preset}, blendshape name: {bsname}')
        self._logger.debug(f'VRM blendshape setting end.')

        return