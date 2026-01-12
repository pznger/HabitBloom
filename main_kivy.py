#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HabitBloom - Kivy 版本入口
用于安卓打包
"""
import os
import sys

# 设置环境变量（安卓兼容）
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

# 初始化中文字体（必须在导入其他 Kivy 模块之前）
try:
    from kivy_ui.fonts import init_fonts
    font_loaded = init_fonts()
    print(f"[HabitBloom] 字体初始化: {'成功' if font_loaded else '失败'}")
except Exception as e:
    print(f"[HabitBloom] 字体初始化异常: {e}")

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.properties import BooleanProperty
from kivy.clock import Clock

# 设置窗口大小（桌面调试用，手机上会自动全屏）
Window.size = (390, 844)

# 导入业务逻辑（复用 PyQt5 版本的）
sys.path.insert(0, os.path.dirname(__file__))
from src.database.db_manager import DatabaseManager
from src.managers.habit_manager import HabitManager
from src.managers.garden_manager import GardenManager
from src.managers.stats_manager import StatsManager

# 导入 Kivy UI
from kivy_ui.screens.garden_screen import GardenScreen
from kivy_ui.screens.habit_screen import HabitScreen
from kivy_ui.screens.stats_screen import StatsScreen
from kivy_ui.screens.settings_screen import SettingsScreen


class HabitBloomApp(App):
    """HabitBloom Kivy 应用"""
    
    dark_mode = BooleanProperty(False)
    
    def build(self):
        """构建应用"""
        self.title = 'HabitBloom'
        
        # 初始化管理器
        self.db = DatabaseManager()
        self.habit_manager = HabitManager()
        self.garden_manager = GardenManager()
        self.stats_manager = StatsManager()
        
        # 创建屏幕管理器
        self.sm = ScreenManager(transition=SlideTransition())
        
        # 添加屏幕
        self.garden_screen = GardenScreen(name='garden')
        self.habit_screen = HabitScreen(name='habits')
        self.stats_screen = StatsScreen(name='stats')
        self.settings_screen = SettingsScreen(name='settings')
        
        self.sm.add_widget(self.garden_screen)
        self.sm.add_widget(self.habit_screen)
        self.sm.add_widget(self.stats_screen)
        self.sm.add_widget(self.settings_screen)
        
        # 默认显示花园
        self.sm.current = 'garden'
        
        # 延迟刷新数据
        Clock.schedule_once(lambda dt: self.refresh_all(), 0.5)
        
        return self.sm
    
    def switch_screen(self, screen_name):
        """切换屏幕"""
        self.sm.current = screen_name
        # 刷新当前屏幕
        current = self.sm.current_screen
        if hasattr(current, 'refresh'):
            current.refresh()
    
    def refresh_all(self):
        """刷新所有屏幕"""
        for screen in [self.garden_screen, self.habit_screen, 
                       self.stats_screen, self.settings_screen]:
            if hasattr(screen, 'refresh'):
                screen.refresh()
    
    def on_dark_mode(self, instance, value):
        """深色模式切换"""
        # 可以在这里更新主题颜色
        pass


if __name__ == '__main__':
    HabitBloomApp().run()
