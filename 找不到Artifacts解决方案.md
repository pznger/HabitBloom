# 🔍 找不到 Artifacts 的解决方案

## 📋 详细步骤（带截图说明）

### 步骤 1：打开 Actions 页面

1. **打开你的 GitHub 仓库**
   - 例如：`https://github.com/你的用户名/HabitBloom`

2. **点击 "Actions" 标签**
   - 在仓库顶部导航栏
   - 位置：Code | Issues | Pull requests | **Actions** | Projects | ...

### 步骤 2：找到运行记录

1. **在左侧选择工作流**
   - 点击 "Build HabitBloom APK" 或 "Build PyQt5 APK"

2. **找到最新的运行记录**
   - 应该显示绿色 ✓（成功）
   - 或黄色 ⚠️（进行中）
   - 点击运行记录进入详情

### 步骤 3：查找 Artifacts

**重要：Artifacts 在页面最底部！**

1. **滚动到页面最底部**
   - Artifacts 不在顶部，需要向下滚动
   - 在 "Summary" 部分下方

2. **查找 "Artifacts" 标题**
   - 应该显示类似：
     ```
     Artifacts
     habitbloom-apk (X MB)
     ```

3. **点击 Artifact 名称下载**
   - 点击后会下载 ZIP 文件
   - 解压得到 APK

---

## 🆘 如果确实找不到 Artifacts

### 可能的原因 1：Artifacts 上传失败

**检查方法：**

1. **查看工作流日志**
   - 在运行记录页面
   - 找到 "Upload APK" 步骤
   - 点击查看详细日志

2. **检查是否有错误**
   - 如果显示红色 ❌，说明上传失败
   - 查看错误信息

**解决方法：**

- 重新运行工作流
- 检查 APK 文件路径是否正确
- 查看工作流配置

---

### 可能的原因 2：工作流还在运行

**检查方法：**

- 如果显示黄色 ⚠️，说明还在运行
- 等待完成后再查看

---

### 可能的原因 3：APK 文件路径错误

**检查方法：**

1. **查看 "Build APK" 步骤的日志**
   - 找到 APK 文件的实际路径
   - 例如：`bin/HabitBloom-1.0.0-debug.apk`

2. **检查工作流配置**
   - 确认 `path` 配置正确
   - 确认 APK 文件确实存在

---

## 🔧 替代方法：从日志中下载

如果 Artifacts 确实找不到，可以：

### 方法 1：检查工作流日志中的文件路径

1. **查看 "Build APK" 步骤**
2. **找到 APK 文件的完整路径**
3. **如果是在 GitHub Actions 中，文件在运行器上，无法直接下载**

### 方法 2：修改工作流添加下载链接

可以在工作流中添加一个步骤，输出 APK 的下载信息。

---

## 📝 检查清单

请确认以下内容：

- [ ] 工作流运行完成（显示绿色 ✓）
- [ ] 滚动到页面最底部
- [ ] 查看 "Summary" 部分下方
- [ ] "Upload APK" 步骤显示成功
- [ ] 没有错误信息

---

## 🚀 快速测试

### 测试 Artifacts 是否工作：

1. **重新运行工作流**
   - Actions → 选择工作流 → Run workflow

2. **等待完成**
   - 确保所有步骤都成功

3. **再次查看 Artifacts**
   - 滚动到最底部
   - 应该能看到 Artifact

---

## 💡 如果还是找不到

### 方案 1：查看工作流日志

1. 打开运行记录
2. 查看每个步骤的日志
3. 找到 APK 文件的实际位置
4. 检查 "Upload APK" 步骤是否有错误

### 方案 2：检查工作流配置

确认工作流文件中的 Upload 步骤存在：

```yaml
- name: Upload APK
  uses: actions/upload-artifact@v4
  with:
    name: habitbloom-apk
    path: bin/*.apk
```

### 方案 3：手动下载（如果是本地构建）

如果是在本地构建成功的，APK 在：

**Kivy 版本：**
```
HabitBloom/bin/HabitBloom-1.0.0-debug.apk
```

**PyQt5 版本：**
```
HabitBloom/android/HabitBloom/app/build/outputs/apk/debug/HabitBloom-1.0.0-debug.apk
```

---

## 📸 位置示意图

```
GitHub 仓库页面
├── Code
├── Issues
├── Pull requests
├── Actions  ← 点击这里
│   ├── 左侧：工作流列表
│   │   ├── Build HabitBloom APK
│   │   └── Build PyQt5 APK
│   └── 右侧：运行记录
│       └── 点击运行记录
│           ├── 顶部：步骤列表
│           ├── 中间：日志输出
│           └── 底部：Summary
│               └── Artifacts  ← 在这里！
```

---

## 🆘 需要帮助？

如果还是找不到，请提供：

1. **工作流运行状态**
   - 是成功（绿色 ✓）还是失败（红色 ❌）？

2. **"Upload APK" 步骤的状态**
   - 是否显示成功？

3. **页面截图**
   - 可以帮助我更好地定位问题

---

**记住：Artifacts 在页面最底部，需要向下滚动！** 📜
