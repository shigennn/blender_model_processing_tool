import os
from inspect import stack
from logging import getLogger
from human import HumanoidBoneName

root_logger_name = os.path.splitext(os.path.basename(stack()[-2].filename))[0]
# module_logger_name = f'{root_logger_name}.human.humanoid_animation'
# module_logger = getLogger(module_logger_name)

REQUIRED_KEYS = {"name", "isLoopAnimation", "fps", "boneAnimations", "hipsPosAnimation", "rootPosition", "rootRotation"}

class HumanoidAnimation:
    def __init__(self, clip: dict) -> None:
        self._logger_name = f'{root_logger_name}.{self.__module__}'
        self._logger = getLogger(self._logger_name)

        self.clip = clip
        if not self._validate(clip):
            self.clip = REST_POSE
            self._logger.warning('Rest pose be set intead.')
        else:
            self._logger.debug(f'Humanoid animation "{clip["name"]}" is created.')


    def _validate_key(self, key_name: str, validate_func, *args) -> bool:
        key_value = self.clip.get(key_name, {})
        if not validate_func(key_name, key_value, *args):
            self._logger.warning(f'Validate humanoid animation error, Invalid value. | key: {key_name}, value: {key_value}')
            return False
        return True


    def _validate(self, clip: dict) -> bool:
        if not all(required_key in clip for required_key in REQUIRED_KEYS):
            self._logger.warning(f'Validate humanoid animation error, Required key not exist. | required keys: {REQUIRED_KEYS}')
            return False

        if not all([
            self._validate_key("name", lambda key, val: isinstance(val, str)),
            self._validate_key("isLoopAnimation", lambda key, val: isinstance(val, bool)),
            self._validate_key("fps", lambda key, val: isinstance(val, int) and val > 0),
            self._validate_key("boneAnimations", self._validate_bone_rotation_animations),
            self._validate_key("hipsPosAnimation", self._validate_root_position_animation),
            self._validate_key("rootPosition", self._validate_root_position_animation),
            self._validate_key("rootRotation", self._validate_root_rotation_animation),
        ]):
            return False

        return True


    def _validate_bone_rotation_animations(self, animation_name: str, animation_data: list) -> bool:
        if not isinstance(animation_data, list):
            # self._logger.warning(f'Validate humanoid animation error, Animation data should be list type. | name: {animation_name}, data type: {type(animation_data)}')
            return False

        for anim in animation_data:
            if not isinstance(anim, dict) or set(anim.keys()) != {"name", "keys"} or not isinstance(anim["name"], str) or not self._validate_keys(anim["keys"], 5):
                # self._logger.warning(f'Validate humanoid animation error, | animation name: {animation_name}, bone name: {anim["name"]}, key0: {anim["keys"][0]}')
                return False
            if not HumanoidBoneName.match_humanoid_bone_name(anim["name"]):
                return False
            
        return True


    def _validate_root_rotation_animation(self, animation_name: str, animation_data: dict):
        if not isinstance(animation_data, dict) or set(animation_data.keys()) != {"name", "keys"} or not isinstance(animation_data["name"], str) or not self._validate_keys(animation_data["keys"], 5):
            # self._logger.warning(f'Validate humanoid animation error, | animation name: {animation_name}, bone name: {animation_data["name"]}, key0: {animation_data["keys"][0]}')
            return False
        return True


    def _validate_root_position_animation(self, animation_name: str, animation_data: dict):
        if not isinstance(animation_data, dict) or set(animation_data.keys()) != {"name", "keys"} or not isinstance(animation_data["name"], str) or not self._validate_keys(animation_data["keys"], 4):
            # self._logger.warning(f'Validate humanoid animation error, | animation name: {animation_name}, bone name: {animation_data["name"]}, key0: {animation_data["keys"][0]}')
            return False
        return True


    def _validate_keys(self, keys, key_length):
        if not isinstance(keys, list):
            return False

        for key in keys:
            if not isinstance(key, list) or len(key) != key_length or not all(isinstance(v, int|float) for v in key):
                return False

        return True


# default rest pose
REST_POSE = {
    "name": "rest pose", 
    "isLoopAnimation": False, 
    "fps": 30, 
    "boneAnimations": [
        {
            "name": "hips", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "spine",
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "chest", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "upperChest", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "neck", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "head", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftUpperLeg", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftLowerLeg", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftFoot", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftToes", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightUpperLeg", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightLowerLeg", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightFoot", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightToes", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftShoulder", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftUpperArm", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftLowerArm", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftHand", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightShoulder", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightUpperArm", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightLowerArm", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightHand", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightThumbProximal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightThumbIntermediate", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightThumbDistal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightIndexProximal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightIndexIntermediate", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightIndexDistal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightMiddleProximal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightMiddleIntermediate", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightMiddleDistal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightRingProximal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightRingIntermediate", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightRingDistal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightLittleProximal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightLittleIntermediate", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "rightLittleDistal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftThumbProximal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftThumbIntermediate", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftThumbDistal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftIndexProximal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftIndexIntermediate", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftIndexDistal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftMiddleProximal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftMiddleIntermediate", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftMiddleDistal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftRingProximal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftRingIntermediate", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftRingDistal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftLittleProximal", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftLittleIntermediate", 
            "keys": [[0,1,0,0,0]]
        }, 
        {
            "name": "leftLittleDistal", 
            "keys": [[0,1,0,0,0]]
        }
    ], 
    "hipsPosAnimation": 
    {
        "name": "hips", 
        "keys": [[0,0,0,0]]
    }, 
    "rootPosition": 
    {
        "name": "rootPosition", 
        "keys": [
            [0,0,0,0]
        ]
    }, 
    "rootRotation": 
    {
        "name": "rootRotation", 
        "keys": [
            [0,1,0,0,0]
        ]
    }
}