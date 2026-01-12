# 📱 如何下载 APK 文件

## 🎉 构建成功！

如果 GitHub Actions 构建成功，APK 文件在以下位置：

---

## 📥 下载 APK 的方法

### 方法 1：从 GitHub Actions Artifacts 下载（推荐）

#### 步骤：

1. **打开 GitHub 仓库**
   - 访问你的 GitHub 仓库页面

2. **点击 "Actions" 标签**
   - 在仓库顶部导航栏

3. **找到最新的运行记录**
   - 应该显示绿色 ✓ 表示成功
   - 点击进入详情

4. **滚动到页面底部**
   - 找到 "Artifacts" 部分

5. **下载 APK**
   - 点击 Artifact 名称（如 `habitbloom-apk` 或 `habitbloom-pyqt5-apk`）
   - 会自动下载一个 ZIP 文件
   - 解压 ZIP 文件，里面就是 APK

---

### 方法 2：从工作流日志中查找路径

如果是在本地构建的，APK 位置：

#### Kivy 版本（Buildozer）：
```
HabitBloom/bin/HabitBloom-1.0.0-debug.apk
```

#### PyQt5 版本（Briefcase）：
```
HabitBloom/android/HabitBloom/app/build/outputs/apk/debug/HabitBloom-1.0.0-debug.apk
```

---

## 🔍 详细步骤（GitHub Actions）

### 截图说明：

```
GitHub 仓库页面
  ↓
点击 "Actions" 标签
  ↓
找到最新的运行（绿色 ✓）
  ↓
点击进入详情
  ↓
滚动到底部
  ↓
找到 "Artifacts" 部分
  ↓
点击 Artifact 名称下载
```

---

## 📋 不同版本的 APK 名称

### Kivy 版本：
- Artifact 名称：`habitbloom-apk`
- APK 文件名：`HabitBloom-1.0.0-debug.apk`

### PyQt5 版本：
- Artifact 名称：`habitbloom-pyqt5-apk`
- APK 文件名：`HabitBloom-1.0.0-debug.apk`

---

## ⚠️ 如果找不到 APK

### 检查清单：

1. **确认构建成功**
   - Actions 页面显示绿色 ✓
   - 没有红色 ❌ 错误

2. **检查 Artifacts 部分**
   - 滚动到页面最底部
   - Artifacts 在 "Summary" 部分下方

3. **检查工作流日志**
   - 查看 "Upload APK" 步骤
   - 确认是否成功上传

4. **Artifacts 保留时间**
   - 默认保留 90 天
   - 如果超过时间可能已删除

---

## 🚀 快速链接

如果构建成功，直接访问：
```
https://github.com/你的用户名/你的仓库名/actions
```

然后：
1. 点击最新的运行记录
2. 滚动到底部
3. 下载 Artifacts

---

## 📱 安装到手机

下载 APK 后：

1. **传输到手机**
   - 通过 USB、WiFi 或云盘

2. **允许安装未知来源**
   - 设置 → 安全 → 允许安装未知来源应用

3. **安装 APK**
   - 点击 APK 文件
   - 按照提示安装

---

## 🆘 仍然找不到？

### 可能的原因：

1. **Artifacts 上传失败**
   - 查看 "Upload APK" 步骤的日志
   - 检查是否有错误

2. **APK 文件路径错误**
   - 检查工作流中的 `path` 配置
   - 确认 APK 文件确实存在

3. **工作流未完成**
   - 等待所有步骤完成
   - 确保没有失败

### 解决方法：

1. **查看工作流日志**
   - 检查每个步骤的输出
   - 查找 APK 文件的实际位置

2. **重新运行工作流**
   - 在 Actions 页面点击 "Re-run jobs"
   - 等待完成后再下载

---

## ✅ 总结

**GitHub Actions 构建成功 → APK 在 Artifacts 中**

**步骤：**
1. 打开仓库 → Actions
2. 点击最新的运行记录
3. 滚动到底部 → Artifacts
4. 下载并解压 ZIP 文件
5. 得到 APK 文件

**就这么简单！** 🎉
