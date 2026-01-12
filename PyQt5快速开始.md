# 🚀 PyQt5 打包成 APK - 快速开始

## ✅ 已为您准备好

我已经创建了所有必需的文件：
- ✅ `pyproject.toml` - Briefcase 配置文件
- ✅ `briefcase_build.py` - Python 打包脚本
- ✅ `一键打包PyQt5.bat` - Windows 一键打包脚本
- ✅ `.github/workflows/build-pyqt5-apk.yml` - GitHub Actions 工作流

---

## 🎯 三种打包方式

### 方式 1：使用批处理脚本（最简单，Windows）

```bash
# 双击运行或在命令行执行
一键打包PyQt5.bat
```

然后选择选项 4（完整流程）

---

### 方式 2：使用 Python 脚本

```bash
# 安装 Briefcase
pip install briefcase

# 运行打包脚本
python briefcase_build.py
```

---

### 方式 3：使用 GitHub Actions（云端打包，推荐）

1. **提交文件到 GitHub**
   ```bash
   git add pyproject.toml
   git add .github/workflows/build-pyqt5-apk.yml
   git commit -m "添加 PyQt5 Android 打包配置"
   git push
   ```

2. **在 GitHub 上触发打包**
   - 打开仓库 → Actions 标签
   - 选择 "Build PyQt5 APK"
   - 点击 "Run workflow"

3. **下载 APK**
   - 等待打包完成（约 15-30 分钟）
   - 在 Artifacts 中下载 APK

---

## 📋 手动步骤（如果脚本不工作）

### 步骤 1：安装 Briefcase

```bash
pip install briefcase
```

### 步骤 2：初始化项目（首次运行）

```bash
briefcase create android
```

**注意：** 首次运行会下载 Android SDK，可能需要 10-30 分钟。

### 步骤 3：构建应用

```bash
briefcase build android
```

### 步骤 4：打包 APK

```bash
briefcase package android
```

### 步骤 5：找到 APK

APK 文件通常在：
```
android/HabitBloom/app/build/outputs/apk/debug/HabitBloom-1.0.0-debug.apk
```

---

## ⚠️ 重要提示

### 1. PyQt5 在 Android 上的限制

- **某些功能可能不可用**
  - 某些 PyQt5 模块在 Android 上可能不完全支持
  - 建议在真实设备上测试所有功能

- **性能考虑**
  - PyQt5 在 Android 上的性能可能不如原生应用
  - 大型应用可能需要优化

### 2. 首次打包时间

- **下载 Android SDK：** 10-30 分钟（取决于网络）
- **构建过程：** 5-15 分钟
- **总时间：** 约 15-45 分钟

### 3. 如果遇到问题

**问题：找不到模块**
- 检查 `pyproject.toml` 中的 `requires` 列表
- 确保所有依赖都已列出

**问题：PyQt5 无法运行**
- 考虑使用 PyQt6（对移动平台支持更好）
- 或者使用 Kivy（需要重写 UI）

**问题：APK 太大**
- 使用 `briefcase package android --release`
- 移除不必要的依赖

---

## 🆚 为什么选择 Briefcase？

| 特性 | Briefcase | Buildozer (Kivy) |
|------|-----------|------------------|
| 支持 PyQt5 | ✅ 是 | ❌ 否 |
| 代码修改 | ✅ 无需修改 | ❌ 需要重写 |
| 打包难度 | 中等 | 简单 |
| Android 支持 | 有限 | 原生支持 |

---

## 📚 详细文档

查看 `PyQt5打包指南.md` 获取：
- 详细步骤说明
- 常见问题解答
- 高级配置选项
- GitHub Actions 配置

---

## 🎉 开始打包！

**推荐方式：**
1. 使用 `一键打包PyQt5.bat`（Windows）
2. 或使用 GitHub Actions（云端打包）

**祝您打包成功！** 🚀
