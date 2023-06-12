import bpy
import json, os
from logging import DEBUG, INFO

# load external module
from sys import path
path.append(os.path.basename(bpy.data.filepath))
from utils import get_root_logger, get_cmdarg
from editor import initialize, Material, create_and_add_material, add_smooth_mod
from importer import import_model
from exporter import export_model
from measurement import create_measurement_objs_from_landmarks

def main() -> None:
    logger = get_root_logger(__file__, INFO)
    logger.info("Process start.")

    context = bpy.context
    data = bpy.data

    initialize(data)

    # read settings file
    with open('../settings/measurement_settings.json', mode='r') as f :
        settings = json.load(f)
    common = settings["common"]
    working_dir = os.path.abspath(common["working_dir"])
    obj_file_name = common["obj_file_name"]
    export_file_name = common["export_file_name"]
    viewer_file_name = common["viewer_file_name"]
    scale = common["scale"]

    # import and setting body obj
    imported = import_model(working_dir, obj_file_name)
    body_obj = imported[0]
    # rescale
    body_obj.scale = tuple(scale for _ in range(3))
    # set all material -> standard, no texture, roughness = 1.0
    for mat in body_obj.data.materials:
        material = Material(mat)
        material.set_shader('STANDARD')
        material.multiply_color = (0.74, 0.74, 0.74, 1.0)
        material.create()
        material = None

    # export model
    export_exts = get_cmdarg('export_exts')
    for ext in export_exts:
        export_model(working_dir, export_file_name, ext)
        logger.info(f'{ext.upper()} created.')

    # viewer fbx
    create_viewerfbx = get_cmdarg('create_viewerfbx')
    if create_viewerfbx:

        # smoothing
        add_smooth_mod(body_obj, 0.5, 10)

        # landmark object
        measurement = settings["measurement"]
        measurement_file_name = measurement["file_name"]
        visualize = measurement["visualize"]
        
        # read measurement json
        measurement_dir = os.path.join(working_dir, measurement_file_name)
        if os.path.exists(measurement_dir):
            with open(measurement_dir, 'r') as file:
                data = json.load(file)
            landmarks = data["Landmark"]

            # create measurement object
            measurement_objs = create_measurement_objs_from_landmarks(
                landmarks = landmarks,
                visualize_points = list(visualize.keys()),
                scale = scale,
                threshold_distance = 0.1,
                bevel_depth = 0.002,
            )

            # set measurement object color
            for index, obj in enumerate(measurement_objs):
                mat = create_and_add_material(obj, obj.name)
                material = Material(mat)
                material.set_shader('STANDARD')
                material.multiply_color = tuple(visualize[obj.name])
                material.emission_color = tuple(visualize[obj.name])

                material.create()
                material = None

        # export fbx
        export_model(working_dir, viewer_file_name, 'FBX')
        logger.info("Viewer fbx created.")

    logger.info("Process end.")

if __name__ == '__main__':
    main()