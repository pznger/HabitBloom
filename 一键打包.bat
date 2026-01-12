@echo off
chcp 65001 >nul
echo ========================================
echo   HabitBloom 一键打包工具
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python 已安装
echo.
echo 🚀 开始自动打包...
echo.

REM 运行 Python 脚本
python auto_build.py

echo.
pause
