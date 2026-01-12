#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HabitBloom GitHub Actions 云端打包脚本
自动创建 GitHub Actions 工作流，在云端打包 APK
"""
import os
import json
from pathlib import Path

def create_github_workflow():
    """创建 GitHub Actions 工作流文件"""
    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = """name: Build HabitBloom APK

on:
  workflow_dispatch:  # 手动触发
  push:
    branches: [ main, master ]
    paths:
      - 'main_kivy.py'
      - 'buildozer.spec'
      - 'src/**'
      - 'kivy_ui/**'

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install system dependencies
      run: |
        sudo apt update
        sudo apt install -y \
          python3-pip \
          build-essential \
          git \
          python3-dev \
          openjdk-11-jdk \
          autoconf \
          libtool \
          pkg-config \
          libffi-dev \
          libssl-dev \
          zlib1g-dev \
          libsdl2-dev \
          libsdl2-image-dev \
          libsdl2-mixer-dev \
          libsdl2-ttf-dev
    
    - name: Set up Java
      run: |
        echo "JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> $GITHUB_ENV
        echo "$JAVA_HOME/bin" >> $GITHUB_PATH
    
    - name: Install Buildozer
      run: |
        pip install --upgrade pip
        pip install buildozer cython
    
    - name: Build APK
      run: |
        cd HabitBloom || cd .
        buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: habitbloom-apk
        path: HabitBloom/bin/*.apk
        retention-days: 7
    
    - name: Create Release
      if: github.event_name == 'workflow_dispatch'
      uses: softprops/action-gh-release@v1
      with:
        files: HabitBloom/bin/*.apk
        draft: false
        prerelease: false
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""
    
    workflow_file = workflow_dir / 'build-apk.yml'
    workflow_file.write_text(workflow_content, encoding='utf-8')
    
    return workflow_file

def create_github_script():
    """创建 GitHub 打包说明"""
    script_content = """# 🚀 HabitBloom GitHub Actions 云端打包

## 使用方法

### 方法一：使用 GitHub Actions（推荐，完全免费）

1. **创建 GitHub 仓库**
   - 登录 https://github.com
   - 创建新仓库（可以是私有的）
   - 上传项目文件

2. **运行打包脚本**
   ```bash
   python github_actions_build.py
   ```
   这会自动创建 GitHub Actions 工作流文件

3. **提交并推送**
   ```bash
   git add .github/workflows/build-apk.yml
   git commit -m "Add GitHub Actions build workflow"
   git push
   ```

4. **触发打包**
   - 打开 GitHub 仓库页面
   - 点击 "Actions" 标签
   - 点击 "Build HabitBloom APK"
   - 点击 "Run workflow" → "Run workflow"
   - 等待打包完成（约 10-20 分钟）

5. **下载 APK**
   - 打包完成后，在 Actions 页面点击对应的运行
   - 在 "Artifacts" 部分下载 APK 文件

### 方法二：使用 Docker（本地打包，无需 WSL）

1. **安装 Docker Desktop**
   - Windows: https://www.docker.com/products/docker-desktop/
   - 安装后启动 Docker Desktop

2. **运行打包脚本**
   ```bash
   python docker_build.py
   ```

3. **等待打包完成**
   - 首次运行会构建 Docker 镜像（需要几分钟）
   - 然后自动开始打包
   - APK 文件在 `bin/` 目录

## 对比

| 方法 | 优点 | 缺点 |
|------|------|------|
| GitHub Actions | 完全免费、云端打包、无需本地环境 | 需要 GitHub 账号 |
| Docker | 本地打包、速度快、可离线 | 需要安装 Docker Desktop |
| WSL | 原生支持、功能完整 | 需要安装 Linux 系统 |

## 推荐

- **不想安装任何软件** → 使用 GitHub Actions
- **想要本地打包** → 使用 Docker
- **想要完整控制** → 使用 WSL
"""
    
    script_file = Path('GITHUB_BUILD.md')
    script_file.write_text(script_content, encoding='utf-8')
    
    return script_file

def main():
    """主函数"""
    print("=" * 60)
    print("  HabitBloom GitHub Actions 云端打包设置")
    print("=" * 60)
    print()
    
    print("这个脚本会：")
    print("1. 创建 GitHub Actions 工作流文件")
    print("2. 创建使用说明文档")
    print()
    
    response = input("是否继续？(y/n): ").strip().lower()
    if response != 'y':
        print("已取消")
        return
    
    print()
    print("正在创建文件...")
    
    # 创建工作流
    workflow_file = create_github_workflow()
    print(f"✅ 已创建: {workflow_file}")
    
    # 创建说明文档
    doc_file = create_github_script()
    print(f"✅ 已创建: {doc_file}")
    
    print()
    print("=" * 60)
    print("✅ 设置完成！")
    print("=" * 60)
    print()
    print("📝 下一步：")
    print()
    print("1. 创建 GitHub 仓库（如果还没有）")
    print("   https://github.com/new")
    print()
    print("2. 提交文件到 GitHub")
    print("   git add .github/workflows/build-apk.yml")
    print("   git commit -m 'Add build workflow'")
    print("   git push")
    print()
    print("3. 在 GitHub 上触发打包")
    print("   - 打开仓库 → Actions 标签")
    print("   - 点击 'Build HabitBloom APK'")
    print("   - 点击 'Run workflow'")
    print()
    print("4. 等待打包完成并下载 APK")
    print()
    print("详细说明请查看: GITHUB_BUILD.md")
    print()

if __name__ == '__main__':
    main()
