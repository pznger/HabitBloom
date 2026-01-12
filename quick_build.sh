#!/bin/bash
# HabitBloom 快速打包脚本
# 简化版打包流程

set -e  # 遇到错误立即退出

echo "========================================"
echo "  HabitBloom 快速打包"
echo "========================================"
echo ""

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否在项目根目录
if [ ! -f "main_kivy.py" ] || [ ! -f "buildozer.spec" ]; then
    echo -e "${RED}❌ 错误: 请在项目根目录运行此脚本${NC}"
    exit 1
fi

# 检查环境
echo "📋 检查环境..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到 Python3${NC}"
    exit 1
fi

if ! command -v java &> /dev/null; then
    echo -e "${RED}❌ 未找到 Java，请安装 JDK 11+${NC}"
    exit 1
fi

# 安装 Buildozer（如果未安装）
if ! command -v buildozer &> /dev/null; then
    echo "📦 安装 Buildozer..."
    pip3 install --upgrade buildozer cython
fi

# 设置 Java 环境（如果未设置）
if [ -z "$JAVA_HOME" ]; then
    if [ -d "/usr/lib/jvm/java-11-openjdk-amd64" ]; then
        export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
        export PATH=$JAVA_HOME/bin:$PATH
        echo -e "${YELLOW}⚠️  已自动设置 JAVA_HOME${NC}"
    fi
fi

# 询问打包类型
echo ""
echo "选择打包类型:"
echo "1) Debug 版本（用于测试）"
echo "2) Release 版本（用于发布，需要签名）"
read -p "请选择 [1/2]: " BUILD_TYPE

case $BUILD_TYPE in
    1)
        BUILD_CMD="debug"
        echo ""
        echo -e "${GREEN}🚀 开始打包 Debug 版本...${NC}"
        ;;
    2)
        BUILD_CMD="release"
        echo ""
        echo -e "${GREEN}🚀 开始打包 Release 版本...${NC}"
        echo -e "${YELLOW}⚠️  注意: Release 版本需要配置签名密钥${NC}"
        ;;
    *)
        echo -e "${RED}❌ 无效选择${NC}"
        exit 1
        ;;
esac

# 清理（可选）
read -p "是否清理之前的构建？[y/N]: " CLEAN
if [[ $CLEAN =~ ^[Yy]$ ]]; then
    echo "🧹 清理构建文件..."
    buildozer android clean
fi

# 开始打包
echo ""
echo "⏳ 开始打包，这可能需要 10-30 分钟..."
echo "   首次打包会下载 Android SDK/NDK（约 2-3GB）"
echo "   请确保网络连接稳定"
echo ""

buildozer android $BUILD_CMD

# 检查结果
if [ -f bin/*.apk ]; then
    APK_FILE=$(ls bin/*.apk | head -1)
    APK_SIZE=$(du -h "$APK_FILE" | cut -f1)
    echo ""
    echo -e "${GREEN}========================================"
    echo "  ✅ 打包成功！"
    echo "========================================${NC}"
    echo "📦 APK 文件: $APK_FILE"
    echo "📊 文件大小: $APK_SIZE"
    echo ""
    echo "📲 下一步："
    echo "   1. 将 APK 文件传输到手机"
    echo "   2. 在手机上开启「允许安装未知来源应用」"
    echo "   3. 点击 APK 文件安装"
    echo ""
else
    echo ""
    echo -e "${RED}========================================"
    echo "  ❌ 打包失败"
    echo "========================================${NC}"
    echo "请检查错误日志："
    echo "  - .buildozer/android/platform/build/dists/habitbloom/build.log"
    exit 1
fi
