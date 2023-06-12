# blender model processing tool

## set up avatar

### overview

-   Set up and export humanoid type 3d model, meshed and bones, animations, materials, meta(export vrm only) by setting
-   And generate thumbnail.png

### How to use

1.  prepare 3d model and texture

    -   specification of 3d mode
        -   humanoid type
        -   single armature
        -   file extension: fbx, gltf, glb, vrm
    -   all 3d model and textures should be in the same directory

2.  edit setting.json

    -   detail below

3.  run

    -   in command line, navigate to the directory
    -   run below  
         ..\resources\blender-3.3.2-windows-x64\blender --background --python setup_avatar.py

4.  command line arguments  
    if use command line arguments, set "--" before arguments.  
    ex. ..\resources\blender-3.3.2-windows-x64\blender --background --python setup_avatar.py -- --export_exts vrm glb --create_thumbnail true
    | argument | value | required | explain |
    | ---- | ---- | ---- | ---- |
    | --export_exts | vrm glb gltf fbx | not required | export to other extension file |
    | --create_thumbnail | true or false | not required | create thumbnail image |

## set up measurement

### overviewer

-   adjust and convert measurement.obj to `FBX`, `OBJ`, `GLB`, `GLTF`
-   craete `measurement_for_viewer.fbx`

### how to use

1.  input file

    -   measurement.obj
    -   measurement.json

2.  edit setting
    edit `settings/measurement_settings.json`  
    Enter the directory where the input 3D model is stored in `common/working_dir`

3.  run

    -   in command line, navigate to the root directory
    -   run below  
         ..\resources\blender-3.3.2-windows-x64\blender --background --python setup_measurement.py -- --export_exts `fileextension` --create_viewerfbx `true` or `false`  
        ex. `..\resources\blender-3.3.2-windows-x64\blender --background --python setup_avatar.py -- --export_exts glb --create_thumbnail true`

    | argument             | value            | required     | explain                                                   |
    | -------------------- | ---------------- | ------------ | --------------------------------------------------------- |
    | `--export_exts`      | vrm glb gltf fbx | not required | export to other extension file                            |
    | `--create_viewerfbx` | true or false    | not required | create adjusted mesurement 3D model with landmark objects |

## dependencies

-   [blender 3.3.2](https://www.blender.org/download/release/Blender3.3/blender-3.3.2-windows-x64.zip)
-   [VRM Add-on for Blender 2.14.3](https://github.com/saturday06/VRM-Addon-for-Blender/releases/download/2_14_3/VRM_Addon_for_Blender-2_14_3.zip)
