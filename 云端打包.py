#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HabitBloom 云端打包脚本
提供多种无需本地 Linux 环境的打包方案
"""
import os
import sys
import subprocess
import platform
import webbrowser
from pathlib import Path

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
    """检查 Docker"""
    try:
        subprocess.run(['docker', '--version'], 
                      capture_output=True, check=True)
        return True
    except:
        return False

def main():
    """主菜单"""
    print("=" * 60)
    print("  HabitBloom 云端打包工具")
    print("  无需安装 Linux/WSL 的打包方案")
    print("=" * 60)
    print()
    
    print("请选择打包方式：")
    print()
    print("1. 🐳 Docker 打包（推荐，本地打包）")
    print("   - 需要安装 Docker Desktop")
    print("   - 本地打包，速度快")
    print("   - 无需 WSL/Linux")
    print()
    print("2. ☁️  GitHub Actions（推荐，完全免费）")
    print("   - 无需安装任何软件")
    print("   - 云端自动打包")
    print("   - 需要 GitHub 账号")
    print()
    print("3. 📖 查看详细说明")
    print()
    
    choice = input("请选择 [1/2/3]: ").strip()
    
    if choice == '1':
        # Docker 打包
        if not check_docker():
            print_error("未检测到 Docker")
            print()
            print_warning("需要安装 Docker Desktop")
            print()
            response = input("是否打开下载页面？(y/n): ").strip().lower()
            if response == 'y':
                webbrowser.open('https://www.docker.com/products/docker-desktop/')
            print()
            print("安装 Docker Desktop 后，运行: python docker_build.py")
        else:
            print_success("检测到 Docker，开始打包...")
            print()
            os.system('python docker_build.py')
    
    elif choice == '2':
        # GitHub Actions
        print_info("设置 GitHub Actions 云端打包...")
        print()
        os.system('python github_actions_build.py')
    
    elif choice == '3':
        # 显示说明
        print()
        print("=" * 60)
        print("  打包方案说明")
        print("=" * 60)
        print()
        print("方案一：Docker 打包")
        print("- 安装 Docker Desktop（约 500MB）")
        print("- 运行: python docker_build.py")
        print("- 首次构建镜像需要几分钟")
        print("- 后续打包约 10-20 分钟")
        print()
        print("方案二：GitHub Actions")
        print("- 完全免费，无需安装软件")
        print("- 需要 GitHub 账号")
        print("- 云端自动打包")
        print("- 运行: python github_actions_build.py")
        print("- 按照提示设置 GitHub 仓库")
        print()
        print("方案三：Google Colab（临时方案）")
        print("- 打开 https://colab.research.google.com")
        print("- 上传项目文件")
        print("- 运行打包代码")
        print("- 下载 APK")
        print()
    
    else:
        print_error("无效选择")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_warning("已取消")
        sys.exit(1)
