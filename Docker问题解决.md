# 🔧 Docker 问题解决指南

## 错误：500 Internal Server Error

这个错误通常表示 **Docker Desktop 未正确启动**。

---

## 🚀 快速修复

### 方法一：自动修复脚本

**Windows 用户：**
```cmd
修复Docker.bat
```

### 方法二：手动修复

#### 步骤 1：检查 Docker Desktop 是否运行

1. 查看系统托盘（右下角）
2. 找到 Docker 图标（鲸鱼图标）
3. 如果图标在闪烁或显示错误 → Docker 未启动

#### 步骤 2：启动 Docker Desktop

1. 在开始菜单搜索 "Docker Desktop"
2. 点击启动
3. **等待 30-60 秒**，直到：
   - 系统托盘图标不再闪烁
   - 图标显示为正常状态

#### 步骤 3：验证 Docker 运行

打开命令行，运行：
```cmd
docker info
```

如果显示 Docker 信息 → ✅ 正常运行
如果显示错误 → 继续下面的步骤

---

## 🔍 常见问题及解决

### 问题 1：Docker Desktop 启动失败

**症状**：点击启动后立即关闭或报错

**解决方法**：
1. **重启电脑**
2. **检查虚拟化是否启用**：
   - 重启时进入 BIOS（通常是 F2、F12、Del）
   - 找到 "Virtualization" 或 "Intel VT-x" / "AMD-V"
   - 确保已启用（Enabled）
3. **重新安装 Docker Desktop**

### 问题 2：WSL 2 后端错误

**症状**：提示 "WSL 2 installation is incomplete"

**解决方法**：
```powershell
# 以管理员身份运行 PowerShell
wsl --update
wsl --set-default-version 2
```

然后重启 Docker Desktop

### 问题 3：端口被占用

**症状**：Docker 启动但无法连接

**解决方法**：
1. 打开 Docker Desktop
2. Settings → Resources → Advanced
3. 修改端口范围
4. 点击 "Apply & Restart"

### 问题 4：Docker 服务未启动

**解决方法**：
```cmd
# 以管理员身份运行
net start com.docker.service
```

或者：
1. 打开"服务"（services.msc）
2. 找到 "Docker Desktop Service"
3. 右键 → 启动

---

## ✅ 验证 Docker 是否正常

运行以下命令验证：

```cmd
# 1. 检查版本
docker --version

# 2. 检查守护进程
docker info

# 3. 测试运行容器
docker run hello-world
```

如果三个命令都成功 → Docker 完全正常！

---

## 🆘 如果还是不行

### 完全重新安装 Docker Desktop

1. **卸载 Docker Desktop**
   - 控制面板 → 程序和功能
   - 卸载 Docker Desktop

2. **清理残留文件**
   ```cmd
   # 删除 Docker 数据（可选）
   rmdir /s "C:\ProgramData\Docker"
   rmdir /s "%USERPROFILE%\.docker"
   ```

3. **重启电脑**

4. **重新安装**
   - 下载最新版：https://www.docker.com/products/docker-desktop/
   - 安装并重启

5. **启动并等待**
   - 启动 Docker Desktop
   - 等待完全启动（系统托盘图标稳定）

---

## 📋 检查清单

打包前确认：

- [ ] Docker Desktop 已安装
- [ ] Docker Desktop 正在运行（系统托盘图标正常）
- [ ] `docker --version` 可以运行
- [ ] `docker info` 可以运行
- [ ] `docker run hello-world` 可以运行

---

## 🎯 推荐流程

1. **运行修复脚本**
   ```cmd
   修复Docker.bat
   ```

2. **如果还是不行，手动检查**
   - 确保 Docker Desktop 正在运行
   - 等待 30 秒让 Docker 完全启动
   - 运行 `docker info` 验证

3. **重新运行打包脚本**
   ```cmd
   python docker_build.py
   ```

---

## 💡 替代方案

如果 Docker 一直有问题，可以使用 **GitHub Actions 云端打包**：

```cmd
python github_actions_build.py
```

完全不需要 Docker，在云端自动打包！

---

祝您顺利解决问题！🌱
