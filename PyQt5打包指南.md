# 📱 PyQt5 打包成 Android APK 指南

## 🎯 使用 BeeWare Briefcase

由于 PyQt5 本身不支持 Android，我们使用 **BeeWare Briefcase** 来将 PyQt5 应用打包成 Android APK。

---

## 📋 前置要求

### 1. Python 环境
- Python 3.8 或更高版本
- pip 已安装

### 2. Android 开发工具（可选，Briefcase 会自动下载）
- Android SDK
- Java JDK

**注意：** Briefcase 会自动下载所需的 Android 工具，但首次运行可能需要较长时间。

---

## 🚀 快速开始

### 方法 1：使用自动化脚本（推荐）

```bash
# 1. 安装依赖
pip install briefcase

# 2. 运行打包脚本
python briefcase_build.py
```

### 方法 2：手动步骤

```bash
# 1. 安装 Briefcase
pip install briefcase

# 2. 初始化项目（首次运行）
briefcase create android

# 3. 构建应用
briefcase build android

# 4. 打包 APK
briefcase package android
```

---

## 📝 详细步骤

### 步骤 1：安装 Briefcase

```bash
pip install briefcase
```

### 步骤 2：检查配置

确保 `pyproject.toml` 文件存在且配置正确：

```toml
[tool.briefcase.app.habitbloom]
sources = ["src", "main.py"]
requires = [
    "PyQt5>=5.15.0",
    "PyQt5-Qt5>=5.15.0",
    "PyQt5-sip>=12.9.0",
]
```

### 步骤 3：初始化项目（首次运行）

```bash
briefcase create android
```

**首次运行会：**
- 下载 Android SDK（如果未安装）
- 创建 Android 项目结构
- 配置 Gradle 构建系统

**注意：** 这可能需要 10-30 分钟，取决于网络速度。

### 步骤 4：构建应用

```bash
briefcase build android
```

这会编译 Python 代码和依赖。

### 步骤 5：打包 APK

```bash
briefcase package android
```

这会生成可安装的 APK 文件，位置通常在：
```
android/HabitBloom/app/build/outputs/apk/debug/
```

---

## 🎨 添加应用图标和启动画面

### 1. 创建资源目录

```bash
mkdir -p resources
```

### 2. 准备图标

- **文件名：** `resources/icon.png`
- **尺寸：** 512x512 像素
- **格式：** PNG，透明背景

### 3. 准备启动画面

- **文件名：** `resources/splash.png`
- **尺寸：** 1242x2208 像素（或按比例）
- **格式：** PNG

### 4. 更新配置

在 `pyproject.toml` 中已配置：
```toml
icon = "resources/icon.png"
splash = "resources/splash.png"
```

---

## 🔧 常见问题

### Q1: Briefcase 下载 Android SDK 很慢

**解决方案：**
1. 使用国内镜像（如果可用）
2. 手动下载 Android SDK 并配置环境变量
3. 使用代理加速下载

### Q2: 构建失败，提示找不到模块

**解决方案：**
1. 检查 `pyproject.toml` 中的 `requires` 列表
2. 确保所有依赖都已列出
3. 运行 `briefcase update android` 更新依赖

### Q3: PyQt5 在 Android 上无法运行

**注意：** PyQt5 在 Android 上的支持可能有限。如果遇到问题：

1. **检查 PyQt5 版本**
   ```bash
   pip show PyQt5
   ```

2. **尝试使用 PyQt6**
   - PyQt6 对移动平台支持更好
   - 需要修改代码以适配 PyQt6

3. **考虑使用 Kivy**
   - Kivy 对 Android 有原生支持
   - 但需要重写 UI 代码

### Q4: APK 文件太大

**解决方案：**
1. 使用 `briefcase package android --release` 生成发布版本
2. 启用代码压缩和优化
3. 移除不必要的依赖

### Q5: 应用无法安装

**解决方案：**
1. 确保手机允许安装未知来源应用
2. 检查 APK 签名是否正确
3. 尝试使用 `briefcase package android --release` 生成签名版本

---

## 📦 使用 GitHub Actions 自动打包

### 创建 GitHub Actions 工作流

创建 `.github/workflows/build-pyqt5-apk.yml`:

```yaml
name: Build PyQt5 APK

on:
  workflow_dispatch:
  push:
    branches: [ main ]
    paths:
      - 'main.py'
      - 'src/**'
      - 'pyproject.toml'

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install Briefcase
      run: |
        pip install briefcase
    
    - name: Create Android project
      run: |
        briefcase create android
    
    - name: Build APK
      run: |
        briefcase build android
        briefcase package android
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: habitbloom-pyqt5-apk
        path: android/HabitBloom/app/build/outputs/apk/**/*.apk
```

---

## 🆚 PyQt5 vs Kivy 对比

| 特性 | PyQt5 + Briefcase | Kivy + Buildozer |
|------|-------------------|------------------|
| 打包工具 | Briefcase | Buildozer |
| Android 支持 | 有限 | 原生支持 |
| 代码修改 | 无需修改 | 需要重写 UI |
| 打包难度 | 中等 | 简单 |
| 性能 | 较好 | 优秀 |
| 社区支持 | 较少 | 较多 |

---

## ⚠️ 重要提示

1. **PyQt5 在 Android 上的限制**
   - 某些 PyQt5 功能可能在 Android 上不可用
   - 建议在 Android 设备上测试所有功能

2. **首次打包时间**
   - 下载 Android SDK 可能需要 10-30 分钟
   - 构建过程可能需要 5-15 分钟

3. **依赖管理**
   - 确保所有依赖都列在 `pyproject.toml` 中
   - 某些 Python 包可能不支持 Android

4. **测试建议**
   - 在真实 Android 设备上测试
   - 测试所有核心功能
   - 检查内存使用情况

---

## 📚 参考资源

- [BeeWare 官方文档](https://briefcase.readthedocs.io/)
- [Briefcase Android 指南](https://briefcase.readthedocs.io/en/latest/tutorial/android/)
- [PyQt5 文档](https://www.riverbankcomputing.com/static/Docs/PyQt5/)

---

## 🎉 完成！

打包成功后，APK 文件位于：
```
android/HabitBloom/app/build/outputs/apk/debug/HabitBloom-1.0.0-debug.apk
```

将 APK 传输到手机并安装即可！

---

**需要帮助？** 查看 `briefcase_build.py` 脚本或运行：
```bash
briefcase --help
```
