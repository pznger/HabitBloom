#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HabitBloom Docker 打包脚本
无需安装 Linux/WSL，使用 Docker 容器打包 APK
"""
import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# 颜色输出
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def check_docker():
    """检查 Docker 是否安装"""
    try:
        result = subprocess.run(
            ['docker', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, None

def check_docker_running():
    """检查 Docker 守护进程是否运行"""
    try:
        result = subprocess.run(
            ['docker', 'info'],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

def fix_docker_issue():
    """修复 Docker 问题"""
    print()
    print("=" * 60)
    print_warning("Docker 未正确运行")
    print("=" * 60)
    print()
    print("可能的原因和解决方法：")
    print()
    print("1. Docker Desktop 未启动")
    print("   → 在开始菜单搜索 'Docker Desktop' 并启动")
    print("   → 等待系统托盘图标不再闪烁（约 30 秒）")
    print()
    print("2. Docker Desktop 需要重启")
    print("   → 右键系统托盘图标 → Quit Docker Desktop")
    print("   → 重新启动 Docker Desktop")
    print()
    print("3. WSL 2 后端未启用")
    print("   → 打开 Docker Desktop")
    print("   → Settings → General")
    print("   → 确保 'Use the WSL 2 based engine' 已勾选")
    print()
    print("4. 虚拟化未启用")
    print("   → 重启电脑")
    print("   → 进入 BIOS 启用虚拟化（Virtualization）")
    print()
    print("5. 完全重新安装")
    print("   → 卸载 Docker Desktop")
    print("   → 重启电脑")
    print("   → 重新安装 Docker Desktop")
    print()
    
    if platform.system() == 'Windows':
        response = input("是否尝试启动 Docker Desktop？(y/n): ").strip().lower()
        if response == 'y':
            try:
                subprocess.Popen(['start', 'docker'], shell=True)
                print_info("已尝试启动 Docker Desktop，请等待 30 秒后重新运行脚本")
            except:
                print_warning("无法自动启动，请手动启动 Docker Desktop")
    
    print()
    print("验证 Docker 是否运行：")
    print("  docker info")
    print()

def install_docker_windows():
    """Windows 安装 Docker 指引"""
    print_info("Docker Desktop 安装指引：")
    print()
    print("1. 下载 Docker Desktop for Windows:")
    print("   https://www.docker.com/products/docker-desktop/")
    print()
    print("2. 运行安装程序并按照提示安装")
    print()
    print("3. 安装完成后重启电脑")
    print()
    print("4. 启动 Docker Desktop（在开始菜单搜索 'Docker Desktop'）")
    print()
    print("5. 等待 Docker 启动完成（系统托盘图标不再闪烁）")
    print()
    print("6. 重新运行此脚本")
    print()
    
    response = input("是否现在打开下载页面？(y/n): ").strip().lower()
    if response == 'y':
        import webbrowser
        webbrowser.open('https://www.docker.com/products/docker-desktop/')

def build_docker_image():
    """构建 Docker 镜像"""
    print_info("构建 Docker 镜像（首次需要几分钟）...")
    
    project_dir = Path(__file__).parent.absolute()
    dockerfile = project_dir / 'Dockerfile'
    
    if not dockerfile.exists():
        print_error("未找到 Dockerfile")
        return False
    
    try:
        cmd = [
            'docker', 'build',
            '-t', 'habitbloom-builder',
            '-f', str(dockerfile),
            str(project_dir)
        ]
        
        print_info(f"执行: {' '.join(cmd)}")
        print()
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        for line in process.stdout:
            print(line, end='')
        
        process.wait()
        
        if process.returncode == 0:
            print_success("Docker 镜像构建完成")
            return True
        else:
            print_error("Docker 镜像构建失败")
            print()
            # 检查是否是 Docker 未运行的问题
            if not check_docker_running():
                fix_docker_issue()
            return False
    except Exception as e:
        print_error(f"构建镜像时出错: {e}")
        error_str = str(e).lower()
        if '500' in error_str or 'ping' in error_str or 'connection' in error_str:
            print()
            print_warning("这可能是 Docker 未正确启动的问题")
            fix_docker_issue()
        return False

def run_docker_build(build_type='debug'):
    """在 Docker 容器中打包"""
    print_info(f"在 Docker 容器中打包 {build_type} 版本...")
    print_warning("这可能需要 10-30 分钟，请耐心等待...")
    print()
    
    project_dir = Path(__file__).parent.absolute()
    
    # 确保 bin 目录存在
    bin_dir = project_dir / 'bin'
    bin_dir.mkdir(exist_ok=True)
    
    try:
        # 运行 Docker 容器
        cmd = [
            'docker', 'run',
            '--rm',  # 运行后自动删除容器
            '-v', f'{project_dir}:/app',  # 挂载项目目录
            '-v', f'{bin_dir}:/app/bin',  # 挂载输出目录
            'habitbloom-builder',
            'buildozer', 'android', build_type
        ]
        
        print_info(f"执行: {' '.join(cmd)}")
        print()
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        for line in process.stdout:
            print(line, end='')
        
        process.wait()
        
        if process.returncode == 0:
            print_success("打包完成！")
            return True
        else:
            print_error("打包失败")
            if not check_docker_running():
                fix_docker_issue()
            return False
    except Exception as e:
        print_error(f"运行容器时出错: {e}")
        error_str = str(e).lower()
        if '500' in error_str or 'ping' in error_str or 'connection' in error_str:
            fix_docker_issue()
        return False

def find_apk():
    """查找生成的 APK"""
    project_dir = Path(__file__).parent.absolute()
    bin_dir = project_dir / 'bin'
    
    if bin_dir.exists():
        apk_files = list(bin_dir.glob('*.apk'))
        if apk_files:
            return apk_files[0]
    return None

def main():
    """主函数"""
    print("=" * 60)
    print("  HabitBloom Docker 打包工具")
    print("  无需安装 Linux/WSL，使用 Docker 容器打包")
    print("=" * 60)
    print()
    
    # 检查 Docker
    docker_installed, docker_version = check_docker()
    if not docker_installed:
        print_error("未检测到 Docker")
        print()
        
        if platform.system() == 'Windows':
            print_warning("需要安装 Docker Desktop for Windows")
            install_docker_windows()
        else:
            print_info("请先安装 Docker:")
            print("  - Ubuntu/Debian: sudo apt install docker.io")
            print("  - macOS: 下载 Docker Desktop")
            print("  - 其他系统: https://docs.docker.com/get-docker/")
        
        return 1
    
    print_success(f"Docker 已安装: {docker_version}")
    print()
    
    # 检查 Docker 是否运行
    print_info("检查 Docker 守护进程...")
    if not check_docker_running():
        print_error("Docker 守护进程未运行")
        fix_docker_issue()
        return 1
    
    print_success("Docker 守护进程运行正常")
    print()
    
    # 检查项目文件
    project_dir = Path(__file__).parent.absolute()
    if not (project_dir / 'main_kivy.py').exists():
        print_error("未找到 main_kivy.py，请确保在项目根目录运行")
        return 1
    
    if not (project_dir / 'buildozer.spec').exists():
        print_error("未找到 buildozer.spec")
        return 1
    
    # 选择打包类型
    print("选择打包类型:")
    print("1) Debug 版本（用于测试）")
    print("2) Release 版本（用于发布，需要签名）")
    choice = input("请选择 [1/2，默认 1]: ").strip() or '1'
    build_type = 'release' if choice == '2' else 'debug'
    print()
    
    # 检查镜像是否存在
    print_info("检查 Docker 镜像...")
    result = subprocess.run(
        ['docker', 'images', '-q', 'habitbloom-builder'],
        capture_output=True,
        text=True
    )
    
    if not result.stdout.strip():
        print_warning("Docker 镜像不存在，开始构建...")
        print()
        if not build_docker_image():
            return 1
        print()
    else:
        print_success("Docker 镜像已存在")
        print()
    
    # 打包
    if run_docker_build(build_type):
        # 查找 APK
        apk = find_apk()
        if apk:
            print()
            print("=" * 60)
            print_success("打包完成！")
            print("=" * 60)
            print()
            print(f"📦 APK 文件: {apk}")
            print(f"📊 文件大小: {apk.stat().st_size / 1024 / 1024:.2f} MB")
            print()
            print("📲 下一步：")
            print("   1. 将 APK 文件传输到手机")
            print("   2. 在手机上开启「允许安装未知来源应用」")
            print("   3. 点击 APK 文件安装")
            return 0
        else:
            print_warning("未找到 APK 文件，请检查 bin/ 目录")
            return 1
    else:
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        print_warning("用户取消操作")
        sys.exit(1)
    except Exception as e:
        print_error(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
