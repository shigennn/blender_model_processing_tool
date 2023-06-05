# blender model processing tool

## Overview

Set up and export humanoid type 3d model, meshed and bones, animations, materials, meta(export vrm only) by setting  
And generate thumbnail.png

## How to use

1.  prepare 3d model and texture

    -   specification of 3d mode
        -   humanoid type
        -   single armature
        -   file extension: fbx, gltf, glb, vrm
    -   all 3d model and textures should be in the same directory

    <br>

2.  edit setting.json

    -   detail below

    <br>

3.  run

    -   in command line, navigate to the directory "/setup_avatar/scripts/"
    -   run below  
         ..\resources\blender-3.3.2-windows-x64\blender --background --python setup_avatar.py

    <br>

4.  command line arguments  
    if use command line arguments, set "--" before arguments.  
    ex) ..\resources\blender-3.3.2-windows-x64\blender --background --python setup_avatar.py -- --export_exts vrm glb --create_thumbnail true
    | argument | value | required | explain |
    | ---- | ---- | ---- | ---- |
    | --export_exts | vrm glb gltf fbx | not required | export to other extension file |
    | --create_thumbnail | true or false | not required | create thumbnail image |
    <br>

## setting.json

1. settings.json
   | key | value | required |
   | ---- | ---- | ---- |
   | common | object, common setting | required |
   | materials | array of material(object) | required |
   | vrm | object, vrm meta setting | if set "vrm" export_exts, required |
   | vrm_blendshapes | object, vrm blendshape setting | if set "vrm" export_exts, required |

 <br>

2. settings.json -> common
   | key | value | required |
   | ---- | ---- | ---- |
   | working_dir | string, directory of 3d model and textures(absolute, realtive) | required |
   | file_name | string, filename of 3d model with extension | required |
   | export_filename | string, filename of export avatar data without extensions | required |
   | thumbnail_file_name | string | required |
   | thumbnail_animation_file | string, animation json file name for thumbnail capture @resources/assets/animations | required |

 <br>

3. settings.json -> material
   | key | value | required |
   | ---- | ---- | ---- |
   | name | string, material name of 3d model | required |
   | settting | object, material setting | required |

 <br>

4. settings.json -> material -> setting
   | key | value | required |
   | ---- | ---- | ---- |
   | shader | string, shader name / STANDARD, UNLIT | required |
   | basecolor_tex | string, file name of basecolor texture | required |
   | normal_tex | string, file name of normal map | not required |
   | roughness_tex | string, file name of roughness map | not required |
   | emission_tex | string, file name of emission map | not required |
   | metallic_param | float, metallic parameter of STANDARD SHADER | STANDARD: required, UNLIT: not required |
   | roughness_param | float, roughness parameter of STANDARD SHADER | STANDARD: required, UNLIT: not required |
   | emission_param | float, emission parameter of STANDARD SHADER | STANDARD: required, UNLIT: not required |
   | blend_method | string, name of blend method / OPAQUE, BLEND, CLIP | required |

 <br>

5. settings.json -> vrm
   | key | value | required |
   | ---- | ---- | ---- |
   | title | string, Title of vrm meta | required |
   | version | string, version of vrm meta | required |
   | author | string, author of vrm meta | required |
   | first_person_bone | string, name of first person bone | not required |
   | first_person_offset | array of float, coodinate of first person offset | not required |
   | look_at_type | string, name of look at type / BlendShape, Bone | not required |

 <br>

6. settings.json -> vrm_blendshape
   | key | value | required |
   | ---- | ---- | ---- |
   | mesh | string, name of mesh type object has blendshape | not required |
   | settings | object, preset names and blendshape names | not required |

 <br>

7. settings.json -> vrm_blendshape -> settings
   | key | value | required |
   | ---- | ---- | ---- |
   | a | string, blendshape name | not required |
   | i | string, blendshape name | not required |
   | u | string, blendshape name | not required |
   | e | string, blendshape name | not required |
   | o | string, blendshape name | not required |
   | blink | string, blendshape name | not required |
   | blink_l | string, blendshape name | not required |
   | blink_r | string, blendshape name | not required |
   | lookup | string, blendshape name | not required |
   | lookdown | string, blendshape name | not required |
   | lookleft | string, blendshape name | not required |
   | lookright | string, blendshape name | not required |
   | neutral | string, blendshape name | not required |
   | joy | string, blendshape name | not required |
   | angry | string, blendshape name | not required |
   | sorrow | string, blendshape name | not required |
   | fun | string, blendshape name | not required |

 <br>

## dependencies

-   [blender 3.3.2](https://www.blender.org/download/release/Blender3.3/blender-3.3.2-windows-x64.zip)
-   [VRM Add-on for Blender 2.14.3](https://github.com/saturday06/VRM-Addon-for-Blender/releases/download/2_14_3/VRM_Addon_for_Blender-2_14_3.zip)
