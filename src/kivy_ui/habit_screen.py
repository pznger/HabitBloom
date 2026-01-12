"""习惯管理页面 - Kivy 版本"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp

from ..managers.habit_manager import HabitManager
from ..utils.constants import CATEGORIES, PLANT_TYPES


class HabitCard(BoxLayout):
    """习惯卡片"""
    
    def __init__(self, habit_data, on_check_in=None, on_delete=None, **kwargs):
        super().__init__(**kwargs)
        self.habit_data = habit_data
        self.on_check_in_callback = on_check_in
        self.on_delete_callback = on_delete
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(70)
        self.padding = [dp(12), dp(8), dp(12), dp(8)]
        self.spacing = dp(10)
        
        # 背景
        with self.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # 图标
        icon = Label(
            text=habit_data.get('icon', '🌱'),
            font_size='24sp',
            size_hint_x=0.15,
        )
        self.add_widget(icon)
        
        # 信息
        info = BoxLayout(orientation='vertical', size_hint_x=0.55, spacing=dp(2))
        
        name = Label(
            text=habit_data.get('name', '习惯'),
            font_size='13sp',
            bold=True,
            color=get_color_from_hex('#333333'),
            halign='left',
            size_hint_y=0.5,
        )
        name.bind(size=name.setter('text_size'))
        info.add_widget(name)
        
        streak = habit_data.get('current_streak', 0)
        status = Label(
            text=f'🔥 连续{streak}天',
            font_size='10sp',
            color=get_color_from_hex('#666666'),
            halign='left',
            size_hint_y=0.5,
        )
        status.bind(size=status.setter('text_size'))
        info.add_widget(status)
        
        self.add_widget(info)
        
        # 打卡按钮
        is_completed = habit_data.get('completed_today', False)
        if is_completed:
            btn = Button(
                text='✓',
                font_size='14sp',
                size_hint_x=0.2,
                background_normal='',
                background_color=get_color_from_hex('#81C784'),
                disabled=True,
            )
        else:
            btn = Button(
                text='打卡',
                font_size='11sp',
                size_hint_x=0.2,
                background_normal='',
                background_color=get_color_from_hex('#4CAF50'),
            )
            btn.bind(on_release=self.on_check_in)
        
        self.add_widget(btn)
    
    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def on_check_in(self, btn):
        if self.on_check_in_callback:
            self.on_check_in_callback(self.habit_data.get('habit_id'))


class AddHabitPopup(Popup):
    """添加习惯弹窗"""
    
    def __init__(self, on_save=None, **kwargs):
        super().__init__(**kwargs)
        self.on_save_callback = on_save
        self.title = '🌱 添加新习惯'
        self.size_hint = (0.9, 0.7)
        
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(12))
        
        # 名称输入
        self.name_input = TextInput(
            hint_text='习惯名称（如：每日阅读）',
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size='14sp',
        )
        layout.add_widget(self.name_input)
        
        # 图标选择
        icon_layout = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(10))
        icon_layout.add_widget(Label(text='图标', size_hint_x=0.3, halign='left'))
        self.icon_spinner = Spinner(
            text='🌱',
            values=['🌱', '📚', '🏃', '💧', '🧘', '✍️', '💪', '🎯', '⏰', '🎵'],
            size_hint_x=0.7,
            font_size='18sp',
        )
        icon_layout.add_widget(self.icon_spinner)
        layout.add_widget(icon_layout)
        
        # 类别选择
        cat_layout = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(10))
        cat_layout.add_widget(Label(text='类别', size_hint_x=0.3, halign='left'))
        cat_values = [f"{v['icon']} {v['name']}" for v in CATEGORIES.values()]
        self.cat_spinner = Spinner(
            text=cat_values[3],  # 生活
            values=cat_values,
            size_hint_x=0.7,
        )
        icon_layout.children[0].bind(size=icon_layout.children[0].setter('text_size'))
        cat_layout.add_widget(self.cat_spinner)
        layout.add_widget(cat_layout)
        
        # 植物类型
        plant_layout = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(10))
        plant_layout.add_widget(Label(text='植物', size_hint_x=0.3, halign='left'))
        plant_values = [f"{v['icon']} {v['name']}" for v in PLANT_TYPES.values()]
        self.plant_spinner = Spinner(
            text=plant_values[0],
            values=plant_values,
            size_hint_x=0.7,
        )
        plant_layout.add_widget(self.plant_spinner)
        layout.add_widget(plant_layout)
        
        layout.add_widget(BoxLayout())  # 占位
        
        # 按钮
        btn_layout = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(10))
        
        cancel_btn = Button(
            text='取消',
            background_normal='',
            background_color=get_color_from_hex('#E0E0E0'),
            color=get_color_from_hex('#333333'),
        )
        cancel_btn.bind(on_release=lambda x: self.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        save_btn = Button(
            text='保存',
            background_normal='',
            background_color=get_color_from_hex('#4CAF50'),
        )
        save_btn.bind(on_release=self.on_save)
        btn_layout.add_widget(save_btn)
        
        layout.add_widget(btn_layout)
        
        self.content = layout
    
    def on_save(self, btn):
        name = self.name_input.text.strip()
        if not name:
            return
        
        # 解析选择的值
        cat_text = self.cat_spinner.text
        cat_keys = list(CATEGORIES.keys())
        cat_idx = next((i for i, v in enumerate(CATEGORIES.values()) if f"{v['icon']} {v['name']}" == cat_text), 3)
        category = cat_keys[cat_idx]
        
        plant_text = self.plant_spinner.text
        plant_keys = list(PLANT_TYPES.keys())
        plant_idx = next((i for i, v in enumerate(PLANT_TYPES.values()) if f"{v['icon']} {v['name']}" == plant_text), 0)
        plant_type = plant_keys[plant_idx]
        
        data = {
            'name': name,
            'icon': self.icon_spinner.text,
            'category': category,
            'plant_type': plant_type,
            'target_frequency': 7,
            'difficulty': 1,
        }
        
        if self.on_save_callback:
            self.on_save_callback(data)
        
        self.dismiss()


class HabitScreen(Screen):
    """习惯管理页面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.habit_manager = HabitManager()
        self._build_ui()
    
    def _build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=[dp(12), dp(10), dp(12), dp(10)], spacing=dp(10))
        
        # 标题栏
        header = BoxLayout(size_hint_y=None, height=dp(45))
        
        title = Label(
            text='📋 我的习惯',
            font_size='18sp',
            bold=True,
            color=get_color_from_hex('#333333'),
            halign='left',
            size_hint_x=0.7,
        )
        title.bind(size=title.setter('text_size'))
        header.add_widget(title)
        
        add_btn = Button(
            text='➕',
            font_size='18sp',
            size_hint_x=0.15,
            background_normal='',
            background_color=get_color_from_hex('#4CAF50'),
        )
        add_btn.bind(on_release=self.show_add_popup)
        header.add_widget(add_btn)
        
        layout.add_widget(header)
        
        # 列表
        scroll = ScrollView(size_hint=(1, 1))
        self.habit_list = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
        )
        self.habit_list.bind(minimum_height=self.habit_list.setter('height'))
        scroll.add_widget(self.habit_list)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        
        Clock.schedule_once(lambda dt: self.refresh(), 0.1)
    
    def refresh(self, *args):
        """刷新列表"""
        self.habit_list.clear_widgets()
        
        today_data = self.habit_manager.get_today_status()
        
        if not today_data:
            empty = Label(
                text='🌱 还没有习惯\n点击右上角添加',
                font_size='14sp',
                color=get_color_from_hex('#888888'),
                halign='center',
                size_hint_y=None,
                height=dp(100),
            )
            empty.bind(size=empty.setter('text_size'))
            self.habit_list.add_widget(empty)
            return
        
        # 待完成
        pending = [h for h in today_data if not h.get('completed_today')]
        completed = [h for h in today_data if h.get('completed_today')]
        
        if pending:
            label = Label(
                text=f'⏳ 待完成 ({len(pending)})',
                font_size='12sp',
                bold=True,
                color=get_color_from_hex('#FF9800'),
                halign='left',
                size_hint_y=None,
                height=dp(30),
            )
            label.bind(size=label.setter('text_size'))
            self.habit_list.add_widget(label)
            
            for habit in pending:
                card = HabitCard(habit, on_check_in=self.on_check_in)
                self.habit_list.add_widget(card)
        
        if completed:
            label = Label(
                text=f'✅ 已完成 ({len(completed)})',
                font_size='12sp',
                bold=True,
                color=get_color_from_hex('#4CAF50'),
                halign='left',
                size_hint_y=None,
                height=dp(30),
            )
            label.bind(size=label.setter('text_size'))
            self.habit_list.add_widget(label)
            
            for habit in completed:
                card = HabitCard(habit)
                self.habit_list.add_widget(card)
    
    def show_add_popup(self, btn):
        """显示添加弹窗"""
        popup = AddHabitPopup(on_save=self.on_add_habit)
        popup.open()
    
    def on_add_habit(self, data):
        """添加习惯"""
        habit_id = self.habit_manager.create_habit(**data)
        if habit_id:
            self.refresh()
            
            popup = Popup(
                title='成功',
                content=Label(text='习惯创建成功！🌱'),
                size_hint=(0.8, 0.3),
            )
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
    
    def on_check_in(self, habit_id):
        """打卡"""
        result = self.habit_manager.check_in(habit_id)
        if result['success']:
            self.refresh()
            
            popup = Popup(
                title='🎉 打卡成功！',
                content=Label(text='继续保持！'),
                size_hint=(0.8, 0.3),
            )
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
    
    def on_enter(self):
        """进入页面"""
        self.refresh()
