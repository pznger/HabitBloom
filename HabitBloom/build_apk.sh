#!/bin/bash
# HabitBloom APK 打包脚本
# 在 Linux/WSL 环境下运行

echo "========================================"
echo "  HabitBloom APK 打包"
echo "========================================"

# 检查是否安装了必要工具
check_dependencies() {
    echo "检查依赖..."
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ 未找到 Python3，请先安装"
        exit 1
    fi
    
    # 检查 pip
    if ! command -v pip3 &> /dev/null; then
        echo "❌ 未找到 pip3，请先安装"
        exit 1
    fi
    
    # 检查 Java
    if ! command -v java &> /dev/null; then
        echo "❌ 未找到 Java，请安装 JDK 11+"
        exit 1
    fi
    
    echo "✅ 基础依赖检查通过"
}

# 安装 Buildozer 和依赖
install_buildozer() {
    echo "安装 Buildozer 和依赖..."
    
    pip3 install --upgrade buildozer
    pip3 install --upgrade cython
    
    # Ubuntu/Debian 依赖
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y \
            python3-pip \
            build-essential \
            git \
            python3-dev \
            ffmpeg \
            libsdl2-dev \
            libsdl2-image-dev \
            libsdl2-mixer-dev \
            libsdl2-ttf-dev \
            libportmidi-dev \
            libswscale-dev \
            libavformat-dev \
            libavcodec-dev \
            zlib1g-dev \
            libgstreamer1.0 \
            gstreamer1.0-plugins-base \
            gstreamer1.0-plugins-good \
            openjdk-11-jdk \
            autoconf \
            libtool \
            pkg-config \
            libffi-dev \
            libssl-dev
    fi
    
    echo "✅ Buildozer 安装完成"
}

# 初始化 Buildozer（首次运行）
init_buildozer() {
    if [ ! -d ".buildozer" ]; then
        echo "初始化 Buildozer（首次运行需要下载 Android SDK/NDK，可能需要较长时间）..."
        buildozer android debug
    fi
}

# 打包 Debug APK
build_debug() {
    echo "开始打包 Debug APK..."
    buildozer android debug
    
    if [ -f "bin/*.apk" ]; then
        echo "✅ APK 打包成功！"
        echo "📦 文件位置: $(ls bin/*.apk)"
    else
        echo "❌ 打包失败，请检查错误日志"
    fi
}

# 打包 Release APK
build_release() {
    echo "开始打包 Release APK..."
    buildozer android release
    
    if [ -f "bin/*-release*.apk" ]; then
        echo "✅ Release APK 打包成功！"
        echo "📦 文件位置: $(ls bin/*-release*.apk)"
    else
        echo "❌ 打包失败，请检查错误日志"
    fi
}

# 主流程
main() {
    check_dependencies
    install_buildozer
    
    case "$1" in
        "release")
            build_release
            ;;
        *)
            build_debug
            ;;
    esac
}

# 运行
main "$@"
