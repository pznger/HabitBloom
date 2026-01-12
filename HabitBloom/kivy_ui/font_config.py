"""字体配置 - 解决中文显示问题"""
import os
import sys
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivy.utils import platform


def get_chinese_font():
    """获取中文字体路径"""
    
    # 项目内置字体（优先）
    project_font = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'NotoSansSC-Regular.ttf')
    if os.path.exists(project_font):
        return os.path.abspath(project_font)
    
    # Windows 系统字体
    if platform == 'win':
        font_paths = [
            'C:/Windows/Fonts/msyh.ttc',      # 微软雅黑
            'C:/Windows/Fonts/msyhbd.ttc',    # 微软雅黑粗体
            'C:/Windows/Fonts/simhei.ttf',    # 黑体
            'C:/Windows/Fonts/simsun.ttc',    # 宋体
        ]
        for path in font_paths:
            if os.path.exists(path):
                return path
    
    # Linux 系统字体
    elif platform == 'linux':
        font_paths = [
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        ]
        for path in font_paths:
            if os.path.exists(path):
                return path
    
    # macOS 系统字体
    elif platform == 'macosx':
        font_paths = [
            '/System/Library/Fonts/PingFang.ttc',
            '/Library/Fonts/Arial Unicode.ttf',
        ]
        for path in font_paths:
            if os.path.exists(path):
                return path
    
    # Android
    elif platform == 'android':
        font_paths = [
            '/system/fonts/NotoSansCJK-Regular.ttc',
            '/system/fonts/DroidSansFallback.ttf',
        ]
        for path in font_paths:
            if os.path.exists(path):
                return path
    
    return None


def setup_chinese_font():
    """设置中文字体"""
    font_path = get_chinese_font()
    
    if font_path:
        print(f"[Font] 使用字体: {font_path}")
        
        # 注册为默认字体
        LabelBase.register(
            name='Roboto',  # 替换默认字体名
            fn_regular=font_path
        )
        
        # 也注册一个 ChineseFont 名称备用
        LabelBase.register(
            name='ChineseFont',
            fn_regular=font_path
        )
        
        return True
    else:
        print("[Font] 警告: 未找到中文字体，中文可能无法正常显示")
        return False


# Emoji 字体（如果需要单独处理）
def get_emoji_font():
    """获取 Emoji 字体"""
    if platform == 'win':
        emoji_path = 'C:/Windows/Fonts/seguiemj.ttf'  # Segoe UI Emoji
        if os.path.exists(emoji_path):
            return emoji_path
    return None
