@echo off
chcp 65001 >nul
echo ========================================
echo   HabitBloom 一键打包（无需 Linux）
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
echo 选择打包方式：
echo.
echo 1. Docker 打包（需要安装 Docker Desktop）
echo 2. GitHub Actions 云端打包（完全免费，无需安装）
echo.

set /p choice=请选择 [1/2]: 

if "%choice%"=="1" (
    echo.
    echo 🐳 使用 Docker 打包...
    python docker_build.py
) else if "%choice%"=="2" (
    echo.
    echo ☁️  设置 GitHub Actions 云端打包...
    python github_actions_build.py
) else (
    echo.
    echo 显示所有选项...
    python 云端打包.py
)

echo.
pause
