import bpy
import os
from inspect import stack
from logging import getLogger
from typing import Tuple
from human import HumanoidAnimation
from editor import World
from capture import CaptureCamera
from vrm import Vrm, NormalizedVrm

root_logger_name = os.path.splitext(os.path.basename(stack()[-2].filename))[0]
module_logger_name = f'{root_logger_name}.capture.avatar_thumbnail'
module_logger = getLogger(module_logger_name)


def generate_vrm_fullbody_thumbnail(
        context: bpy.types.Context,
        target_vrm: Vrm,
        humanoid_animation: HumanoidAnimation,
        save_path: str,
        file_name: str,
        background_color: Tuple[int] = (255, 255, 255, 0),
        thumbnail_width_px: int = 1080,
        thumbnail_height_px: int = 1920,
        is_transparent: bool = False
    ):
    module_logger.debug(f'Take vrm fullbody thumbnail start.')
    
    # make pose
    normalized_vrm = NormalizedVrm(target_vrm)
    normalized_vrm.set_pose(humanoid_animation, 0)

    # set world / background
    world = World()
    world.solid_color(background_color)

    # capture
    capture_camera = CaptureCamera(context.scene)
    capture_camera.fit_to_avatar_fullbody(target_vrm.avatar, thumbnail_width_px, thumbnail_height_px)
    capture_camera.take_eevee_snapshot(save_path, file_name, is_transparent)
    capture_camera.delete()

    module_logger.debug(f'Take vrm fullbody thumbnail end.')
    return


def generate_vrm_movie(
        context: bpy.types.Context,
        target_vrm: Vrm,
        humanoid_animation: HumanoidAnimation,
        save_path: str,
        file_name: str,
        background_color: Tuple[int] = (255, 255, 255, 0),
        movie_width_px: int = 1080,
        movie_height_px: int = 1920,
        is_transparent: bool = False,
        camera: bpy.types.Object = None,
        start_frame: int = 0,
        end_frame: int = 120,
        frame_step: int = 1,
        fps: int = 30,
    ):
    module_logger.debug(f'Take vrm movie start.')
    
    # make pose
    normalized_vrm = NormalizedVrm(target_vrm)
    normalized_vrm.set_motion(humanoid_animation)

    # capture
    capture_camera = CaptureCamera(context.scene, camera)
    capture_camera.take_movie(
        file_path= save_path, 
        file_name= file_name, 
        start_frame= start_frame,
        end_frame= end_frame,
        frame_step= frame_step,
        fps= fps,
        is_transparent= is_transparent
    )
    # capture_camera.delete()

    module_logger.debug(f'Take vrm movie end.')
    return