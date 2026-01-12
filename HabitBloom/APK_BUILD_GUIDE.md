# 📱 HabitBloom APK 打包完整指南

本指南将一步步引导您将 HabitBloom 应用打包成可以在手机上安装的 APK 文件。

## 📋 前置要求

### 系统要求
- **Windows 10/11** 或 **Linux** 或 **macOS**
- 至少 **8GB 可用磁盘空间**（Android SDK/NDK 约 2-3GB）
- 至少 **4GB 内存**
- 稳定的网络连接（首次打包需要下载大量文件）

### 必需软件
1. **Python 3.8+**
2. **Java JDK 11+**（Android 构建需要）
3. **Git**（用于下载依赖）

---

## 🚀 方法一：Windows 使用 WSL（推荐）

### 步骤 1：安装 WSL 和 Ubuntu

1. **打开 PowerShell（管理员模式）**
   ```powershell
   # 检查 WSL 是否已安装
   wsl --list --verbose
   ```

2. **如果没有安装，执行：**
   ```powershell
   wsl --install -d Ubuntu-22.04
   ```

3. **重启电脑**（如果需要）

4. **打开 Ubuntu**，设置用户名和密码

### 步骤 2：在 WSL 中配置环境

1. **更新系统包**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. **安装基础工具**
   ```bash
   sudo apt install -y \
       python3 \
       python3-pip \
       python3-dev \
       build-essential \
       git \
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
   ```

3. **配置 Java 环境变量**
   ```bash
   echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc
   echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
   source ~/.bashrc
   
   # 验证 Java
   java -version
   # 应该显示 openjdk version "11.x.x"
   ```

### 步骤 3：进入项目目录

```bash
# Windows 路径映射到 WSL
cd /mnt/d/笔记/副业/LLM_APP/HabitBloom

# 如果路径有中文，可能需要使用引号
cd "/mnt/d/笔记/副业/LLM_APP/HabitBloom"
```

**注意**：如果路径包含中文导致问题，可以：
- 在 Windows 中复制项目到纯英文路径（如 `D:\Projects\HabitBloom`）
- 然后在 WSL 中使用 `/mnt/d/Projects/HabitBloom`

### 步骤 4：安装 Buildozer

```bash
# 升级 pip
pip3 install --upgrade pip

# 安装 Buildozer 和 Cython
pip3 install buildozer cython

# 验证安装
buildozer --version
```

### 步骤 5：配置网络（如果需要代理）

如果下载 Android SDK 时遇到网络问题，可以设置代理：

```bash
# 设置代理（根据您的实际情况修改）
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890

# 或者使用系统代理
export http_proxy=$HTTP_PROXY
export https_proxy=$HTTPS_PROXY
```

### 步骤 6：首次初始化 Buildozer

```bash
# 首次运行会下载 Android SDK/NDK（约 2-3GB，需要 10-30 分钟）
# 请耐心等待，确保网络稳定
buildozer android debug

# 如果中途失败，可以重新运行，Buildozer 会继续下载
```

**首次运行说明**：
- 会自动下载 Android SDK、NDK、Gradle 等工具
- 下载的文件保存在 `~/.buildozer/` 目录
- 如果下载失败，可以删除 `.buildozer` 目录重新开始

### 步骤 7：检查 buildozer.spec 配置

确保 `buildozer.spec` 文件配置正确：

```bash
# 查看配置文件
cat buildozer.spec
```

关键配置项：
- `source.main = main_kivy.py` ✅
- `requirements = python3,kivy==2.3.1,pillow` ✅
- `android.api = 33` ✅
- `android.minapi = 21` ✅

### 步骤 8：开始打包

```bash
# 清理之前的构建（可选）
buildozer android clean

# 打包 Debug 版本（用于测试）
buildozer android debug

# 打包过程可能需要 10-30 分钟，请耐心等待
```

### 步骤 9：获取 APK 文件

打包成功后，APK 文件在 `bin/` 目录：

```bash
# 查看生成的 APK
ls -lh bin/*.apk

# 复制到 Windows 目录（方便传输到手机）
cp bin/*.apk /mnt/d/Downloads/habitbloom.apk
```

---

## 🐧 方法二：Linux 原生环境

如果您使用的是 Linux 系统，步骤类似，但不需要 WSL：

### 步骤 1：安装依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y \
    python3 python3-pip python3-dev \
    build-essential git \
    openjdk-11-jdk \
    autoconf libtool pkg-config \
    libffi-dev libssl-dev zlib1g-dev \
    libsdl2-dev libsdl2-image-dev \
    libsdl2-mixer-dev libsdl2-ttf-dev

# 配置 Java
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

### 步骤 2-9：同 WSL 方法

按照 WSL 方法的步骤 3-9 执行即可。

---

## ☁️ 方法三：使用 Google Colab（无需本地环境）

如果本地环境配置困难，可以使用 Google Colab 云端打包：

### 步骤 1：准备项目文件

将以下文件/目录压缩成 zip：
- `main_kivy.py`
- `buildozer.spec`
- `src/` 目录
- `kivy_ui/` 目录
- `requirements_kivy.txt`

### 步骤 2：在 Colab 中运行

