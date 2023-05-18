import bpy
import os, math
from typing import Tuple
from inspect import stack
from logging import getLogger

from utils import to_vector_rgb
from human import Avatar
from editor import create_camera

root_logger_name = os.path.splitext(os.path.basename(stack()[-2].filename))[0]
# module_logger_name = f'{root_logger_name}.capture.capture'
# module_logger = getLogger(module_logger_name)


class CaptureCamera:
    def __init__(self, scene: bpy.types.Scene, camera: bpy.types.Object = None) -> None:
        self._logger_name = f'{root_logger_name}.{self.__module__}'
        self._logger = getLogger(self._logger_name)
        self.render = scene.render

        if camera:
            self.camera = camera
        else:
             self.camera = create_camera("CaptureCamera", (0, 0, 0), (90, 0, 0), 50)

        # for render, should set the scene.camera after add new camera
        # if not set it, should use render('INVOKE_DEFAULT')
        scene.camera = self.camera

    
    # delete created camera data and object    
    def delete(self):
        bpy.data.cameras.remove(self.camera.data)
        return


    def fit_to_avatar_fullbody(self, target_avatar: Avatar, image_width: int|float, image_height: int|float) -> None:
        # adjuster 
        CAPTURE_HEIGHT_FACTOR = 0.62
        CAPTURE_LENGTH_FACTOR = 0.95
        DEFAULT_FOV = 35
        CAMERA_ANGLE = 87
        
        avatar_height = target_avatar.bounds_size["height"]
        aspect_ratio = image_width / image_height
        
        # caliculate
        sensor_width = avatar_height * aspect_ratio
        horizontal_fov = math.radians(DEFAULT_FOV)
        focal_length = sensor_width / (2 * math.tan(horizontal_fov / 2))

        # update camera settings
        self.camera.location.y = - (avatar_height * CAPTURE_HEIGHT_FACTOR * CAPTURE_LENGTH_FACTOR) / math.tan(horizontal_fov / 2)
        self.camera.location.z = avatar_height * CAPTURE_HEIGHT_FACTOR
        self.camera.rotation_mode = 'XYZ'
        self.camera.rotation_euler = (math.radians(CAMERA_ANGLE), 0, 0)
        self.camera.data.sensor_width = sensor_width
        self.camera.data.lens = focal_length

        # update scene
        self.render.resolution_x = image_width
        self.render.resolution_y = image_height

        return
    

    def take_eevee_snapshot(
        self, 
        file_path: str, 
        file_name: str = 'snapshot', 
        is_transparent: bool = False
    ) -> None:
        context = bpy.context
        self._prepare_shot(context, file_path, file_name, is_transparent)

        # set renderer
        self.render.engine = 'BLENDER_EEVEE'

        # take snapshot single frame
        bpy.ops.render.render(animation = False, write_still = True)

        return
    
    '''under construction'''
    def take_movie(
        self,
        file_path: str,
        file_name: str = "movie",
        start_frame: int = 1,
        end_frame: int = 30,
        frame_step: int = 1,
        fps: int = 30,
        is_transparent: bool = False,
    ) -> None:
        context = bpy.context
        self._prepare_shot(context, file_path, file_name, is_transparent)

        # set renderer
        self.render.engine = 'BLENDER_EEVEE'

        # set output format to movie
        self.render.image_settings.file_format = 'FFMPEG'
        self.render.ffmpeg.format = 'MPEG4'
        self.render.ffmpeg.codec = 'H264'

        # set movie settings
        self.render.fps = fps
        context.scene.frame_start = start_frame
        context.scene.frame_end = end_frame
        context.scene.frame_step = frame_step

        # set file name
        file_extension = ".mp4"
        self.render.filepath = os.path.join(file_path, file_name + file_extension)

        # take movie
        bpy.ops.render.render(animation = True)

        return

    
    def take_snapshot(
        self, 
        file_path: str, 
        file_name: str = 'snapshot', 
        background_color_8bit: Tuple[int] = (255, 255, 255), 
        is_transparent: bool = False
    ) -> None:
        context = bpy.context
        self._prepare_shot(context, file_path, file_name, is_transparent)

        # set scene viewport shading
        space = context.space_data
        space.shading.type = 'SOLID'
        space.overlay.show_overlays = False
        space.shading.background_type = 'VIEWPORT'
        space.shading.background_color = to_vector_rgb(background_color_8bit)

        # take snapshot single frame
        bpy.ops.render.opengl(animation = False, write_still = True)

        return
    
    # !!!underconstruction!!!
    def take_snapshot_with_grid(
        self, 
        file_path: str, 
        file_name: str = 'snapshot', 
        background_color_8bit: Tuple[int] = (255, 255, 255), 
    ) -> None:
        context = bpy.context
        self._prepare_shot(context, file_path, file_name, False)

        # set scene viewport shading
        space = context.space_data
        space.shading.type = 'SOLID'
        space.overlay.show_overlays = True
        space.shading.background_type = 'VIEWPORT'
        space.shading.background_color = to_vector_rgb(background_color_8bit)

        # take snapshot single frame
        bpy.ops.render.opengl(animation = False, write_still = True)

        return
    

    def _prepare_shot(self, context: bpy.types.Context, file_path: str, file_name: str, is_transparent: bool) -> None:
        # activate render camera
        context.view_layer.objects.active = self.camera
        # set render
        self.render.film_transparent = is_transparent
        self.render.image_settings.file_format = 'PNG'
        self.render.filepath = os.path.join(file_path, f'{file_name}.png')

        return