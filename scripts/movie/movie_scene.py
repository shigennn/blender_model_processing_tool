import os
from typing import List, Optional
from inspect import stack
from logging import getLogger

root_logger_name = os.path.splitext(os.path.basename(stack()[-2].filename))[0]
module_logger_name = f'{root_logger_name}.editor.material'
module_logger = getLogger(module_logger_name)


class Scene:
    REQUIRED_KEYS = {
        "title": str,
        "blend_file": str,
        "animation_clip": str,
        "start_frame": int,
        "end_frame": int,
        "fps": int
    }

    def __init__(self, scene_object: dict):
        self._logger_name = f'{root_logger_name}.{self.__module__}'
        self._logger = getLogger(self._logger_name)

        self.scene_object = scene_object
        self.validated = self.validate()

    def validate(self):
        for key, value_type in self.REQUIRED_KEYS.items():
            value = self.scene_object.get(key)
            if value is None:
                self._logger.error(f"{key} key must be present in the scene_object.")
                return False
            if not isinstance(value, value_type):
                self._logger.error(f"{key} must be of type {value_type.__name__}.")
                return False

        if not self.scene_object["blend_file"].endswith(".blend"):
            self._logger.error("blend_file must end with '.blend'.")
            return False
        if not self.scene_object["animation_clip"].endswith(".json"):
            self._logger.error("animation_clip must end with '.json'.")
            return False

        return True