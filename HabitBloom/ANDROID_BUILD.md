# HabitBloom 安卓打包指南

## 📁 项目结构

```
HabitBloom/
├── main.py              # PyQt5 桌面版入口
├── main_kivy.py         # Kivy 安卓版入口
├── buildozer.spec       # Buildozer 打包配置
├── requirements.txt     # PyQt5 依赖
├── requirements_kivy.txt # Kivy 依赖
├── build_apk.sh         # 打包脚本
├── src/                 # 共享业务逻辑
│   ├── database/
│   ├── managers/
│   └── utils/
├── kivy_ui/             # Kivy UI 层
│   ├── base.py
│   ├── screens/
│   └── widgets/
└── (PyQt5 views/)       # PyQt5 UI 层
```

## 🖥️ 桌面版运行（PyQt5）

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
python main.py
```

## 📱 Kivy 版本测试（桌面）

```bash
# 安装 Kivy
pip install -r requirements_kivy.txt

# 运行
python main_kivy.py
```

## 🔨 打包 APK

### 方法一：使用 WSL/Linux（推荐）

Buildozer 只能在 Linux 环境运行。Windows 用户需要使用 WSL。

#### 1. 安装 WSL（Windows）

```powershell
# PowerShell 管理员模式
wsl --install -d Ubuntu
```

#### 2. 在 WSL 中打包

```bash
# 进入项目目录
cd /mnt/d/笔记/副业/LLM_APP/HabitBloom

# 安装依赖
sudo apt update
sudo apt install -y python3-pip build-essential git python3-dev openjdk-11-jdk

# 安装 Buildozer
pip3 install buildozer cython

# 打包 APK（首次运行会下载 Android SDK/NDK，约 1-2GB）
buildozer android debug
```

#### 3. 获取 APK

打包成功后，APK 文件在 `bin/` 目录：
```
bin/habitbloom-1.0.0-arm64-v8a-debug.apk
```

### 方法二：使用 Google Colab（云端打包）

如果本地环境有问题，可以使用 Google Colab：

1. 打开 https://colab.research.google.com
2. 上传项目文件
3. 运行以下代码：

```python
# 安装 Buildozer
!pip install buildozer cython
!sudo apt install -y build-essential openjdk-11-jdk

# 上传 main_kivy.py, buildozer.spec, src/, kivy_ui/

# 打包
!buildozer android debug

# 下载 APK
from google.colab import files
files.download('bin/habitbloom-1.0.0-arm64-v8a-debug.apk')
```

### 方法三：使用 GitHub Actions

创建 `.github/workflows/build.yml`：

```yaml
name: Build APK

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install buildozer cython
          sudo apt install -y build-essential openjdk-11-jdk
      
      - name: Build APK
        run: |
          cd HabitBloom
          buildozer android debug
      
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: habitbloom-apk
          path: HabitBloom/bin/*.apk
```

## ⚠️ 常见问题

### 1. 首次打包很慢
首次运行会下载 Android SDK、NDK，约 1-2GB，需要 10-30 分钟。

### 2. 内存不足
打包需要至少 4GB 内存。如果失败，尝试：
```bash
export GRADLE_OPTS="-Xmx2048m"
```

### 3. Java 版本问题
需要 JDK 11+：
```bash
sudo apt install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### 4. 网络问题
Android SDK 下载可能需要代理：
```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

## 📲 安装到手机

1. 将 APK 传输到手机
2. 开启「允许安装未知来源应用」
3. 点击 APK 安装

## 🔑 发布版本

发布到应用商店需要签名：

```bash
# 生成签名密钥
keytool -genkey -v -keystore habitbloom.keystore -alias habitbloom -keyalg RSA -keysize 2048 -validity 10000

# 修改 buildozer.spec
android.keystore = ~/habitbloom.keystore
android.keyalias = habitbloom

# 打包 Release 版本
buildozer android release
```
