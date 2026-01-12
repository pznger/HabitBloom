@echo off
chcp 65001 >nul
echo ============================================================
echo   HabitBloom PyQt5 Android 打包工具
echo ============================================================
echo.

cd /d "%~dp0"

echo 正在检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python 环境正常
echo.

echo 正在安装/更新 Briefcase...
python -m pip install --upgrade briefcase
if errorlevel 1 (
    echo ❌ Briefcase 安装失败
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 开始打包流程
echo ============================================================
echo.

echo 请选择操作:
echo 1. 初始化项目（首次运行）
echo 2. 构建 APK
echo 3. 打包 APK
echo 4. 完整流程（初始化 + 构建 + 打包）
echo.

set /p choice=请输入选项 (1-4): 

if "%choice%"=="1" (
    echo.
    echo 正在初始化 Android 项目...
    briefcase create android
    if errorlevel 1 (
        echo ❌ 初始化失败
        pause
        exit /b 1
    )
    echo ✅ 初始化成功
) else if "%choice%"=="2" (
    echo.
    echo 正在构建 APK...
    briefcase build android
    if errorlevel 1 (
        echo ❌ 构建失败
        pause
        exit /b 1
    )
    echo ✅ 构建成功
) else if "%choice%"=="3" (
    echo.
    echo 正在打包 APK...
    briefcase package android
    if errorlevel 1 (
        echo ❌ 打包失败
        pause
        exit /b 1
    )
    echo ✅ 打包成功
    echo.
    echo APK 文件位置:
    dir /s /b android\*.apk 2>nul
) else if "%choice%"=="4" (
    echo.
    echo 步骤 1/3: 初始化项目...
    briefcase create android
    if errorlevel 1 (
        echo ❌ 初始化失败
        pause
        exit /b 1
    )
    echo.
    echo 步骤 2/3: 构建 APK...
    briefcase build android
    if errorlevel 1 (
        echo ❌ 构建失败
        pause
        exit /b 1
    )
    echo.
    echo 步骤 3/3: 打包 APK...
    briefcase package android
    if errorlevel 1 (
        echo ❌ 打包失败
        pause
        exit /b 1
    )
    echo.
    echo ✅ 完整流程成功！
    echo.
    echo APK 文件位置:
    dir /s /b android\*.apk 2>nul
) else (
    echo ❌ 无效选项
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 完成！
echo ============================================================
pause
