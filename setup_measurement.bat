cd /D %~dp0
cd scripts

..\resources\blender-3.3.2-windows-x64\blender --python setup_measurement.py

pause

exit