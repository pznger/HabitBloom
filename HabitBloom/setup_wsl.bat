@echo off
chcp 65001 >nul
echo ========================================
echo   HabitBloom WSL 环境设置助手
echo ========================================
echo.

REM 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ 请以管理员身份运行此脚本！
    echo    右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo 📋 检查 WSL 状态...
wsl --list --verbose >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ⚠️  WSL 未安装或未启用
    echo.
    echo 正在安装 WSL 和 Ubuntu...
    echo 这可能需要几分钟，请耐心等待...
    echo.
    wsl --install -d Ubuntu-22.04
    echo.
    echo ✅ WSL 安装完成！
    echo.
    echo ⚠️  重要提示：
    echo    1. 请重启电脑
    echo    2. 重启后打开 Ubuntu，设置用户名和密码
    echo    3. 然后在 Ubuntu 中继续后续步骤
    echo.
    pause
    exit /b 0
) else (
    echo ✅ WSL 已安装
    echo.
    wsl --list --verbose
    echo.
)

echo.
echo 📝 下一步操作：
echo.
echo 1. 打开 Ubuntu（在开始菜单搜索 "Ubuntu"）
echo 2. 进入项目目录：
echo    cd /mnt/d/笔记/副业/LLM_APP/HabitBloom
echo.
echo    如果路径有中文导致问题，请先复制项目到英文路径：
echo    例如：D:\Projects\HabitBloom
echo    然后使用：cd /mnt/d/Projects/HabitBloom
echo.
echo 3. 运行环境检查：
echo    chmod +x check_env.sh
echo    ./check_env.sh
echo.
echo 4. 开始打包：
echo    chmod +x quick_build.sh
echo    ./quick_build.sh
echo.
echo 或者查看详细指南：
echo   - 打包指南-中文.md（快速指南）
echo   - APK_BUILD_GUIDE.md（详细文档）
echo.
pause
