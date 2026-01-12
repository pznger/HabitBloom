#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HabitBloom 配置检查脚本
检查 buildozer.spec 和项目文件是否配置正确
"""
import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    path = Path(filepath)
    exists = path.exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    if not exists:
        print(f"   错误: 文件不存在！")
    return exists

def check_directory_exists(dirpath, description):
    """检查目录是否存在"""
    path = Path(dirpath)
    exists = path.exists() and path.is_dir()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {dirpath}")
    if not exists:
        print(f"   错误: 目录不存在！")
    return exists

def check_buildozer_spec():
    """检查 buildozer.spec 配置"""
    print("\n" + "="*60)
    print("检查 buildozer.spec 配置")
    print("="*60)
    
    spec_file = Path("buildozer.spec")
    if not spec_file.exists():
        print("❌ buildozer.spec 文件不存在！")
        return False
    
    with open(spec_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = []
    
    # 检查必需配置项
    required_configs = [
        ("title = HabitBloom", "应用标题"),
        ("package.name = habitbloom", "包名"),
        ("source.main = main_kivy.py", "主入口文件"),
        ("requirements =", "依赖配置"),
        ("android.api =", "Android API"),
        ("android.minapi =", "Android 最低 API"),
    ]
    
    for config, desc in required_configs:
        if config in content:
            print(f"✅ {desc}: 已配置")
            checks.append(True)
        else:
            print(f"❌ {desc}: 未找到 '{config}'")
            checks.append(False)
    
    # 检查 requirements 格式
    if "requirements = " in content:
        print("⚠️  警告: requirements 行末尾有空格，可能导致问题")
        print("   建议: requirements = python3,kivy==2.3.1,pillow")
    
    # 检查主文件
    if "source.main = main_kivy.py" in content:
        if not Path("main_kivy.py").exists():
            print("❌ 错误: buildozer.spec 指定 main_kivy.py 但文件不存在")
            checks.append(False)
        else:
            print("✅ 主入口文件存在")
            checks.append(True)
    
    return all(checks)

def check_project_structure():
    """检查项目结构"""
    print("\n" + "="*60)
    print("检查项目结构")
    print("="*60)
    
    required_files = [
        ("main_kivy.py", "Kivy 主入口文件"),
        ("buildozer.spec", "Buildozer 配置文件"),
    ]
    
    required_dirs = [
        ("src", "源代码目录"),
        ("kivy_ui", "Kivy UI 目录"),
        ("src/database", "数据库模块"),
        ("src/managers", "业务逻辑模块"),
        ("kivy_ui/screens", "Kivy 屏幕组件"),
    ]
    
    all_ok = True
    
    for filepath, desc in required_files:
        if not check_file_exists(filepath, desc):
            all_ok = False
    
    for dirpath, desc in required_dirs:
        if not check_directory_exists(dirpath, desc):
            all_ok = False
    
    return all_ok

def check_imports():
    """检查关键导入是否正常"""
    print("\n" + "="*60)
    print("检查 Python 导入")
    print("="*60)
    
    try:
        # 检查 main_kivy.py 是否可以导入
        sys.path.insert(0, str(Path.cwd()))
        
        # 检查 Kivy
        try:
            import kivy
            print(f"✅ Kivy: {kivy.__version__}")
        except ImportError:
            print("❌ Kivy: 未安装（打包时会在云端安装）")
        
        # 检查关键模块
        modules_to_check = [
            ("src.database.db_manager", "数据库管理器"),
            ("src.managers.habit_manager", "习惯管理器"),
            ("kivy_ui.fonts", "字体模块"),
        ]
        
        for module, desc in modules_to_check:
            try:
                __import__(module)
                print(f"✅ {desc}: 导入成功")
            except ImportError as e:
                print(f"❌ {desc}: 导入失败 - {e}")
        
        return True
    except Exception as e:
        print(f"❌ 检查导入时出错: {e}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("  HabitBloom 配置检查工具")
    print("="*60)
    
    # 切换到项目目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    results = []
    
    # 检查项目结构
    results.append(("项目结构", check_project_structure()))
    
    # 检查 buildozer.spec
    results.append(("buildozer.spec", check_buildozer_spec()))
    
    # 检查导入（可选，不影响打包）
    try:
        check_imports()
    except:
        pass
    
    # 总结
    print("\n" + "="*60)
    print("检查结果总结")
    print("="*60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 所有检查通过！配置看起来正确。")
        print("\n下一步：")
        print("1. 上传项目到 GitHub")
        print("2. 在 Actions 中运行打包工作流")
    else:
        print("⚠️  发现问题，请根据上述错误修复配置。")
        print("\n常见问题：")
        print("- 确保所有必需文件都存在")
        print("- 检查 buildozer.spec 中的路径是否正确")
        print("- 确保 requirements 行没有多余空格")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
