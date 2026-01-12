# 🔧 解决 GitHub 访问问题

## ❌ 问题描述

Briefcase 无法从 GitHub 克隆模板仓库：
- 无法连接到 `github.com`
- 连接超时
- 网络限制

---

## 🚀 解决方案

### 方案 1：使用代理（推荐，如果有代理）

#### 设置 Git 代理

```bash
# 设置 HTTP 代理（替换为你的代理地址和端口）
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 设置环境变量
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890

# 然后重新运行
briefcase create android
```

#### 取消代理（如果需要）

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

### 方案 2：使用 GitHub Actions（最推荐，完全避免网络问题）

**这是最可靠的方案！** 在云端运行，完全避免本地网络问题。

#### 步骤：

1. **提交代码到 GitHub**
   ```bash
   git add .
   git commit -m "Add PyQt5 Android build"
   git push
   ```

2. **在 GitHub 上触发打包**
   - 打开仓库 → Actions 标签
   - 选择 "Build PyQt5 APK"
   - 点击 "Run workflow"

3. **等待并下载 APK**
   - 等待 15-30 分钟
   - 在 Artifacts 中下载 APK

**优势：**
- ✅ 云端运行，网络稳定
- ✅ 自动下载所有依赖
- ✅ 无需本地配置
- ✅ 完全免费

---

### 方案 3：手动下载模板（高级）

#### 步骤 1：手动下载模板

1. **访问模板仓库**
   - 使用浏览器或代理访问：
   - https://github.com/beeware/briefcase-android-gradle-template
   - 或使用镜像站点

2. **下载 ZIP 文件**
   - 点击 "Code" → "Download ZIP"
   - 解压到临时目录

3. **配置 Briefcase 使用本地模板**

创建或编辑 `%USERPROFILE%\.briefcase\briefcase.toml`：

```toml
[tool.briefcase]
template = "file:///C:/path/to/briefcase-android-gradle-template"
```

**注意：** 这需要修改 Briefcase 的配置，可能比较复杂。

---

### 方案 4：使用 GitHub 镜像（如果可用）

#### 配置 Git 使用镜像

```bash
# 使用 GitHub 镜像（如果可用）
git config --global url."https://mirror.ghproxy.com/https://github.com/".insteadOf "https://github.com/"
```

**注意：** 镜像可能不稳定，需要根据实际情况调整。

---

### 方案 5：使用 VPN 或加速工具

如果其他方案不可行：

1. **使用 VPN 连接到稳定的网络**
2. **使用网络加速工具**
3. **在非高峰时段重试**

---

## 🛠️ 快速修复脚本

运行 `修复GitHub访问.bat` 脚本，可以：
- 配置 Git 代理
- 提供手动下载指南
- 推荐使用 GitHub Actions

---

## 📋 推荐方案对比

| 方案 | 难度 | 可靠性 | 推荐度 |
|------|------|--------|--------|
| GitHub Actions | ⭐ 简单 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 使用代理 | ⭐⭐ 中等 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 手动下载 | ⭐⭐⭐⭐ 困难 | ⭐⭐⭐ | ⭐⭐ |
| VPN/加速 | ⭐⭐ 中等 | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 最佳实践

**如果网络不稳定，强烈推荐使用 GitHub Actions：**

1. ✅ 完全避免本地网络问题
2. ✅ 自动处理所有依赖下载
3. ✅ 无需配置代理或 VPN
4. ✅ 打包完成后直接下载 APK

**步骤：**
1. 提交代码到 GitHub（可以使用 Git 客户端或网页上传）
2. 在 Actions 中运行工作流
3. 等待完成并下载 APK

---

## 🆘 如果所有方案都失败

**最后的选择：**

1. **使用手机热点**
   - 某些网络环境下，手机热点可能可以访问 GitHub

2. **更换网络环境**
   - 使用不同的网络（如移动网络、公共 Wi-Fi）

3. **联系网络管理员**
   - 如果是公司/学校网络，可能需要申请访问权限

---

## 📚 参考资源

- [Git 代理配置](https://git-scm.com/docs/git-config)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Briefcase 文档](https://briefcase.readthedocs.io/)

---

**强烈推荐：使用 GitHub Actions 云端打包，完全避免网络问题！** 🚀
