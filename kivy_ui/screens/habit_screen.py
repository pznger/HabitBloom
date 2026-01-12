"""习惯管理屏幕"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.app import App

from ..base import BaseScreen, Card, COLORS, RoundedButton
from ..fonts import CLabel, CButton, CTextInput, get_font_name


class HabitCard(BoxLayout):
    """习惯卡片（紧凑型）"""
    
    def __init__(self, habit_data, **kwargs):
        super().__init__(**kwargs)
        self.habit_data = habit_data
        self.habit_id = habit_data.get('habit_id', 0)
        self.register_event_type('on_check_in')
        
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = [dp(12), dp(8)]
        self.spacing = dp(10)
        
        # 背景
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # 图标（使用文字替代 emoji）
        icon_text = habit_data.get('icon', '●')
        # 如果是 emoji 就替换为圆点
        if icon_text and ord(icon_text[0]) > 127:
            icon_text = '●'
        icon = CLabel(text=icon_text, font_size=dp(22), size_hint_x=None, width=dp(40))
        self.add_widget(icon)
        
        # 信息
        info = BoxLayout(orientation='vertical', spacing=dp(2))
        
        name = CLabel(text=habit_data.get('name', ''), font_size=dp(13), bold=True,
                    halign='left', color=COLORS['text'])
        name.bind(size=name.setter('text_size'))
        info.add_widget(name)
        
        streak = habit_data.get('current_streak', 0)
        status = CLabel(text=f'★ 连续{streak}天', font_size=dp(10),
                      halign='left', color=COLORS['text_secondary'])
        status.bind(size=status.setter('text_size'))
        info.add_widget(status)
        
        self.add_widget(info)
        
        # 打卡按钮
        is_completed = habit_data.get('completed_today', False)
        btn = CButton(
            text='√' if is_completed else '打卡',
            size_hint_x=None,
            width=dp(55),
            font_size=dp(11),
            background_color=COLORS['secondary'] if is_completed else COLORS['primary_light'],
            background_normal='',
            disabled=is_completed
        )
        if not is_completed:
            btn.bind(on_press=self._on_check)
        
        self.add_widget(btn)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def _on_check(self, *args):
        self.dispatch('on_check_in', self.habit_id)
    
    def on_check_in(self, habit_id):
        pass


class HabitScreen(BaseScreen):
    """习惯管理屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
    
    def _build_ui(self):
        # 标题栏
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50),
                          padding=[dp(5), 0])
        
        title = CLabel(text='我的习惯', font_size=dp(18), bold=True,
                     halign='left', color=COLORS['text'])
        title.bind(size=title.setter('text_size'))
        header.add_widget(title)
        
        add_btn = CButton(
            text='+',
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            font_size=dp(18),
            background_color=COLORS['primary_light'],
            background_normal=''
        )
        add_btn.bind(on_press=self._show_add_popup)
        header.add_widget(add_btn)
        
        self.content.add_widget(header)
        
        # 习惯列表（滚动）
        scroll = ScrollView(size_hint=(1, 1))
        
        self.habit_list = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            padding=[0, dp(10)]
        )
        self.habit_list.bind(minimum_height=self.habit_list.setter('height'))
        
        scroll.add_widget(self.habit_list)
        self.content.add_widget(scroll)
    
    def refresh(self):
        """刷新习惯列表"""
        app = App.get_running_app()
        if not app:
            return
        
        today_data = app.habit_manager.get_today_status()
        
        self.habit_list.clear_widgets()
        
        if not today_data:
            empty = CLabel(
                text='还没有习惯\n点击右上角添加',
                font_size=dp(14),
                halign='center',
                color=COLORS['text_secondary']
            )
            self.habit_list.add_widget(empty)
            return
        
        # 分组：待完成和已完成
        pending = [h for h in today_data if not h.get('completed_today')]
        completed = [h for h in today_data if h.get('completed_today')]
        
        if pending:
            pending_lbl = CLabel(
                text=f'待完成 ({len(pending)})',
                font_size=dp(13),
                bold=True,
                size_hint_y=None,
                height=dp(30),
                halign='left',
                color=COLORS['accent']
            )
            pending_lbl.bind(size=pending_lbl.setter('text_size'))
            self.habit_list.add_widget(pending_lbl)
            
            for habit in pending:
                card = HabitCard(habit)
                card.bind(on_check_in=self._on_check_in)
                self.habit_list.add_widget(card)
        
        if completed:
            completed_lbl = CLabel(
                text=f'已完成 ({len(completed)})',
                font_size=dp(13),
                bold=True,
                size_hint_y=None,
                height=dp(30),
                halign='left',
                color=COLORS['primary_light']
            )
            completed_lbl.bind(size=completed_lbl.setter('text_size'))
            self.habit_list.add_widget(completed_lbl)
            
            for habit in completed:
                card = HabitCard(habit)
                self.habit_list.add_widget(card)
    
    def _on_check_in(self, widget, habit_id):
        """打卡"""
        app = App.get_running_app()
        result = app.habit_manager.check_in(habit_id)
        
        if result['success']:
            Clock.schedule_once(lambda dt: self.refresh(), 0.3)
            Clock.schedule_once(lambda dt: app.garden_screen.refresh(), 0.3)
    
    def _show_add_popup(self, *args):
        """显示添加习惯弹窗"""
        content = BoxLayout(orientation='vertical', padding=[dp(15)], spacing=dp(12))
        
        # 名称
        name_input = CTextInput(
            hint_text='习惯名称（如：每日阅读）',
            multiline=False,
            size_hint_y=None,
            height=dp(45)
        )
        content.add_widget(name_input)
        
        # 图标选择（用文字替代 emoji）
        icon_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
        icon_lbl = CLabel(text='图标:', size_hint_x=0.3, color=COLORS['text'])
        icon_box.add_widget(icon_lbl)
        
        icon_spinner = Spinner(
            text='●',
            values=['●', '◆', '■', '▲', '★', '♠', '♣', '♥'],
            size_hint_x=0.7,
            font_name=get_font_name()
        )
        icon_box.add_widget(icon_spinner)
        content.add_widget(icon_box)
        
        # 类别
        cat_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
        cat_lbl = CLabel(text='类别:', size_hint_x=0.3, color=COLORS['text'])
        cat_box.add_widget(cat_lbl)
        
        cat_spinner = Spinner(
            text='健康',
            values=['健康', '学习', '工作', '生活'],
            size_hint_x=0.7,
            font_name=get_font_name()
        )
        cat_box.add_widget(cat_spinner)
        content.add_widget(cat_box)
        
        # 植物类型
        plant_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
        plant_lbl = CLabel(text='植物:', size_hint_x=0.3, color=COLORS['text'])
        plant_box.add_widget(plant_lbl)
        
        plant_spinner = Spinner(
            text='花朵',
            values=['花朵', '树木', '仙人掌', '草药'],
            size_hint_x=0.7,
            font_name=get_font_name()
        )
        plant_box.add_widget(plant_spinner)
        content.add_widget(plant_box)
        
        # 按钮
        btn_box = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(10))
        
        popup = Popup(title='添加新习惯', content=content, size_hint=(0.9, 0.55),
                     title_font=get_font_name())
        
        cancel_btn = CButton(text='取消', background_color=COLORS['border'])
        cancel_btn.bind(on_press=popup.dismiss)
        btn_box.add_widget(cancel_btn)
        
        def save(*args):
            name = name_input.text.strip()
            if not name:
                return
            
            icon = icon_spinner.text
            
            cat_map = {'健康': 'health', '学习': 'study', '工作': 'work', '生活': 'life'}
            category = cat_map.get(cat_spinner.text, 'life')
            
            plant_map = {'花朵': 'flower', '树木': 'tree', '仙人掌': 'cactus', '草药': 'herb'}
            plant_type = plant_map.get(plant_spinner.text, 'flower')
            
            app = App.get_running_app()
            app.habit_manager.create_habit(
                name=name, icon=icon, category=category, plant_type=plant_type
            )
            
            popup.dismiss()
            Clock.schedule_once(lambda dt: self.refresh(), 0.2)
            Clock.schedule_once(lambda dt: app.garden_screen.refresh(), 0.2)
        
        save_btn = CButton(text='保存', background_color=COLORS['primary_light'])
        save_btn.bind(on_press=save)
        btn_box.add_widget(save_btn)
        
        content.add_widget(btn_box)
        popup.open()
