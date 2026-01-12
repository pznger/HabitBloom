@echo off
chcp 65001 >nul
echo ============================================================
echo   HabitBloom GitHub 访问问题修复工具
echo ============================================================
echo.

cd /d "%~dp0"

echo 正在检查 GitHub 连接...
ping -n 1 github.com >nul 2>&1
if errorlevel 1 (
    echo ❌ 无法访问 GitHub
    echo.
) else (
    echo ✅ GitHub 连接正常
    echo.
)

echo ============================================================
echo 解决方案选择
echo ============================================================
echo.
echo 1. 配置 Git 代理（如果有代理服务器）
echo 2. 使用 GitHub Actions 云端打包（强烈推荐）
echo 3. 手动下载模板指南
echo 4. 重试连接（使用当前网络）
echo 5. 查看详细说明
echo.

set /p choice=请选择方案 (1-5): 

if "%choice%"=="1" (
    goto :proxy
) else if "%choice%"=="2" (
    goto :github
) else if "%choice%"=="3" (
    goto :manual
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
echo 配置 Git 代理
echo ============================================================
echo.
set /p proxy_host=请输入代理地址 (例如: 127.0.0.1): 
set /p proxy_port=请输入代理端口 (例如: 7890): 

set proxy_url=http://%proxy_host%:%proxy_port%

echo.
echo 正在配置 Git 代理...
git config --global http.proxy %proxy_url%
git config --global https.proxy %proxy_url%

set HTTP_PROXY=%proxy_url%
set HTTPS_PROXY=%proxy_url%

echo.
echo ✅ 已设置代理：
echo    Git HTTP 代理: %proxy_url%
echo    Git HTTPS 代理: %proxy_url%
echo    环境变量 HTTP_PROXY: %HTTP_PROXY%
echo    环境变量 HTTPS_PROXY: %HTTPS_PROXY%
echo.
echo 现在可以运行：
echo    briefcase create android
echo.
echo 提示: 如果需要取消代理，运行：
echo    git config --global --unset http.proxy
echo    git config --global --unset https.proxy
echo.
pause
exit /b 0

:github
echo.
echo ============================================================
echo 使用 GitHub Actions 云端打包（强烈推荐）
echo ============================================================
echo.
echo ✅ 这是最可靠的方案，完全避免网络问题！
echo.
echo 步骤：
echo 1. 确保代码已提交到 GitHub
echo    如果还没有，可以使用：
echo    - GitHub Desktop（图形界面）
echo    - 网页上传（最简单）
echo    - Git 命令行
echo.
echo 2. 打开仓库 → Actions 标签
echo.
echo 3. 选择 "Build PyQt5 APK"
echo.
echo 4. 点击 "Run workflow"
echo.
echo 5. 等待打包完成（约 15-30 分钟）
echo.
echo 6. 在 Artifacts 中下载 APK
echo.
echo 优势：
echo   ✅ 云端运行，网络稳定
echo   ✅ 自动下载所有依赖
echo   ✅ 无需配置代理或 VPN
echo   ✅ 完全免费
echo   ✅ 无需本地安装 Android SDK
echo.
echo 查看详细说明: PyQt5快速开始.md
echo.
pause
exit /b 0

:manual
echo.
echo ============================================================
echo 手动下载模板指南
echo ============================================================
echo.
echo 步骤 1: 下载模板
echo   访问: https://github.com/beeware/briefcase-android-gradle-template
echo   点击 "Code" → "Download ZIP"
echo   或使用镜像站点
echo.
echo 步骤 2: 解压模板
echo   解压到临时目录，例如: C:\temp\briefcase-android-gradle-template
echo.
echo 步骤 3: 配置 Briefcase 使用本地模板
echo   编辑: %USERPROFILE%\.briefcase\briefcase.toml
echo   添加: template = "file:///C:/temp/briefcase-android-gradle-template"
echo.
echo 注意: 手动配置可能比较复杂，建议使用 GitHub Actions
echo.
echo 详细说明请查看: 解决GitHub访问问题.md
echo.
pause
exit /b 0

:retry
echo.
echo ============================================================
echo 重试连接
echo ============================================================
echo.
echo 正在测试 GitHub 连接...
ping -n 3 github.com
echo.
echo 提示：
echo - 如果无法连接，建议使用 GitHub Actions（选项 2）
echo - 或者配置代理（选项 1）
echo.
set /p confirm=是否继续尝试 Briefcase 初始化？(y/n): 
if /i not "%confirm%"=="y" (
    exit /b 0
)

echo.
echo 正在重试 Briefcase 初始化...
briefcase create android
if errorlevel 1 (
    echo.
    echo ❌ 连接仍然失败
    echo.
    echo 强烈建议：
    echo 1. 使用 GitHub Actions（选项 2，推荐）
    echo 2. 配置代理（选项 1）
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
echo   - 解决GitHub访问问题.md
echo   - PyQt5打包指南.md
echo   - PyQt5快速开始.md
echo.
echo 常见问题：
echo   1. 无法访问 GitHub → 使用代理或 GitHub Actions
echo   2. 连接超时 → 使用 GitHub Actions（推荐）
echo   3. 网络限制 → 使用 GitHub Actions（推荐）
echo.
echo 最佳方案：
echo   使用 GitHub Actions 云端打包
echo   - 完全避免网络问题
echo   - 自动处理所有依赖
echo   - 无需本地配置
echo.
pause
exit /b 0
