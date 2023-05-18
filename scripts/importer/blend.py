import bpy
import os, sys
from inspect import stack
from logging import getLogger

root_logger_name = os.path.splitext(os.path.basename(stack()[-2].filename))[0]
module_logger_name = f'{root_logger_name}.importer.blend'
module_logger = getLogger(module_logger_name)

from utils import validate_path, get_ext, get_filename_without_ext


def append_to_scene(
        data: bpy.types.BlendData, 
        scene: bpy.types.Scene,
        directory: str, 
        file_name: str
    ) -> None:
    directory = os.path.abspath(directory)
    path_valid = validate_path(directory, file_name, "blend")

    if path_valid.get("error"):
        module_logger.error(path_valid["error"])
        sys.exit()

    if path_valid.get("warn"):
        module_logger.error(path_valid["warn"])
        sys.exit()

    file_path = path_valid.get("path")

    # append object from .blend file
    with data.libraries.load(file_path) as (data_from, data_to):
        data_to.objects = data_from.objects

    # link object to current scene
    for ob in data_to.objects:
        if ob is not None:
            scene.collection.objects.link(ob)

    return 