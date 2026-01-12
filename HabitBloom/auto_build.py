#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HabitBloom 全自动打包脚本
一键完成环境配置和 APK 打包
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

def run_cmd(cmd, shell=False, check=True, capture_output=False):
    """运行命令"""
    try:
        if isinstance(cmd, str):
            cmd = cmd.split()
        result = subprocess.run(
            cmd,
            shell=shell,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        if capture_output:
            print_error(f"命令执行失败: {e.stderr}")
        else:
            print_error(f"命令执行失败: {e}")
        return None
    except FileNotFoundError:
        print_error(f"命令未找到: {cmd}")
        return None

def check_command(cmd):
    """检查命令是否存在"""
    return shutil.which(cmd) is not None

def is_windows():
    return platform.system() == 'Windows'

def is_linux():
    return platform.system() == 'Linux'

def check_wsl():
    """检查 WSL 是否可用"""
    if not is_windows():
        return False
    result = run_cmd(['wsl', '--list', '--verbose'], capture_output=True, check=False)
    return result is not None and result.returncode == 0

def install_wsl():
    """安装 WSL"""
    print_info("检测到 Windows 系统，需要 WSL 环境")
    print_warning("WSL 安装需要管理员权限")
    
    response = input("是否现在安装 WSL？(y/n): ").strip().lower()
    if response != 'y':
        print_error("需要 WSL 才能继续，请手动安装后重新运行此脚本")
        print_info("安装命令: wsl --install -d Ubuntu-22.04")
        return False
    
    print_info("正在安装 WSL...")
    print_warning("这可能需要几分钟，请耐心等待...")
    
    # 尝试以管理员权限运行
    try:
        result = run_cmd(['wsl', '--install', '-d', 'Ubuntu'], check=False)
        if result and result.returncode == 0:
            print_success("WSL 安装完成！")
            print_warning("请重启电脑，然后重新运行此脚本")
            return True
        else:
            print_error("WSL 安装失败，请以管理员身份运行此脚本")
            print_info("或者手动运行: wsl --install -d Ubuntu-22.04")
            return False
    except Exception as e:
        print_error(f"安装 WSL 时出错: {e}")
        return False

def run_in_wsl(cmd):
    """在 WSL 中运行命令"""
    wsl_cmd = ['wsl', 'bash', '-c', cmd]
    return run_cmd(wsl_cmd, check=False)

def setup_linux_env():
    """在 Linux/WSL 中设置环境"""
    print_info("开始配置 Linux 环境...")
    
    # 更新系统
    print_info("更新系统包列表...")
    run_cmd(['sudo', 'apt', 'update'], check=False)
    
    # 安装基础工具
    print_info("安装基础工具（这可能需要几分钟）...")
    packages = [
        'python3', 'python3-pip', 'python3-dev',
        'build-essential', 'git',
        'openjdk-11-jdk',
        'autoconf', 'libtool', 'pkg-config',
        'libffi-dev', 'libssl-dev', 'zlib1g-dev',
        'libsdl2-dev', 'libsdl2-image-dev',
        'libsdl2-mixer-dev', 'libsdl2-ttf-dev'
    ]
    
    cmd = f"sudo apt install -y {' '.join(packages)}"
    result = run_cmd(cmd, shell=True, check=False)
    
    if result and result.returncode == 0:
        print_success("基础工具安装完成")
    else:
        print_warning("部分包安装可能失败，继续尝试...")
    
    # 配置 Java
    print_info("配置 Java 环境...")
    java_home = '/usr/lib/jvm/java-11-openjdk-amd64'
    if os.path.exists(java_home):
        os.environ['JAVA_HOME'] = java_home
        os.environ['PATH'] = f"{java_home}/bin:{os.environ.get('PATH', '')}"
        print_success("Java 环境已配置")
    else:
        print_warning("Java 路径未找到，可能需要手动配置")
    
    # 安装 Buildozer
    print_info("安装 Buildozer...")
    run_cmd(['pip3', 'install', '--upgrade', 'pip'], check=False)
    run_cmd(['pip3', 'install', '--upgrade', 'buildozer', 'cython'], check=False)
    
    # 验证
    result = run_cmd(['buildozer', '--version'], capture_output=True, check=False)
    if result and result.returncode == 0:
        print_success(f"Buildozer 安装成功: {result.stdout.strip()}")
        return True
    else:
        print_error("Buildozer 安装失败")
        return False

def get_project_path():
    """获取项目路径"""
    script_dir = Path(__file__).parent.absolute()
    return str(script_dir)

def convert_to_wsl_path(windows_path):
    """将 Windows 路径转换为 WSL 路径"""
    # 替换盘符
    if ':' in windows_path:
        drive = windows_path[0].lower()
        path = windows_path[3:].replace('\\', '/')
        return f"/mnt/{drive}{path}"
    return windows_path.replace('\\', '/')

def build_apk_in_wsl(project_path_wsl, build_type='debug'):
    """在 WSL 中打包 APK"""
    print_info(f"在 WSL 中打包 {build_type} 版本...")
    
    # 进入项目目录
    cmd = f"cd '{project_path_wsl}' && buildozer android {build_type}"
    
    print_warning("开始打包，这可能需要 10-30 分钟...")
    print_warning("首次打包会下载 Android SDK/NDK（约 2-3GB），请确保网络稳定")
    print()
    
    # 直接运行，显示输出
    wsl_cmd = ['wsl', 'bash', '-c', cmd]
    try:
        process = subprocess.Popen(
            wsl_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 实时显示输出
        for line in process.stdout:
            print(line, end='')
        
        process.wait()
        
        if process.returncode == 0:
            print_success("打包完成！")
            return True
        else:
            print_error("打包失败，请查看上面的错误信息")
            return False
    except Exception as e:
        print_error(f"打包过程出错: {e}")
        return False

def find_apk(project_path):
    """查找生成的 APK 文件"""
    bin_dir = Path(project_path) / 'bin'
    if bin_dir.exists():
        apk_files = list(bin_dir.glob('*.apk'))
        if apk_files:
            return apk_files[0]
    return None

def copy_apk_to_windows(apk_path_wsl):
    """将 APK 复制到 Windows 目录"""
    if not is_windows():
        return None
    
    # 转换为 Windows 路径
    if apk_path_wsl.startswith('/mnt/'):
        drive = apk_path_wsl[5]
        path = apk_path_wsl[6:]
        windows_path = f"{drive.upper()}:{path.replace('/', '\\')}"
        
        # 复制到下载目录
        downloads = Path.home() / 'Downloads'
        if downloads.exists():
            dest = downloads / Path(apk_path_wsl).name
            try:
                shutil.copy2(windows_path, dest)
                print_success(f"APK 已复制到: {dest}")
                return str(dest)
            except Exception as e:
                print_warning(f"复制 APK 失败: {e}")
    
    return None

def main():
    """主函数"""
    print("=" * 50)
    print("  HabitBloom 全自动打包工具")
    print("=" * 50)
    print()
    
    # 检查项目文件
    project_path = get_project_path()
    if not Path(project_path, 'main_kivy.py').exists():
        print_error("未找到 main_kivy.py，请确保在项目根目录运行此脚本")
        return 1
    
    if not Path(project_path, 'buildozer.spec').exists():
        print_error("未找到 buildozer.spec，请确保在项目根目录运行此脚本")
        return 1
    
    print_success(f"项目路径: {project_path}")
    print()
    
    # 选择打包类型
    print("选择打包类型:")
    print("1) Debug 版本（用于测试）")
    print("2) Release 版本（用于发布，需要签名）")
    choice = input("请选择 [1/2，默认 1]: ").strip() or '1'
    build_type = 'release' if choice == '2' else 'debug'
    print()
    
    # Windows 系统
    if is_windows():
        print_info("检测到 Windows 系统")
        
        # 检查 WSL
        if not check_wsl():
            print_warning("未检测到 WSL")
            if not install_wsl():
                return 1
            print()
            print_warning("请重启电脑后重新运行此脚本")
            return 0
        
        print_success("WSL 已安装")
        
        # 转换路径
        project_path_wsl = convert_to_wsl_path(project_path)
        print_info(f"WSL 项目路径: {project_path_wsl}")
        print()
        
        # 在 WSL 中设置环境
        print_info("在 WSL 中配置环境...")
        setup_script = f"""
        cd '{project_path_wsl}' || exit 1
        sudo apt update -qq
        sudo apt install -y python3 python3-pip python3-dev build-essential git openjdk-11-jdk autoconf libtool pkg-config libffi-dev libssl-dev zlib1g-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev > /dev/null 2>&1
        pip3 install --upgrade pip buildozer cython > /dev/null 2>&1
        export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
        export PATH=$JAVA_HOME/bin:$PATH
        buildozer --version
        """
        
        result = run_in_wsl(setup_script)
        if result and result.returncode == 0:
            print_success("环境配置完成")
        else:
            print_warning("环境配置可能不完整，继续尝试打包...")
        
        print()
        
        # 打包
        if build_apk_in_wsl(project_path_wsl, build_type):
            # 查找 APK
            apk_search = f"find '{project_path_wsl}/bin' -name '*.apk' 2>/dev/null | head -1"
            result = run_in_wsl(apk_search)
            if result and result.stdout.strip():
                apk_path_wsl = result.stdout.strip()
                print_success(f"APK 文件: {apk_path_wsl}")
                
                # 复制到 Windows
                copy_apk_to_windows(apk_path_wsl)
                
                print()
                print("=" * 50)
                print_success("打包完成！")
                print("=" * 50)
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
    
    # Linux 系统
    elif is_linux():
        print_info("检测到 Linux 系统")
        print()
        
        # 设置环境
        if not setup_linux_env():
            print_error("环境配置失败")
            return 1
        
        print()
        
        # 打包
        print_info(f"开始打包 {build_type} 版本...")
        print_warning("这可能需要 10-30 分钟，请耐心等待...")
        print()
        
        os.chdir(project_path)
        result = run_cmd(['buildozer', 'android', build_type], check=False)
        
        if result and result.returncode == 0:
            # 查找 APK
            apk = find_apk(project_path)
            if apk:
                print_success(f"APK 文件: {apk}")
                print()
                print("=" * 50)
                print_success("打包完成！")
                print("=" * 50)
                return 0
            else:
                print_warning("未找到 APK 文件，请检查 bin/ 目录")
                return 1
        else:
            print_error("打包失败")
            return 1
    
    else:
        print_error(f"不支持的操作系统: {platform.system()}")
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
