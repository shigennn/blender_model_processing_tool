# 課題： materialはmaterials collenctionベースで探索するようにしたい
# 課題： material, set texture path, 拡張子による識別
import bpy
import json, os
from logging import DEBUG, INFO
import random

# load external module
from sys import path
path.append(os.path.basename(bpy.data.filepath))
from utils import get_root_logger, get_cmdarg
from editor import initialize, Material
from importer import import_model, append_to_scene
from exporter import export_model
from human import Avatar, HumanoidAnimation
from vrm import Vrm
from capture import generate_vrm_fullbody_thumbnail, generate_vrm_movie


def main() -> None:
    logger = get_root_logger(__file__, INFO)
    logger.info("Process start.")

    context = bpy.context
    data = bpy.data

    initialize(data)

    # read settings file
    with open('../settings/settings.json', mode='r') as f :
        settings = json.load(f)
    common = settings["common"]
    working_dir = os.path.abspath(common["working_dir"])
    file_name = common["file_name"]
    export_file_name = common["export_file_name"]
    thumbnail_file_name = common["thumbnail_file_name"]
    thumbnail_animation_file = common["thumbnail_animation_file"]

    # import
    import_model(working_dir, file_name)

    # search and set avatar, pose
    avatar = Avatar(context, data)
    avatar.adapt_actions(data.actions)

    # set materials
    materials = settings["materials"]
    for material in materials:
        name = material["name"]
        setting = material["setting"]
        mat = data.materials.get(name)
        if not mat:
            logger.error(f'Material not found. | material name: {name}')
            continue
        material = Material(mat)
        material.texture_dir = working_dir
        material.setting(setting)
        material.create()
        material = None

    # vrm settings / need for thumbnail
    vrm = Vrm(avatar)
    vrm_setting = settings["vrm"]
    vrm.set_meta(vrm_setting)
    vrm.bone_mapping(os.path.abspath("../settings/bone_mapper.json"))
    vrm_blendshapes = settings.get("vrm_blendshapes")
    if vrm_blendshapes:
        vrm.set_blendshape(context, vrm_blendshapes["mesh"], vrm_blendshapes["settings"])
    

    # export model
    export_exts = get_cmdarg('export_exts')
    for ext in export_exts:
        avatar.reset_pose()
        export_model(working_dir, export_file_name, ext)
        logger.info(f'{ext.upper()} created.')

    # thumbnail
    create_thumbnail = get_cmdarg('create_thumbnail')
    if create_thumbnail:
        # create humanoid animation
        animation_file_path = os.path.join("../resources/assets/animations/", thumbnail_animation_file)
        with open(animation_file_path, "r") as f:
            pose = json.load(f)
        animation = HumanoidAnimation(pose)

        # take thumbnail with normalized vrm pose
        generate_vrm_fullbody_thumbnail(
            context= context,
            target_vrm= vrm,
            humanoid_animation= animation,
            save_path= working_dir,
            file_name= thumbnail_file_name,
            # background_color= (252, 252, 252, 0),
            thumbnail_width_px= 1000,
            thumbnail_height_px= 1334,
            is_transparent= True,
        )
        logger.info("Thumbnail created.")


    # create_movie = get_cmdarg('create_movie')
    # if create_movie:

    #     with open('../settings/movie_configs.json', "r") as f:
    #         movie_configs = json.load(f)

    #     # pick up random scene
    #     scene = random.choice(movie_configs["scenes"])
    #     asset_dir = movie_configs["asset_dir"]
        
    #     # create_vrm_movie(data, context, scene)

    #     # title = scene["title"]
    #     # blend_file = scene["blend_file"]
    #     # animation_clip = scene["animation_clip"]
    #     # start_frame = scene["start_frame"]
    #     # end_frame = scene["end_frame"]
    #     # fps = scene["fps"]

    #     '''test under construnction'''    
    #     # append scene
    #     append_to_scene(data, context.scene, "../resources/assets/scenes", "test2.blend")

    #     # take thumbnail with normalized vrm pose
    #     generate_vrm_movie(
    #         context= context,
    #         target_vrm= vrm,
    #         humanoid_animation= animation,
    #         save_path= working_dir,
    #         file_name= "test",
    #         is_transparent= False,
    #         camera= context.scene.objects["Camera"],
    #         start_frame = 0,
    #         end_frame = 70,
    #         frame_step = 1,
    #         fps = 30,
    #     )
    #     logger.info("Movie created.")
    #     '''test under construnction'''    


    logger.info("Process end.")



if __name__ == '__main__':
    main()