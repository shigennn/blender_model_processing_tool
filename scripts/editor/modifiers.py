import bpy
import os
from typing import Optional
from inspect import stack
from logging import getLogger

root_logger_name = os.path.splitext(os.path.basename(stack()[-2].filename))[0]
module_logger_name = f'{root_logger_name}.editor.modifiers'
module_logger = getLogger(module_logger_name)

# add smooth modifier to object
def add_smooth_mod(object: bpy.types.Object, factor: float = 0.5, iterations: int = 1) -> bpy.types.SmoothModifier:
    smooth_mod = object.modifiers.new('Smooth', 'SMOOTH')

    smooth_mod.factor = factor
    smooth_mod.iterations = iterations

    return smooth_mod