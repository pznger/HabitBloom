@echo off
chcp 65001 >nul
echo ============================================================
echo   HabitBloom Android SDK 下载问题修复工具
echo ============================================================
echo.

cd /d "%~dp0"

echo 正在检查网络连接...
ping -n 1 8.8.8.8 >nul 2>&1
if errorlevel 1 (
    echo ❌ 网络连接异常
    echo.
    echo 请检查：
    echo 1. 网络连接是否正常
    echo 2. 防火墙设置
    echo 3. 代理配置
    echo.
    goto :menu
) else (
    echo ✅ 网络连接正常
)

echo.
echo ============================================================
echo 解决方案选择
echo ============================================================
echo.
echo 1. 配置代理（如果有代理服务器）
echo 2. 手动下载 SDK 指南
echo 3. 使用 GitHub Actions 云端打包（推荐）
echo 4. 重试下载（使用当前网络）
echo 5. 查看详细说明
echo.

set /p choice=请选择方案 (1-5): 

if "%choice%"=="1" (
    goto :proxy
) else if "%choice%"=="2" (
    goto :manual
) else if "%choice%"=="3" (
    goto :github
) else if "%choice%"=="4" (
    goto :retry
) else if "%choice%"=="5" (
    goto :help
) else (
    echo ❌ 无效选项
    pause
    exit /b 1
)

:proxy
echo.
echo ============================================================
echo 配置代理
echo ============================================================
echo.
set /p proxy_host=请输入代理地址 (例如: 127.0.0.1): 
set /p proxy_port=请输入代理端口 (例如: 7890): 

set HTTP_PROXY=http://%proxy_host%:%proxy_port%
set HTTPS_PROXY=http://%proxy_host%:%proxy_port%

echo.
echo ✅ 已设置代理：
echo    HTTP_PROXY=%HTTP_PROXY%
echo    HTTPS_PROXY=%HTTPS_PROXY%
echo.
echo 现在可以运行：
echo    briefcase create android
echo.
pause
exit /b 0

:manual
echo.
echo ============================================================
echo 手动下载 Android SDK 指南
echo ============================================================
echo.
echo 步骤 1: 下载 Android SDK Command-Line Tools
echo   访问: https://developer.android.com/studio#command-tools
echo   或使用镜像站点
echo.
echo 步骤 2: 解压到以下目录：
echo   %USERPROFILE%\.briefcase\tools\android_sdk\cmdline-tools\latest
echo.
echo 步骤 3: 设置环境变量
echo   set ANDROID_HOME=%USERPROFILE%\.briefcase\tools\android_sdk
echo.
echo 步骤 4: 接受许可证
echo   sdkmanager --licenses
echo.
echo 步骤 5: 安装 SDK 组件
echo   sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.0"
echo.
echo 详细说明请查看: 解决SDK下载问题.md
echo.
pause
exit /b 0

:github
echo.
echo ============================================================
echo 使用 GitHub Actions 云端打包（推荐）
echo ============================================================
echo.
echo ✅ 这是最可靠的方案，完全避免网络问题！
echo.
echo 步骤：
echo 1. 确保代码已提交到 GitHub
echo 2. 打开仓库 → Actions 标签
echo 3. 选择 "Build PyQt5 APK"
echo 4. 点击 "Run workflow"
echo 5. 等待打包完成（约 15-30 分钟）
echo 6. 在 Artifacts 中下载 APK
echo.
echo 优势：
echo   ✅ 云端运行，网络稳定
echo   ✅ 自动下载所有依赖
echo   ✅ 无需本地配置
echo   ✅ 完全免费
echo.
echo 查看详细说明: PyQt5快速开始.md
echo.
pause
exit /b 0

:retry
echo.
echo ============================================================
echo 重试下载
echo ============================================================
echo.
echo 正在重试 Briefcase 初始化...
echo.
echo 提示：
echo - 如果网络不稳定，可能需要多次重试
echo - 建议在网络较好的时段重试
echo - 可以考虑使用代理或 VPN
echo.
set /p confirm=是否继续？(y/n): 
if /i not "%confirm%"=="y" (
    exit /b 0
)

briefcase create android
if errorlevel 1 (
    echo.
    echo ❌ 下载仍然失败
    echo.
    echo 建议：
    echo 1. 使用代理（选项 1）
    echo 2. 手动下载 SDK（选项 2）
    echo 3. 使用 GitHub Actions（选项 3，推荐）
) else (
    echo.
    echo ✅ 初始化成功！
)

pause
exit /b 0

:help
echo.
echo ============================================================
echo 详细说明
echo ============================================================
echo.
echo 请查看以下文档：
echo   - 解决SDK下载问题.md
echo   - PyQt5打包指南.md
echo   - PyQt5快速开始.md
echo.
echo 常见问题：
echo   1. 网络连接中断 → 使用代理或 GitHub Actions
echo   2. 下载速度慢 → 使用代理或手动下载
echo   3. 无法访问 Google 服务器 → 使用 GitHub Actions（推荐）
echo.
pause
exit /b 0

:menu
pause
exit /b 1
