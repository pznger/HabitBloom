"""设置屏幕"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.app import App
from kivy.utils import platform
import os

from ..base import BaseScreen, Card, COLORS
from ..fonts import CLabel, CButton, CTextInput, get_font_name
from src.utils.constants import APP_NAME, APP_VERSION


class SettingsSection(Card):
    """设置区块"""
    
    def __init__(self, title, icon='', **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.spacing = dp(10)
        
        # 标题
        title_lbl = CLabel(
            text=f'{icon} {title}' if icon else title,
            font_size=dp(13),
            bold=True,
            size_hint_y=None,
            height=dp(25),
            halign='left',
            color=COLORS['text']
        )
        title_lbl.bind(size=title_lbl.setter('text_size'))
        self.add_widget(title_lbl)


class SettingRow(BoxLayout):
    """设置行"""
    
    def __init__(self, label, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(40)
        
        lbl = CLabel(text=label, font_size=dp(12), halign='left', color=COLORS['text'])
        lbl.bind(size=lbl.setter('text_size'))
        self.add_widget(lbl)


class SettingsScreen(BaseScreen):
    """设置屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
    
    def _build_ui(self):
        # 标题
        title = CLabel(
            text='设置',
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            halign='left',
            color=COLORS['text']
        )
        title.bind(size=title.setter('text_size'))
        self.content.add_widget(title)
        
        # 滚动内容
        scroll = ScrollView(size_hint=(1, 1))
        
        self.settings_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            size_hint_y=None,
            padding=[0, dp(5)]
        )
        self.settings_layout.bind(minimum_height=self.settings_layout.setter('height'))
        
        scroll.add_widget(self.settings_layout)
        self.content.add_widget(scroll)
        
        self._build_sections()
    
    def _build_sections(self):
        """构建设置区块"""
        # 用户信息
        user_section = SettingsSection('用户信息', '◆')
        user_section.height = dp(120)
        
        name_row = SettingRow('昵称')
        self.name_input = CTextInput(
            text='',
            multiline=False,
            size_hint_x=0.6,
            height=dp(35),
            size_hint_y=None
        )
        name_row.add_widget(self.name_input)
        user_section.add_widget(name_row)
        
        save_btn = CButton(
            text='保存',
            size_hint_y=None,
            height=dp(35),
            background_color=COLORS['primary_light'],
            background_normal=''
        )
        save_btn.bind(on_press=self._save_user)
        user_section.add_widget(save_btn)
        
        self.settings_layout.add_widget(user_section)
        
        # 外观
        theme_section = SettingsSection('外观', '◐')
        theme_section.height = dp(70)
        
        dark_row = SettingRow('深色模式')
        self.dark_switch = Switch(active=False, size_hint_x=None, width=dp(60))
        self.dark_switch.bind(active=self._on_dark_toggle)
        dark_row.add_widget(self.dark_switch)
        theme_section.add_widget(dark_row)
        
        self.settings_layout.add_widget(theme_section)
        
        # 数据管理
        data_section = SettingsSection('数据管理', '▤')
        data_section.height = dp(130)
        
        export_row = BoxLayout(size_hint_y=None, height=dp(35))
        export_lbl = CLabel(text='导出数据', font_size=dp(12), halign='left', color=COLORS['text'])
        export_lbl.bind(size=export_lbl.setter('text_size'))
        export_row.add_widget(export_lbl)
        
        export_btn = CButton(
            text='导出',
            size_hint_x=0.3,
            background_color=(0.13, 0.59, 0.95, 1),
            background_normal=''
        )
        export_btn.bind(on_press=self._export_data)
        export_row.add_widget(export_btn)
        data_section.add_widget(export_row)
        
        import_row = BoxLayout(size_hint_y=None, height=dp(35))
        import_lbl = CLabel(text='恢复数据', font_size=dp(12), halign='left', color=COLORS['text'])
        import_lbl.bind(size=import_lbl.setter('text_size'))
        import_row.add_widget(import_lbl)
        
        import_btn = CButton(
            text='导入',
            size_hint_x=0.3,
            background_color=COLORS['accent'],
            background_normal=''
        )
        import_btn.bind(on_press=self._import_data)
        import_row.add_widget(import_btn)
        data_section.add_widget(import_row)
        
        self.settings_layout.add_widget(data_section)
        
        # 关于
        about_section = SettingsSection('关于', 'i')
        about_section.height = dp(100)
        
        app_name = CLabel(
            text=f'{APP_NAME}',
            font_size=dp(15),
            bold=True,
            size_hint_y=None,
            height=dp(25),
            halign='left',
            color=COLORS['text']
        )
        app_name.bind(size=app_name.setter('text_size'))
        about_section.add_widget(app_name)
        
        version = CLabel(
            text=f'版本 {APP_VERSION}',
            font_size=dp(11),
            size_hint_y=None,
            height=dp(20),
            halign='left',
            color=COLORS['text_secondary']
        )
        version.bind(size=version.setter('text_size'))
        about_section.add_widget(version)
        
        desc = CLabel(
            text='让习惯如花般绽放',
            font_size=dp(11),
            size_hint_y=None,
            height=dp(20),
            halign='left',
            color=COLORS['text_secondary']
        )
        desc.bind(size=desc.setter('text_size'))
        about_section.add_widget(desc)
        
        self.settings_layout.add_widget(about_section)
    
    def refresh(self):
        """刷新设置"""
        app = App.get_running_app()
        if app:
            user = app.db.get_user()
            if user:
                self.name_input.text = user.username
    
    def _save_user(self, *args):
        """保存用户信息"""
        app = App.get_running_app()
        if app:
            user = app.db.get_user()
            if user:
                user.username = self.name_input.text.strip() or '用户'
                app.db.update_user(user)
                self._show_message('已保存！')
    
    def _on_dark_toggle(self, switch, active):
        """深色模式切换"""
        app = App.get_running_app()
        if app:
            app.dark_mode = active
    
    def _export_data(self, *args):
        """导出数据"""
        app = App.get_running_app()
        if app:
            from src.utils.helpers import get_backup_dir, export_data_to_json
            from datetime import datetime
            
            backup_dir = get_backup_dir()
            filename = f"habitbloom_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(backup_dir, filename)
            
            data = app.db.export_all_data()
            if export_data_to_json(data, filepath):
                self._show_message(f'已导出到:\n{backup_dir}')
            else:
                self._show_message('导出失败')
    
    def _import_data(self, *args):
        """导入数据"""
        self._show_message('请使用文件管理器\n选择备份文件导入')
    
    def _show_message(self, text):
        """显示消息弹窗"""
        content = BoxLayout(orientation='vertical', padding=[dp(20)])
        
        msg = CLabel(text=text, font_size=dp(13), halign='center', color=COLORS['text'])
        content.add_widget(msg)
        
        btn = CButton(text='确定', size_hint_y=None, height=dp(40),
                    background_color=COLORS['primary_light'], background_normal='')
        
        popup = Popup(title='', content=content, size_hint=(0.8, 0.3), separator_height=0,
                     title_font=get_font_name())
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        
        popup.open()
