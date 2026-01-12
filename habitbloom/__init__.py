"""
HabitBloom - 让习惯如花般绽放
个人习惯养成应用
Briefcase 入口点
"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

# 直接导入并运行 main.py 中的主函数
# 由于 Briefcase 会将所有 sources 中的文件复制到应用包中，
# main.py 应该可以直接导入
try:
    # 尝试直接导入 main 模块
    import main
    if hasattr(main, 'main'):
        main.main()
    else:
        raise ImportError("main.py 中没有找到 main() 函数")
except ImportError:
    # 如果直接导入失败，使用 importlib
    import importlib.util
    main_path = os.path.join(project_root, 'main.py')
    if os.path.exists(main_path):
        spec = importlib.util.spec_from_file_location("main", main_path)
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        main_module.main()
    else:
        raise RuntimeError(f"找不到 main.py 文件: {main_path}")
