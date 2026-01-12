# 🔧 修复 libtool 错误

## ❌ 问题

构建失败，错误信息：
```
configure.ac:215: error: possibly undefined macro: LT_SYS_SYMBOL_USCORE
autoreconf: error: /usr/bin/autoconf failed with exit status: 1
```

## ✅ 已应用的修复

### 1. 安装 libtool-bin 和 m4

在工作流中添加了：
- `libtool-bin` - libtool 的二进制工具
- `m4` - 宏处理器（autoconf 需要）

### 2. 更新 NDK 版本

将 `buildozer.spec` 中的 NDK 版本从 `25b` 更新到 `27c`：
- NDK 25b 可能太旧，导致兼容性问题
- NDK 27c 是更新的版本，应该更稳定

## 🚀 下一步

### 1. 提交更改

```bash
git add .github/workflows/build-apk.yml
git add buildozer.spec
git commit -m "修复 libtool 错误：添加 libtool-bin 和更新 NDK 版本"
git push
```

### 2. 重新运行工作流

- Actions → Build HabitBloom APK → Run workflow

### 3. 如果仍然失败

可能需要：
- 检查 NDK 27c 是否可用（如果不可用，尝试其他版本）
- 或者尝试移除 pyjnius 依赖（如果不需要）

---

**已修复，请重新运行！** 🚀
