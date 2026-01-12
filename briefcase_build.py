#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HabitBloom PyQt5 Android 打包脚本
使用 BeeWare Briefcase 将 PyQt5 应用打包成 APK
"""
import os
import sys
import subprocess
from pathlib import Path

def check_briefcase():
    """检查 Briefcase 是否已安装"""
    try:
        result = subprocess.run(
            ["briefcase", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Briefcase 已安装: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Briefcase 未安装")
        return False

def install_briefcase():
    """安装 Briefcase"""
    print("正在安装 Briefcase...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "briefcase"],
            check=True
        )
        print("✅ Briefcase 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Briefcase 安装失败: {e}")
        return False

def create_resources():
    """创建资源文件目录"""
    resources_dir = Path("resources")
    resources_dir.mkdir(exist_ok=True)
    
    # 创建占位图标和启动画面说明
    readme = resources_dir / "README.md"
    if not readme.exists():
        readme.write_text("""# 资源文件

## 需要的文件

1. **icon.png** - 应用图标
   - 尺寸: 512x512 像素
   - 格式: PNG
   - 透明背景

2. **splash.png** - 启动画面
   - 尺寸: 1242x2208 像素（或按比例）
   - 格式: PNG

如果没有这些文件，Briefcase 会使用默认图标。
""", encoding='utf-8')
        print("✅ 已创建 resources 目录")
    
    return resources_dir.exists()

def setup_briefcase():
    """初始化 Briefcase 项目"""
    print("\n" + "="*60)
    print("初始化 Briefcase 项目")
    print("="*60)
    
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml 文件不存在！")
        return False
    
    # 检查网络连接
    print("检查网络连接...")
    try:
        import urllib.request
        urllib.request.urlopen("https://www.google.com", timeout=5)
        print("✅ 网络连接正常")
    except:
        print("⚠️  网络连接可能有问题")
        print("提示: 如果下载失败，可以：")
        print("  1. 使用代理（设置 HTTP_PROXY 和 HTTPS_PROXY）")
        print("  2. 使用 GitHub Actions 云端打包")
        print("  3. 手动下载 Android SDK")
        print("  详细说明请查看: 解决SDK下载问题.md")
    
    try:
        print("\n运行: briefcase create android")
        print("提示: 首次运行需要下载 Android SDK，可能需要 10-30 分钟")
        print("      如果下载失败，请查看 解决SDK下载问题.md")
        
        result = subprocess.run(
            ["briefcase", "create", "android"],
            check=True,
            capture_output=False
        )
        print("✅ Briefcase 项目初始化成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 初始化失败")
        print("\n可能的原因：")
        print("  1. 网络连接问题（无法访问 GitHub 或下载 Android SDK）")
        print("  2. 防火墙阻止连接")
        print("  3. 代理配置问题")
        print("  4. 无法克隆 GitHub 模板仓库")
        print("\n解决方案：")
        print("  1. 运行: 修复GitHub访问.bat（如果无法访问 GitHub）")
        print("  2. 运行: 修复SDK下载.bat（如果无法下载 SDK）")
        print("  3. 查看: 解决GitHub访问问题.md")
        print("  4. 使用 GitHub Actions 云端打包（强烈推荐，完全避免网络问题）")
        print("\n推荐：使用 GitHub Actions 云端打包")
        print("  - 提交代码到 GitHub")
        print("  - 在 Actions 中运行 'Build PyQt5 APK'")
        print("  - 等待完成并下载 APK")
        return False

def build_apk():
    """构建 APK"""
    print("\n" + "="*60)
    print("构建 Android APK")
    print("="*60)
    
    try:
        print("运行: briefcase build android")
        subprocess.run(
            ["briefcase", "build", "android"],
            check=True
        )
        print("✅ 构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def package_apk():
    """打包 APK"""
    print("\n" + "="*60)
    print("打包 Android APK")
    print("="*60)
    
    try:
        print("运行: briefcase package android")
        subprocess.run(
            ["briefcase", "package", "android"],
            check=True
        )
        print("✅ 打包成功")
        
        # 查找 APK 文件
        apk_files = list(Path("android").rglob("*.apk"))
        if apk_files:
            print(f"\n✅ APK 文件位置:")
            for apk in apk_files:
                print(f"   {apk.absolute()}")
        else:
            print("⚠️  未找到 APK 文件")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("  HabitBloom PyQt5 Android 打包工具")
    print("="*60)
    print()
    
    # 检查并安装 Briefcase
    if not check_briefcase():
        print("\n需要安装 Briefcase...")
        if not install_briefcase():
            print("\n❌ 无法安装 Briefcase，请手动安装:")
            print("   pip install briefcase")
            return 1
    
    # 创建资源目录
    create_resources()
    
    # 询问用户要执行的操作
    print("\n请选择操作:")
    print("1. 初始化项目（首次运行）")
    print("2. 构建 APK")
    print("3. 打包 APK（生成可安装的 APK）")
    print("4. 完整流程（初始化 + 构建 + 打包）")
    
    choice = input("\n请输入选项 (1-4): ").strip()
    
    if choice == "1":
        setup_briefcase()
    elif choice == "2":
        build_apk()
    elif choice == "3":
        package_apk()
    elif choice == "4":
        if setup_briefcase():
            if build_apk():
                package_apk()
    else:
        print("❌ 无效选项")
        return 1
    
    print("\n" + "="*60)
    print("完成！")
    print("="*60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
