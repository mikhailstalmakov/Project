@echo off
cd /d "%~dp0"
echo Запуск программы...
echo.
py dependency_visualizer\depvis_stage1.py -c test_config.xml
echo.
pause

