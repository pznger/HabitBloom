# 📦 Artifacts 查找详细指南

## 🎯 关键提示

**Artifacts 在页面最底部，需要向下滚动！**

很多用户找不到是因为没有滚动到底部。

---

## 📍 详细步骤（一步一步）

### 第 1 步：进入 Actions 页面

1. 打开你的 GitHub 仓库
   - 网址类似：`https://github.com/你的用户名/仓库名`

2. 点击顶部的 **"Actions"** 标签
   - 在导航栏中，通常在 "Pull requests" 和 "Projects" 之间

### 第 2 步：选择工作流

1. 在左侧边栏，你会看到工作流列表：
   - `Build HabitBloom APK` (Kivy 版本)
   - `Build PyQt5 APK` (PyQt5 版本)

2. 点击你运行的工作流名称

### 第 3 步：找到运行记录

1. 在右侧，你会看到运行记录列表
2. 找到最新的运行（通常在最上面）
3. 应该显示：
   - ✅ 绿色 ✓ = 成功
   - ⚠️ 黄色 ⚠️ = 进行中
   - ❌ 红色 ❌ = 失败

4. **点击运行记录**（点击运行记录的那一行）

### 第 4 步：进入运行详情

1. 现在你进入了运行详情页面
2. 你会看到：
   - 顶部：步骤列表（Checkout code, Set up Python, Build APK, Upload APK 等）
   - 中间：日志输出
   - **底部：Summary 和 Artifacts** ← **重要！**

### 第 5 步：找到 Artifacts（关键！）

**⚠️ 重要：Artifacts 在页面最底部！**

1. **向下滚动页面**
   - 一直滚动到最底部
   - 不要只看顶部和中间

2. **找到 "Summary" 部分**
   - 在页面最底部
   - 显示工作流摘要信息

3. **在 Summary 下方，找到 "Artifacts" 部分**
   - 应该显示类似：
     ```
     Artifacts
     ┌─────────────────────────────┐
     │ habitbloom-apk               │
     │ 15.2 MB                      │
     │ [Download]                   │
     └─────────────────────────────┘
     ```

4. **点击 Artifact 名称或 Download 按钮**
   - 会下载一个 ZIP 文件
   - 解压后就是 APK 文件

---

## 🔍 如果还是找不到

### 检查 1：确认工作流已完成

- ✅ 所有步骤都显示绿色 ✓
- ❌ 如果有红色 ❌，说明有步骤失败

### 检查 2：查看 "Upload APK" 步骤

1. 在步骤列表中，找到 **"Upload APK"** 步骤
2. 点击查看详细日志
3. 检查是否显示：
   - ✅ "Uploaded artifact" = 成功
   - ❌ 错误信息 = 失败

### 检查 3：确认文件路径

**Kivy 版本工作流：**
- 路径：`bin/*.apk`
- 如果 APK 不在 `bin/` 目录，上传会失败

**PyQt5 版本工作流：**
- 路径：`android/**/*.apk`
- 如果 APK 不在 `android/` 目录，上传会失败

---

## 🛠️ 排查步骤

### 步骤 1：检查工作流日志

1. 打开运行记录
2. 查看 "Build APK" 步骤的日志
3. 找到类似这样的输出：
   ```
   ✅ 构建成功
   -rw-r--r-- 1 user user 15M Jan 12 16:00 bin/HabitBloom-1.0.0-debug.apk
   ```
4. 确认 APK 文件确实生成了

### 步骤 2：检查 Upload 步骤

1. 查看 "Upload APK" 步骤
2. 应该显示：
   ```
   Uploaded artifact 'habitbloom-apk' (15.2 MB)
   ```
3. 如果没有这个输出，说明上传失败

### 步骤 3：检查工作流配置

确认工作流文件中有 Upload 步骤：

```yaml
- name: Upload APK
  uses: actions/upload-artifact@v4
  with:
    name: habitbloom-apk
    path: bin/*.apk
```

---

## 💡 常见问题

### Q: 为什么我看不到 Artifacts？

**A:** 可能的原因：
1. 没有滚动到页面最底部
2. "Upload APK" 步骤失败了
3. APK 文件路径不正确
4. 工作流还在运行中

### Q: Upload APK 步骤显示失败怎么办？

**A:** 
1. 查看错误信息
2. 检查 APK 文件路径是否正确
3. 确认 APK 文件确实存在
4. 重新运行工作流

### Q: 可以手动下载 APK 吗？

**A:** 
- 如果是在 GitHub Actions 中构建，只能通过 Artifacts 下载
- 如果是在本地构建，APK 在项目目录中

---

## 🚀 快速验证

### 测试 Artifacts 是否工作：

1. **重新运行工作流**
   ```
   Actions → 选择工作流 → Run workflow → Run workflow
   ```

2. **等待完成**
   - 确保所有步骤都成功（绿色 ✓）

3. **立即查看 Artifacts**
   - 滚动到页面最底部
   - 应该能看到 Artifact

---

## 📸 视觉指南

```
GitHub 仓库页面
│
├─ [Code] [Issues] [Pull requests] [Actions] ← 点击这里
│
Actions 页面
│
├─ 左侧边栏             右侧内容区
│  ├─ Build HabitBloom  │ 运行记录列表
│  │  APK               │  ├─ ✓ Run #123 (最新)
│  └─ Build PyQt5 APK   │  ├─ ✓ Run #122
│                        │  └─ ✓ Run #121
│
点击运行记录进入详情
│
运行详情页面
│
├─ 顶部：步骤列表
│  ├─ ✓ Checkout code
│  ├─ ✓ Set up Python
│  ├─ ✓ Build APK
│  └─ ✓ Upload APK
│
├─ 中间：日志输出
│  (各种构建日志)
│
└─ 底部：Summary ← 滚动到这里！
    │
    └─ Artifacts ← APK 在这里！
        └─ habitbloom-apk (15.2 MB) [Download]
```

---

## ✅ 总结

**关键点：**
1. ✅ Artifacts 在页面**最底部**
2. ✅ 需要**向下滚动**才能看到
3. ✅ 在 "Summary" 部分下方
4. ✅ 确保 "Upload APK" 步骤成功

**如果还是找不到，请：**
1. 截图给我看运行详情页面的底部
2. 告诉我 "Upload APK" 步骤的状态
3. 或者告诉我你看到的具体内容

---

**记住：向下滚动，向下滚动，向下滚动！** 📜⬇️
