#!/bin/bash
# HabitBloom 环境检查脚本
# 在打包前运行此脚本检查环境是否准备就绪

echo "========================================"
echo "  HabitBloom 打包环境检查"
echo "========================================"
echo ""

ERRORS=0
WARNINGS=0

# 检查 Python
echo "1. 检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "   ✅ Python3: $PYTHON_VERSION"
    
    # 检查版本是否 >= 3.8
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        echo "   ⚠️  警告: Python 版本应 >= 3.8，当前为 $PYTHON_VERSION"
        ((WARNINGS++))
    fi
else
    echo "   ❌ 未找到 Python3"
    ((ERRORS++))
fi
echo ""

# 检查 pip
echo "2. 检查 pip..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version 2>&1 | awk '{print $2}')
    echo "   ✅ pip3: $PIP_VERSION"
else
    echo "   ❌ 未找到 pip3"
    ((ERRORS++))
fi
echo ""

# 检查 Java
echo "3. 检查 Java..."
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -n 1 | awk '{print $3}' | tr -d '"')
    echo "   ✅ Java: $JAVA_VERSION"
    
    # 检查是否为 JDK 11+
    if [ -n "$JAVA_HOME" ]; then
        echo "   ✅ JAVA_HOME: $JAVA_HOME"
    else
        echo "   ⚠️  警告: JAVA_HOME 未设置"
        ((WARNINGS++))
    fi
    
    # 检查版本
    JAVA_MAJOR=$(echo $JAVA_VERSION | cut -d. -f1)
    if [ "$JAVA_MAJOR" -lt 11 ]; then
        echo "   ⚠️  警告: Java 版本应 >= 11，当前为 $JAVA_VERSION"
        ((WARNINGS++))
    fi
else
    echo "   ❌ 未找到 Java"
    ((ERRORS++))
fi
echo ""

# 检查 Buildozer
echo "4. 检查 Buildozer..."
if command -v buildozer &> /dev/null; then
    BUILDozer_VERSION=$(buildozer --version 2>&1 | head -n 1)
    echo "   ✅ Buildozer: $BUILDozer_VERSION"
else
    echo "   ⚠️  未安装 Buildozer（首次运行会自动安装）"
    ((WARNINGS++))
fi
echo ""

# 检查 Cython
echo "5. 检查 Cython..."
if python3 -c "import cython" 2>/dev/null; then
    CYTHON_VERSION=$(python3 -c "import cython; print(cython.__version__)" 2>/dev/null)
    echo "   ✅ Cython: $CYTHON_VERSION"
else
    echo "   ⚠️  未安装 Cython（首次运行会自动安装）"
    ((WARNINGS++))
fi
echo ""

# 检查必要文件
echo "6. 检查项目文件..."
if [ -f "main_kivy.py" ]; then
    echo "   ✅ main_kivy.py 存在"
else
    echo "   ❌ main_kivy.py 不存在"
    ((ERRORS++))
fi

if [ -f "buildozer.spec" ]; then
    echo "   ✅ buildozer.spec 存在"
else
    echo "   ❌ buildozer.spec 不存在"
    ((ERRORS++))
fi

if [ -d "src" ]; then
    echo "   ✅ src/ 目录存在"
else
    echo "   ❌ src/ 目录不存在"
    ((ERRORS++))
fi

if [ -d "kivy_ui" ]; then
    echo "   ✅ kivy_ui/ 目录存在"
else
    echo "   ❌ kivy_ui/ 目录不存在"
    ((ERRORS++))
fi
echo ""

# 检查磁盘空间
echo "7. 检查磁盘空间..."
AVAILABLE_SPACE=$(df -h . | tail -1 | awk '{print $4}')
echo "   可用空间: $AVAILABLE_SPACE"
# 简单检查，如果小于 5GB 给出警告
AVAILABLE_GB=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$AVAILABLE_GB" -lt 5 ]; then
    echo "   ⚠️  警告: 可用空间可能不足（建议至少 8GB）"
    ((WARNINGS++))
fi
echo ""

# 检查网络（可选）
echo "8. 检查网络连接..."
if ping -c 1 -W 2 google.com &> /dev/null; then
    echo "   ✅ 网络连接正常"
else
    echo "   ⚠️  无法连接到 Google（可能影响 SDK 下载）"
    ((WARNINGS++))
fi
echo ""

# 总结
echo "========================================"
echo "  检查完成"
echo "========================================"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ 环境检查通过！可以开始打包。"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  有 $WARNINGS 个警告，但可以继续打包。"
    exit 0
else
    echo "❌ 发现 $ERRORS 个错误，请先解决这些问题。"
    exit 1
fi
