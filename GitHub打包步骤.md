# 🚀 HabitBloom GitHub Actions 打包步骤

## ✅ 已完成的准备工作

我已经为您创建了 GitHub Actions 配置文件：
- ✅ `.github/workflows/build-apk.yml` - 打包工作流
- ✅ `.gitignore` - Git 忽略文件

---

## 📝 接下来的步骤（只需 5 分钟）

### 步骤 1：创建 GitHub 仓库

1. **打开 GitHub**
   - 访问：https://github.com/new
   - 如果没有账号，先注册（免费）

2. **创建新仓库**
   - Repository name: `HabitBloom`（或任意名称）
   - 选择 Public 或 Private（都可以）
   - **不要**勾选 "Initialize with README"
   - 点击 "Create repository"

### 步骤 2：上传项目到 GitHub

#### 方法 A：使用 GitHub Desktop（最简单）

1. **下载 GitHub Desktop**
   - https://desktop.github.com/
   - 安装并登录

2. **添加仓库**
   - File → Add Local Repository
   - 选择 HabitBloom 项目文件夹
   - 点击 "Publish repository"
   - 选择刚才创建的仓库
   - 点击 "Publish repository"

#### 方法 B：使用命令行（如果已安装 Git）

```bash
# 进入项目目录
cd HabitBloom

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: HabitBloom app"

# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/HabitBloom.git

# 推送
git branch -M main
git push -u origin main
```

#### 方法 C：使用网页上传（最简单，无需安装）

1. 在 GitHub 仓库页面，点击 "uploading an existing file"
2. 将整个 HabitBloom 文件夹拖拽到页面
3. 点击 "Commit changes"

### 步骤 3：触发打包

1. **打开 Actions 标签**
   - 在 GitHub 仓库页面
   - 点击顶部的 "Actions" 标签

2. **运行工作流**
   - 点击左侧 "Build HabitBloom APK"
   - 点击右侧 "Run workflow" 按钮
   - 点击绿色的 "Run workflow" 按钮
   - 等待打包开始

3. **查看进度**
   - 点击正在运行的工作流
   - 可以看到实时日志
   - 打包需要 10-20 分钟

### 步骤 4：下载 APK

1. **打包完成后**
   - 刷新 Actions 页面
   - 点击最新的运行记录（绿色 ✓）

2. **下载 APK**
   - 滚动到页面底部
   - 找到 "Artifacts" 部分
   - 点击 "habitbloom-apk" 下载
   - 解压 zip 文件，里面就是 APK

---

## 🎯 快速流程总结

```
1. 创建 GitHub 仓库
   ↓
2. 上传项目文件（GitHub Desktop 或网页上传）
   ↓
3. 打开 Actions → Build HabitBloom APK → Run workflow
   ↓
4. 等待 10-20 分钟
   ↓
5. 下载 APK 文件
```

---

## ⚡ 最快方式（推荐）

**使用 GitHub Desktop：**

1. 下载：https://desktop.github.com/
2. 安装并登录
3. File → Add Local Repository → 选择 HabitBloom 文件夹
4. Publish repository → 选择仓库 → Publish
5. 在 GitHub 网页上：Actions → Run workflow
6. 等待完成并下载 APK

**总耗时：约 15-25 分钟**（包括上传和打包）

---

## 📋 检查清单

上传前确认：

- [ ] `.github/workflows/build-apk.yml` 文件存在
- [ ] `main_kivy.py` 文件存在
- [ ] `buildozer.spec` 文件存在
- [ ] `src/` 目录存在
- [ ] `kivy_ui/` 目录存在

---

## 🆘 遇到问题？

### Q: Actions 页面显示 "No workflows found"
**A**: 确保 `.github/workflows/build-apk.yml` 文件已上传

### Q: 打包失败
**A**: 
1. **查看错误日志**
   - 在 Actions 页面点击失败的运行
   - 查看 "Build APK" 步骤的详细日志
   - 查找红色错误信息

2. **检查 buildozer.spec 配置**
   ```bash
   # 在本地运行检查脚本
   python 检查配置.py
   ```
   
   确保以下配置正确：
   - ✅ `source.main = main_kivy.py` - 主入口文件
   - ✅ `requirements = python3,kivy==2.3.1,pillow` - 依赖（注意：逗号后不要有空格）
   - ✅ `android.api = 33` - Android API 版本
   - ✅ `android.minapi = 21` - 最低 API 版本

3. **检查必需文件**
   - ✅ `main_kivy.py` - 必须存在
   - ✅ `buildozer.spec` - 必须存在
   - ✅ `src/` 目录 - 必须存在
   - ✅ `kivy_ui/` 目录 - 必须存在

4. **常见错误及解决方法**
   
   **错误：找不到 main_kivy.py**
   - 确保文件已上传到 GitHub
   - 检查文件名大小写是否正确
   
   **错误：requirements 格式错误**
   - 确保格式为：`requirements = python3,kivy==2.3.1,pillow`
   - 不要有多余空格：`requirements = python3, kivy==2.3.1` ❌
   - 正确格式：`requirements = python3,kivy==2.3.1` ✅
   
   **错误：找不到模块**
   - 确保所有 Python 文件都已上传
   - 检查 `src/` 和 `kivy_ui/` 目录结构完整
   
   **错误：SDK 许可证问题**
   - 确保 `buildozer.spec` 中有：`android.accept_sdk_license = True`

### Q: 找不到 APK
**A**: 
- 确保打包成功（绿色 ✓）
- 滚动到页面底部查看 Artifacts
- 如果超时，Artifacts 会在 7 天后自动删除

---

## 🎉 完成！

打包成功后，您就可以在手机上安装 HabitBloom 了！

**需要帮助？**
- 查看详细文档：`无需Linux打包指南.md`
- GitHub Actions 文档：https://docs.github.com/en/actions

祝您打包顺利！🌱
