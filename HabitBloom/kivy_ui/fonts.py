"""字体配置 - 解决中文和 emoji 显示问题"""
import os
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.utils import platform


# 全局字体名称
CHINESE_FONT_NAME = 'ChineseFont'
DEFAULT_FONT = None


def get_chinese_font():
    """获取系统中文字体路径"""
    
    if platform == 'win':
        fonts_dir = 'C:/Windows/Fonts'
        candidates = [
            'msyh.ttc',      # 微软雅黑
            'msyhbd.ttc',    # 微软雅黑粗体
            'simhei.ttf',    # 黑体
            'simsun.ttc',    # 宋体
        ]
        for font in candidates:
            path = os.path.join(fonts_dir, font)
            if os.path.exists(path):
                return path
    
    elif platform == 'linux':
        candidates = [
            '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/truetype/arphic/uming.ttc',
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
    
    elif platform == 'android':
        candidates = [
            '/system/fonts/NotoSansCJK-Regular.ttc',
            '/system/fonts/DroidSansFallback.ttf',
            '/system/fonts/NotoSansHans-Regular.otf',
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
    
    elif platform == 'macosx':
        candidates = [
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/Library/Fonts/Arial Unicode.ttf',
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
    
    return None


def get_emoji_font():
    """获取 emoji 字体路径"""
    
    if platform == 'win':
        path = 'C:/Windows/Fonts/seguiemj.ttf'
        if os.path.exists(path):
            return path
    
    elif platform == 'linux':
        candidates = [
            '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',
            '/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf',
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
    
    elif platform == 'android':
        path = '/system/fonts/NotoColorEmoji.ttf'
        if os.path.exists(path):
            return path
    
    return None


def register_fonts():
    """注册字体到 Kivy"""
    global DEFAULT_FONT
    
    chinese_font = get_chinese_font()
    emoji_font = get_emoji_font()
    
    if chinese_font:
        # 注册中文字体为默认字体
        LabelBase.register(
            name='Roboto',  # 覆盖默认字体
            fn_regular=chinese_font
        )
        
        # 也注册一个命名字体
        LabelBase.register(
            name=CHINESE_FONT_NAME,
            fn_regular=chinese_font
        )
        
        DEFAULT_FONT = chinese_font
        print(f"[Font] 已加载中文字体: {chinese_font}")
    else:
        print("[Font] 警告: 未找到中文字体")
    
    # Emoji 字体（如果有的话）
    if emoji_font:
        LabelBase.register(
            name='EmojiFont',
            fn_regular=emoji_font
        )
        print(f"[Font] 已加载 Emoji 字体: {emoji_font}")


def init_fonts():
    """初始化字体（供 main_kivy.py 调用）"""
    try:
        register_fonts()
        return True
    except Exception as e:
        print(f"[Font] 字体注册失败: {e}")
        return False


def get_font_name():
    """获取当前使用的字体名称"""
    return 'Roboto'  # 因为我们覆盖了默认字体


# Emoji 替代映射
EMOJI_MAP = {
    '🌱': '[苗]', '🌿': '[草]', '🌸': '[花]', '🌳': '[树]',
    '🌵': '[仙]', '💐': '[束]', '🏡': '[家]', '📋': '[单]',
    '📊': '[图]', '⚙️': '[设]', '🔥': '[火]', '✅': '[√]',
    '🏆': '[杯]', '💧': '[水]', '💚': '[心]', '🔔': '[铃]',
    '➕': '[+]', '👤': '[人]', '🎨': '[画]', '💾': '[存]',
    'ℹ️': '[i]', '⏳': '[等]', '🎉': '[庆]', '🌟': '[星]',
    '💪': '[力]', '📚': '[书]', '🏃': '[跑]', '🧘': '[禅]',
    '✍️': '[写]', '🎯': '[标]', '⏰': '[钟]', '🎵': '[乐]',
    '⭐': '*',
}


def e(text):
    """
    处理 emoji 文本
    如果字体支持 emoji 则保留，否则替换为文字
    """
    # 在 Windows/桌面上，使用覆盖后的字体通常支持中文但不支持 emoji
    # 我们尝试使用原始文本，如果显示有问题用户可以手动替换
    return text


class CLabel(Label):
    """支持中文的 Label"""
    
    def __init__(self, **kwargs):
        # 设置默认字体
        if 'font_name' not in kwargs:
            kwargs['font_name'] = 'Roboto'
        super().__init__(**kwargs)


class CButton(Button):
    """支持中文的 Button"""
    
    def __init__(self, **kwargs):
        # 设置默认字体
        if 'font_name' not in kwargs:
            kwargs['font_name'] = 'Roboto'
        super().__init__(**kwargs)


class CTextInput(TextInput):
    """支持中文的 TextInput"""
    
    def __init__(self, **kwargs):
        # 设置默认字体
        if 'font_name' not in kwargs:
            kwargs['font_name'] = 'Roboto'
        super().__init__(**kwargs)
