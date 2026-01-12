"""Kivy 基础组件"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import StringProperty, NumericProperty
from kivy.metrics import dp

from .fonts import e, get_font_name, CLabel, CButton


# 主题颜色
COLORS = {
    'primary': (0.18, 0.49, 0.20, 1),       # #2E7D32
    'primary_light': (0.30, 0.69, 0.31, 1),  # #4CAF50
    'secondary': (0.51, 0.78, 0.52, 1),      # #81C784
    'accent': (1.0, 0.72, 0.30, 1),          # #FFB74D
    'background': (0.95, 0.97, 0.91, 1),     # #F1F8E9
    'surface': (1, 1, 1, 1),                  # white
    'text': (0.11, 0.37, 0.13, 1),           # #1B5E20
    'text_secondary': (0.4, 0.4, 0.4, 1),
    'border': (0.78, 0.90, 0.79, 1),         # #C8E6C9
}


class RoundedButton(Button):
    """圆角按钮"""
    
    def __init__(self, bg_color=COLORS['primary'], **kwargs):
        # 设置中文字体
        if 'font_name' not in kwargs:
            kwargs['font_name'] = get_font_name()
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.bg_color = bg_color
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])


class NavBar(BoxLayout):
    """底部导航栏"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = [dp(10), dp(5)]
        self.spacing = dp(5)
        
        # 背景
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # 导航按钮
        self.buttons = {}
        nav_items = [
            ('garden', '🏡', '花园'),
            ('habits', '📋', '习惯'),
            ('stats', '📊', '统计'),
            ('settings', '⚙', '设置'),
        ]
        
        for name, icon, text in nav_items:
            btn = NavButton(icon=icon, text=text, name=name)
            btn.bind(on_press=self.on_nav_press)
            self.buttons[name] = btn
            self.add_widget(btn)
        
        # 默认选中花园
        self.select('garden')
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def on_nav_press(self, btn):
        self.select(btn.name)
        from kivy.app import App
        app = App.get_running_app()
        if app:
            app.switch_screen(btn.name)
    
    def select(self, name):
        for btn_name, btn in self.buttons.items():
            btn.selected = (btn_name == name)


class NavButton(BoxLayout):
    """导航按钮"""
    
    icon = StringProperty('')
    text = StringProperty('')
    name = StringProperty('')
    _selected = False
    
    def __init__(self, icon='', text='', name='', **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_press')
        self.icon = icon
        self.text = text
        self.name = name
        self.orientation = 'vertical'
        self.padding = [0, dp(5)]
        
        # 图标（使用 CLabel 支持中文）
        self.icon_label = CLabel(
            text=icon,
            font_size=dp(18),
            size_hint_y=0.6,
            color=COLORS['text_secondary']
        )
        self.add_widget(self.icon_label)
        
        # 文字（使用 CLabel 支持中文）
        self.text_label = CLabel(
            text=text,
            font_size=dp(10),
            size_hint_y=0.4,
            color=COLORS['text_secondary']
        )
        self.add_widget(self.text_label)
    
    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, value):
        self._selected = value
        color = COLORS['primary_light'] if value else COLORS['text_secondary']
        self.icon_label.color = color
        self.text_label.color = color
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_press')
            return True
        return super().on_touch_down(touch)
    
    def on_press(self):
        pass


class BaseScreen(Screen):
    """基础屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical')
        
        # 内容区域
        self.content = BoxLayout(orientation='vertical', padding=[dp(12), dp(10)])
        self.main_layout.add_widget(self.content)
        
        # 底部导航
        self.navbar = NavBar()
        self.main_layout.add_widget(self.navbar)
        
        self.add_widget(self.main_layout)
        
        # 设置背景
        with self.canvas.before:
            Color(*COLORS['background'])
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def refresh(self):
        """子类重写此方法刷新数据"""
        pass
    
    def on_enter(self):
        """进入屏幕时"""
        self.navbar.select(self.name)


class Card(BoxLayout):
    """卡片组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(15), dp(12)]
        self.spacing = dp(8)
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self._update_bg, size=self._update_bg)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class StatCard(Card):
    """统计卡片"""
    
    def __init__(self, icon='', value='0', label='', color=COLORS['primary_light'], **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = dp(90)
        
        # 图标（使用 CLabel 支持中文和 emoji）
        icon_lbl = CLabel(text=e(icon), font_size=dp(20), size_hint_y=0.4, color=color)
        self.add_widget(icon_lbl)
        
        # 数值
        self.value_lbl = CLabel(text=str(value), font_size=dp(22), bold=True, 
                               size_hint_y=0.35, color=color)
        self.add_widget(self.value_lbl)
        
        # 标签
        label_lbl = CLabel(text=label, font_size=dp(10), size_hint_y=0.25, 
                          color=COLORS['text_secondary'])
        self.add_widget(label_lbl)
    
    def set_value(self, value):
        self.value_lbl.text = str(value)
