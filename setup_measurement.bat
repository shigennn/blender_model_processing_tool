cd /D %~dp0
cd scripts

..\resources\blender-3.3.2-windows-x64\blender --background --python setup_measurement.py -- --export_exts glb --create_viewerfbx true

pause

exit