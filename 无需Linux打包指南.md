# 🚀 HabitBloom 无需 Linux 打包指南

不想安装 Linux/WSL？这里有两种完全不需要 Linux 的打包方案！

---

## 方案一：Docker 打包 ⭐ 推荐

### 优点
- ✅ 本地打包，速度快
- ✅ 无需安装完整的 Linux 系统
- ✅ 只需安装 Docker Desktop（约 500MB）
- ✅ 可以离线打包

### 步骤

#### 1. 安装 Docker Desktop

**Windows:**
1. 下载：https://www.docker.com/products/docker-desktop/
2. 运行安装程序
3. 重启电脑
4. 启动 Docker Desktop（等待启动完成）

**验证安装：**
```cmd
docker --version
```

#### 2. 运行打包脚本

```cmd
python docker_build.py
```

或者双击：`一键打包-无需Linux.bat`，选择选项 1

#### 3. 等待完成

- 首次运行：会构建 Docker 镜像（5-10 分钟）
- 然后自动打包 APK（10-20 分钟）
- APK 文件在 `bin/` 目录

---

## 方案二：GitHub Actions 云端打包 ⭐⭐ 最推荐

### 优点
- ✅ **完全免费**
- ✅ **无需安装任何软件**
- ✅ **云端自动打包**
- ✅ **支持自动发布**

### 步骤

#### 1. 创建 GitHub 仓库

1. 登录 https://github.com
2. 点击右上角 "+" → "New repository"
3. 输入仓库名称（如 `HabitBloom`）
4. 选择 Public 或 Private
5. 点击 "Create repository"

#### 2. 设置 GitHub Actions

运行脚本：
```cmd
python github_actions_build.py
```

这会自动创建 `.github/workflows/build-apk.yml` 文件

#### 3. 上传到 GitHub

```bash
# 如果还没有 git 仓库
git init
git add .
git commit -m "Initial commit"

# 添加 GitHub 远程仓库
git remote add origin https://github.com/你的用户名/HabitBloom.git
git branch -M main
git push -u origin main
```

或者使用 GitHub Desktop 图形界面上传

#### 4. 触发打包

1. 打开 GitHub 仓库页面
2. 点击 "Actions" 标签
3. 点击左侧 "Build HabitBloom APK"
4. 点击右侧 "Run workflow" 按钮
5. 点击绿色的 "Run workflow" 按钮
6. 等待打包完成（约 10-20 分钟）

#### 5. 下载 APK

1. 打包完成后，刷新 Actions 页面
2. 点击最新的运行记录
3. 滚动到底部 "Artifacts" 部分
4. 点击下载 APK 文件

---

## 方案三：Google Colab（临时方案）

如果以上两种都不行，可以使用 Google Colab：

### 步骤

1. **打开 Colab**
   - 访问 https://colab.research.google.com
   - 创建新笔记本

2. **上传项目**
   - 在左侧文件面板上传项目 zip 文件
   - 或使用以下代码：

```python
# 安装依赖
!pip install buildozer cython
!apt update
!apt install -y build-essential openjdk-11-jdk git

# 解压项目（如果上传了 zip）
!unzip habitbloom.zip -d habitbloom

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

## 对比三种方案

| 方案 | 需要安装 | 速度 | 难度 | 推荐度 |
|------|---------|------|------|--------|
| **Docker** | Docker Desktop | 快 | ⭐⭐ | ⭐⭐⭐ |
| **GitHub Actions** | 无需 | 中等 | ⭐ | ⭐⭐⭐⭐ |
| **Google Colab** | 无需 | 慢 | ⭐⭐ | ⭐⭐ |

---

## 快速开始

### 最简单的方式（GitHub Actions）

```cmd
# 1. 运行设置脚本
python github_actions_build.py

# 2. 按照提示创建 GitHub 仓库并上传

# 3. 在 GitHub 上点击 "Run workflow"

# 4. 等待完成并下载 APK
```

### 本地打包（Docker）

```cmd
# 1. 安装 Docker Desktop
# 2. 运行打包脚本
python docker_build.py
```

---

## 常见问题

### Q: Docker Desktop 安装失败
**A**: 
- 确保启用了虚拟化（BIOS 设置）
- 确保 Windows 版本 >= Windows 10 64-bit
- 尝试以管理员身份安装

### Q: GitHub Actions 打包失败
**A**: 
- 检查 `.github/workflows/build-apk.yml` 文件是否存在
- 确保项目文件已正确上传
- 查看 Actions 页面的错误日志

### Q: 哪种方案最快？
**A**: 
- Docker 本地打包最快（10-20 分钟）
- GitHub Actions 次之（10-20 分钟，但需要等待队列）
- Google Colab 最慢（20-30 分钟）

---

## 推荐流程

**不想安装任何软件** → 使用 GitHub Actions
1. 运行 `python github_actions_build.py`
2. 创建 GitHub 仓库并上传
3. 在 GitHub 上触发打包
4. 下载 APK

**想要本地打包** → 使用 Docker
1. 安装 Docker Desktop
2. 运行 `python docker_build.py`
3. 等待完成，APK 在 `bin/` 目录

---

就这么简单！选择最适合你的方案即可！🎉
