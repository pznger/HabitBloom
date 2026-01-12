# 🔧 解决 Android SDK 下载问题

## ❌ 问题描述

Briefcase 在下载 Android SDK Command-Line Tools 时失败：
- 网络连接中断
- 下载速度慢或超时
- 无法访问 Google 服务器

---

## 🚀 解决方案

### 方案 1：使用代理（推荐，如果有代理）

#### Windows 设置代理环境变量

```bash
# 设置 HTTP 代理（替换为你的代理地址和端口）
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890

# 然后运行 Briefcase
briefcase create android
```

#### 或者在 PowerShell 中：

```powershell
$env:HTTP_PROXY="http://127.0.0.1:7890"
$env:HTTPS_PROXY="http://127.0.0.1:7890"
briefcase create android
```

---

### 方案 2：手动下载并配置 Android SDK

#### 步骤 1：手动下载 Android SDK Command-Line Tools

1. **访问 Android 开发者网站**
   - https://developer.android.com/studio#command-tools
   - 或使用镜像站点

2. **下载 Command-Line Tools**
   - 选择 Windows 版本
   - 下载 `commandlinetools-win-*.zip`

3. **解压到指定位置**
   ```bash
   # Briefcase 默认位置
   %USERPROFILE%\.briefcase\tools\android_sdk\cmdline-tools
   
   # 或者创建目录
   mkdir "%USERPROFILE%\.briefcase\tools\android_sdk\cmdline-tools\latest"
   # 将解压的内容放到 latest 目录中
   ```

#### 步骤 2：配置环境变量

```bash
# 设置 Android SDK 路径
set ANDROID_HOME=%USERPROFILE%\.briefcase\tools\android_sdk
set PATH=%PATH%;%ANDROID_HOME%\cmdline-tools\latest\bin
```

#### 步骤 3：接受 SDK 许可证

```bash
# 使用 sdkmanager 接受许可证
sdkmanager --licenses
# 输入 y 接受所有许可证
```

#### 步骤 4：安装必要的 SDK 组件

```bash
# 安装 Android SDK Platform 33
sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.0"
```

#### 步骤 5：重新运行 Briefcase

```bash
briefcase create android
```

---

### 方案 3：使用国内镜像（如果可用）

#### 配置 Android SDK 镜像源

创建或编辑 `%USERPROFILE%\.android\repositories.cfg`：

```ini
# 使用清华大学镜像（如果可用）
https://mirrors.tuna.tsinghua.edu.cn/android/repository/
```

**注意：** 镜像源可能不稳定，需要根据实际情况调整。

---

### 方案 4：使用 GitHub Actions（推荐，完全避免本地下载）

使用 GitHub Actions 在云端打包，完全避免本地网络问题：

1. **提交代码到 GitHub**
2. **在 Actions 中运行打包工作流**
3. **下载生成的 APK**

详见：`.github/workflows/build-pyqt5-apk.yml`

---

### 方案 5：使用 VPN 或加速工具

如果其他方案不可行：

1. **使用 VPN 连接到稳定的网络**
2. **使用网络加速工具**
3. **在非高峰时段重试**

---

## 🛠️ 自动化脚本

我已经创建了 `修复SDK下载.bat` 脚本，可以：
- 检查网络连接
- 配置代理（如果可用）
- 提供手动下载指南

---

## 📋 快速检查清单

- [ ] 检查网络连接是否正常
- [ ] 尝试使用代理（如果有）
- [ ] 考虑使用 GitHub Actions 云端打包
- [ ] 手动下载 SDK（如果网络持续失败）
- [ ] 检查防火墙设置

---

## 🆘 如果所有方案都失败

**最后的选择：使用 GitHub Actions**

这是最可靠的方法，因为：
- ✅ 在云端运行，网络稳定
- ✅ 自动下载所有依赖
- ✅ 无需本地配置
- ✅ 完全免费

**步骤：**
1. 提交代码到 GitHub
2. 在 Actions 中运行工作流
3. 等待打包完成
4. 下载 APK

---

## 📚 参考资源

- [Android SDK 官方下载](https://developer.android.com/studio#command-tools)
- [Briefcase 文档](https://briefcase.readthedocs.io/)
- [Android SDK 镜像配置](https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/)

---

**推荐方案：使用 GitHub Actions 云端打包，完全避免网络问题！** 🚀
