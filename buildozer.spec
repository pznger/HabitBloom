[app]

# HabitBloom - 习惯养成应用
title = HabitBloom
package.name = habitbloom
package.domain = org.habitbloom

# 应用源码目录
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db

# 主入口文件
source.main = main_kivy.py

# 排除的文件和目录（PyQt5相关）
source.exclude_dirs = __pycache__, .git, .vscode, .idea
source.exclude_patterns = main.py, *_qt.py

# 版本信息
version = 1.0.0

# 应用依赖
# 注意：sqlite3 是 Python 标准库，不需要单独安装
requirements = python3,kivy==2.3.1,pillow

# 权限
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, VIBRATE, RECEIVE_BOOT_COMPLETED

# Android API 版本
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# 架构
android.archs = arm64-v8a, armeabi-v7a

# 应用图标（需要创建）
# icon.filename = %(source.dir)s/assets/icon.png

# 启动画面
# presplash.filename = %(source.dir)s/assets/presplash.png
presplash.color = #4CAF50

# 屏幕方向
orientation = portrait

# 全屏
fullscreen = 0

# Android 特定设置
android.accept_sdk_license = True
android.release_artifact = apk

# 日志级别
log_level = 2

# Buildozer 缓存目录
# buildozer.dir = ./.buildozer

[buildozer]
log_level = 2
warn_on_root = 1

# Android 签名配置（发布版本需要）
# android.keystore = ~/keystores/habitbloom.keystore
# android.keyalias = habitbloom
