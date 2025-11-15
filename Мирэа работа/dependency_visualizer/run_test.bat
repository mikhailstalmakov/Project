@echo off
echo ========================================
echo Testing Dependency Visualizer
echo ========================================
echo.

echo Test 1: Configuration and Direct Dependencies
echo ----------------------------------------
python main.py config_test.xml
echo.
echo Press any key to continue...
pause >nul

echo.
echo Test 2: With Filtering
echo ----------------------------------------
python main.py config_test_filter.xml
echo.
echo Press any key to continue...
pause >nul

echo.
echo Test 3: Reverse Dependencies
echo ----------------------------------------
python main.py config_test.xml --reverse E
echo.
echo Press any key to continue...
pause >nul

echo.
echo Test 4: Real Package from PyPI (requests)
echo ----------------------------------------
python main.py config.xml
echo.
echo All tests completed!
pause