1. 打开 https://colab.research.google.com
2. 创建新笔记本
3. 运行以下代码：

```python
# 安装依赖
!pip install buildozer cython
!apt update
!apt install -y build-essential openjdk-11-jdk git

# 上传项目 zip 文件（在左侧文件面板）
# 然后解压
!unzip habitbloom.zip -d habitbloom
!cd habitbloom && ls

# 打包
!cd habitbloom && buildozer android debug

# 下载 APK
from google.colab import files
import glob
apk_files = glob.glob('habitbloom/bin/*.apk')
if apk_files:
    files.download(apk_files[0])
```

---

## 📲 安装到手机

### 步骤 1：传输 APK 到手机

- **方法 A**：使用 USB 数据线连接手机，复制 APK 文件
- **方法 B**：通过微信/QQ 发送到手机
- **方法 C**：上传到网盘，在手机上下载

### 步骤 2：允许安装未知来源应用

**Android 设置步骤**：
1. 打开「设置」→「安全」或「应用」
2. 找到「允许安装未知来源应用」或「安装未知应用」
3. 选择您要使用的应用（文件管理器/浏览器），开启权限

**不同品牌可能略有不同**：
- **小米**：设置 → 应用设置 → 授权管理 → 安装未知应用
- **华为**：设置 → 安全 → 更多安全设置 → 外部来源应用下载
- **OPPO/OnePlus**：设置 → 其他设置 → 设备与隐私 → 安装未知应用

### 步骤 3：安装 APK

1. 在手机上找到下载的 APK 文件
2. 点击 APK 文件
3. 点击「安装」
4. 等待安装完成
5. 点击「打开」启动应用

---

## ⚠️ 常见问题解决

### 问题 1：Buildozer 下载失败

**症状**：下载 Android SDK/NDK 时网络错误

**解决方案**：
```bash
# 设置代理
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890

# 或者使用镜像源（如果可用）
# 重新运行 buildozer android debug
```

### 问题 2：内存不足

**症状**：编译时出现 "Out of memory" 错误

**解决方案**：
```bash
# 限制 Gradle 内存使用
export GRADLE_OPTS="-Xmx2048m -XX:MaxPermSize=512m"

# 重新打包
buildozer android debug
```

### 问题 3：Java 版本错误

**症状**：提示 Java 版本不兼容

**解决方案**：
```bash
# 确保使用 JDK 11
sudo apt install openjdk-11-jdk

# 设置环境变量
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# 验证
java -version
javac -version
```

### 问题 4：路径包含中文导致错误

**症状**：WSL 中无法访问包含中文的路径

**解决方案**：
```bash
# 在 Windows 中将项目复制到纯英文路径
# 例如：D:\Projects\HabitBloom
# 然后在 WSL 中使用
cd /mnt/d/Projects/HabitBloom
```

### 问题 5：APK 安装后闪退

**可能原因**：
1. 缺少权限配置
2. 数据库路径问题
3. 字体文件未正确加载

**解决方案**：
- 检查 `buildozer.spec` 中的权限配置
- 查看手机日志：`adb logcat | grep python`
- 确保 `android.permissions` 包含必要权限

### 问题 6：中文显示为方框

**解决方案**：
- 确保 `kivy_ui/fonts.py` 中的字体加载逻辑正确
- Android 系统会自动使用系统字体，通常不需要额外配置
- 如果仍有问题，检查字体文件路径

---

## 🔑 打包 Release 版本（用于发布）

如果要发布到应用商店，需要签名：

### 步骤 1：生成签名密钥

```bash
# 创建密钥库目录
mkdir -p ~/keystores
cd ~/keystores

# 生成密钥（会提示输入密码和信息）
keytool -genkey -v \
    -keystore habitbloom.keystore \
    -alias habitbloom \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000

# 记住密码和别名，后续需要用到
```

### 步骤 2：配置 buildozer.spec

编辑 `buildozer.spec`，取消注释并修改：

```ini
android.keystore = ~/keystores/habitbloom.keystore
android.keyalias = habitbloom
```

### 步骤 3：打包 Release

```bash
buildozer android release
```

打包时会提示输入密钥库密码。

---

## 📊 打包时间参考

- **首次打包**：30-60 分钟（下载 SDK/NDK）
- **后续打包**：10-20 分钟（仅编译）
- **清理后打包**：15-25 分钟

---

## ✅ 打包检查清单

打包前确认：

- [ ] Python 3.8+ 已安装
- [ ] Java JDK 11+ 已安装并配置
- [ ] Buildozer 已安装
- [ ] `buildozer.spec` 配置正确
- [ ] `main_kivy.py` 可以正常运行
- [ ] 所有依赖已列出在 `requirements` 中
- [ ] 网络连接稳定（首次打包需要下载大量文件）
- [ ] 有足够的磁盘空间（至少 8GB）

---

## 🎉 完成！

打包成功后，您就可以在手机上安装和使用 HabitBloom 了！

如果遇到其他问题，请检查：
1. Buildozer 日志：`.buildozer/android/platform/build/dists/habitbloom/build.log`
2. 应用日志：使用 `adb logcat` 查看运行时错误

祝您打包顺利！🌱
