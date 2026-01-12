# 📋 GitHub Actions 工作流说明

## ✅ 已修复的问题

### 问题：GitHub Releases requires a tag

**原因：** `action-gh-release` 需要 Git 标签才能创建 Release。

**解决方案：**
- 修改为只在有标签时创建 Release
- 如果没有标签，只上传 Artifacts（APK 文件）

---

## 🎯 工作流说明

### 1. Build HabitBloom APK (Kivy 版本)

**文件：** `.github/workflows/build-apk.yml`

**触发条件：**
- 手动触发（workflow_dispatch）
- 推送到 main/master 分支时（如果相关文件有变化）

**功能：**
- ✅ 构建 Kivy 版本的 APK
- ✅ 上传 APK 到 Artifacts
- ✅ 如果有标签，自动创建 Release

### 2. Build PyQt5 APK

**文件：** `.github/workflows/build-pyqt5-apk.yml`

**触发条件：**
- 手动触发（workflow_dispatch）
- 推送到 main/master 分支时（如果相关文件有变化）

**功能：**
- ✅ 构建 PyQt5 版本的 APK
- ✅ 上传 APK 到 Artifacts

---

## 📦 下载 APK

### 方法 1：从 Artifacts 下载（推荐）

1. 打开 GitHub 仓库 → Actions 标签
2. 点击最新的运行记录
3. 滚动到底部，在 "Artifacts" 部分下载 APK

**优点：**
- ✅ 无需标签
- ✅ 每次运行都有 Artifacts
- ✅ 简单直接

### 方法 2：从 Release 下载

如果需要创建 Release：

1. **创建 Git 标签**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **自动创建 Release**
   - 推送标签后，工作流会自动运行
   - 如果有标签，会自动创建 Release 并上传 APK

3. **下载 Release**
   - 打开仓库 → Releases
   - 下载 APK 文件

**优点：**
- ✅ 版本管理清晰
- ✅ 可以添加 Release 说明
- ✅ 适合正式发布

---

## 🔧 工作流配置

### 触发条件

```yaml
on:
  workflow_dispatch:  # 手动触发
  push:
    branches: [ main, master ]
    paths:
      - 'main.py'  # 只有这些文件变化时才触发
```

### Artifacts 保留时间

- 默认保留 90 天（GitHub 默认）
- 可以在 Artifacts 页面手动删除

### Release 创建条件

```yaml
- name: Create Release (only if tag exists)
  if: startsWith(github.ref, 'refs/tags/')
```

只有在推送标签时才会创建 Release。

---

## 🚀 使用指南

### 日常打包（推荐）

1. **手动触发**
   - 打开 Actions → 选择工作流 → Run workflow

2. **下载 APK**
   - 等待完成 → 在 Artifacts 中下载

### 正式发布

1. **创建标签**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **自动创建 Release**
   - 工作流自动运行
   - 自动创建 Release 并上传 APK

3. **编辑 Release 说明**
   - 打开 Releases 页面
   - 编辑 Release 说明

---

## ⚠️ 注意事项

1. **Artifacts 限制**
   - 每个 Artifact 最大 10GB
   - 免费账户有存储限制

2. **Release 需要标签**
   - 没有标签时不会创建 Release
   - 这是正常的，不会影响 APK 下载

3. **工作流运行时间**
   - 首次运行：15-30 分钟（下载依赖）
   - 后续运行：10-20 分钟

---

## 🆘 常见问题

### Q: 为什么没有创建 Release？

**A:** Release 只在有标签时创建。如果没有标签：
- ✅ APK 仍然会出现在 Artifacts 中
- ✅ 可以正常下载
- ⚠️ 不会创建 Release（这是正常的）

### Q: 如何创建标签？

```bash
# 创建标签
git tag v1.0.0

# 推送标签
git push origin v1.0.0
```

### Q: Artifacts 在哪里？

- 打开 Actions → 点击运行记录 → 滚动到底部 → Artifacts

### Q: 可以同时运行两个工作流吗？

- ✅ 可以，它们是独立的
- ✅ 会生成两个不同的 APK（Kivy 和 PyQt5）

---

## 📚 参考

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Artifacts 文档](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)
- [Releases 文档](https://docs.github.com/en/repositories/releasing-projects-on-github)

---

**总结：APK 文件会始终出现在 Artifacts 中，可以正常下载。Release 是可选的，需要标签才会创建。** ✅
