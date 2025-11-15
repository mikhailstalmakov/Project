# Скрипт для проверки работы программы визуализации зависимостей
# Запуск: .\test.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing Dependency Visualizer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Получаем текущую директорию скрипта
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Test 1: Configuration and Direct Dependencies" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
python main.py config_test.xml
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "Test 2: With Filtering" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
python main.py config_test_filter.xml
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "Test 3: Reverse Dependencies" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
python main.py config_test.xml --reverse E
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "Test 4: Real Package from PyPI (requests)" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
python main.py config.xml
Write-Host ""
Write-Host "All tests completed!" -ForegroundColor Green

