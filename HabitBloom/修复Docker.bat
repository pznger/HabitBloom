@echo off
chcp 65001 >nul
echo ========================================
echo   Docker 问题修复助手
echo ========================================
echo.

echo 正在检查 Docker 状态...
docker info >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ Docker 运行正常
    echo.
    pause
    exit /b 0
)

echo ❌ Docker 未运行或未正确配置
echo.

echo 正在尝试启动 Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe" 2>nul
if %errorLevel% equ 0 (
    echo ✅ 已启动 Docker Desktop
    echo.
    echo ⏳ 请等待 30 秒让 Docker 完全启动...
    echo.
    timeout /t 30 /nobreak >nul
) else (
    echo ⚠️  无法自动启动 Docker Desktop
    echo.
    echo 请手动启动：
    echo 1. 在开始菜单搜索 "Docker Desktop"
    echo 2. 点击启动
    echo 3. 等待系统托盘图标不再闪烁
    echo.
)

echo 正在验证 Docker...
docker info >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ Docker 现在运行正常！
    echo.
    echo 可以重新运行打包脚本了
) else (
    echo ❌ Docker 仍然无法运行
    echo.
    echo 请尝试：
    echo 1. 重启 Docker Desktop
    echo 2. 重启电脑
    echo 3. 检查虚拟化是否启用（BIOS 设置）
    echo.
)

pause
