"""花园页面 - Kivy 版本"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp

from ..managers.garden_manager import GardenManager
from ..managers.habit_manager import HabitManager
from ..utils.helpers import get_greeting


class PlantCard(BoxLayout):
    """植物卡片"""
    
    def __init__(self, plant_data, on_check_in=None, **kwargs):
        super().__init__(**kwargs)
        self.plant_data = plant_data
        self.on_check_in_callback = on_check_in
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(160), dp(180))
        self.padding = [dp(10), dp(10), dp(10), dp(10)]
        self.spacing = dp(5)
        
        # 背景
        with self.canvas.before:
            health = plant_data.get('health', 100)
            if health >= 80:
                Color(*get_color_from_hex('#FFFFFF'))
            elif health >= 50:
                Color(*get_color_from_hex('#FFF8E1'))
            else:
                Color(*get_color_from_hex('#FFEBEE'))
            self.bg_rect = RoundedRectangle(
                pos=self.pos, 
                size=self.size,
                radius=[dp(16)]
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # 植物图标
        icon = Label(
            text=plant_data.get('plant_icon', '🌱'),
            font_size='40sp',
            size_hint_y=0.4,
        )
        self.add_widget(icon)
        
        # 名称
        name = Label(
            text=plant_data.get('name', '习惯'),
            font_size='13sp',
            bold=True,
            color=get_color_from_hex('#333333'),
            size_hint_y=0.15,
            halign='center',
        )
        name.bind(size=name.setter('text_size'))
        self.add_widget(name)
        
        # 状态
        streak = plant_data.get('current_streak', 0)
        stage_name = plant_data.get('stage_name', '种子')
        status_text = f"🔥 {streak}天 · {stage_name}" if streak > 0 else f"🌱 {stage_name}"
        
        status = Label(
            text=status_text,
            font_size='10sp',
            color=get_color_from_hex('#666666'),
            size_hint_y=0.1,
        )
        self.add_widget(status)
        
        # 健康条
        health_bar = ProgressBar(
            max=100,
            value=plant_data.get('health', 100),
            size_hint_y=0.08,
        )
        self.add_widget(health_bar)
        
        # 打卡按钮
        if plant_data.get('is_completed_today'):
            btn = Button(
                text='✅ 已完成',
                font_size='11sp',
                size_hint_y=0.2,
                background_normal='',
                background_color=get_color_from_hex('#81C784'),
                disabled=True,
            )
        else:
            btn = Button(
                text='浇灌 💧',
                font_size='11sp',
                size_hint_y=0.2,
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
            self.on_check_in_callback(self.plant_data.get('habit_id'))


class AddPlantCard(BoxLayout):
    """添加植物卡片"""
    
    def __init__(self, on_add=None, **kwargs):
        super().__init__(**kwargs)
        self.on_add_callback = on_add
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(160), dp(180))
        self.padding = [dp(10), dp(10), dp(10), dp(10)]
        
        # 背景
        with self.canvas.before:
            Color(*get_color_from_hex('#F5F5F5'))
            self.bg_rect = RoundedRectangle(
                pos=self.pos, 
                size=self.size,
                radius=[dp(16)]
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # 图标
        icon = Label(
            text='➕',
            font_size='36sp',
            size_hint_y=0.6,
        )
        self.add_widget(icon)
        
        # 文字
        text = Label(
            text='添加习惯',
            font_size='12sp',
            color=get_color_from_hex('#666666'),
            size_hint_y=0.4,
        )
        self.add_widget(text)
        
        # 点击事件
        btn = Button(
            background_color=(0, 0, 0, 0),
            on_release=self.on_add,
        )
        self.add_widget(btn)
    
    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def on_add(self, btn):
        if self.on_add_callback:
            self.on_add_callback()


class GardenScreen(Screen):
    """花园页面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.garden_manager = GardenManager()
        self.habit_manager = HabitManager()
        self._build_ui()
    
    def _build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=[dp(12), dp(10), dp(12), dp(10)], spacing=dp(10))
        
        # 问候语
        greeting = get_greeting()
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(60))
        
        greeting_label = Label(
            text=f'{greeting}！',
            font_size='20sp',
            bold=True,
            color=get_color_from_hex('#333333'),
            halign='left',
            size_hint_y=0.6,
        )
        greeting_label.bind(size=greeting_label.setter('text_size'))
        header.add_widget(greeting_label)
        
        subtitle = Label(
            text='看看你的习惯花园 🌱',
            font_size='13sp',
            color=get_color_from_hex('#666666'),
            halign='left',
            size_hint_y=0.4,
        )
        subtitle.bind(size=subtitle.setter('text_size'))
        header.add_widget(subtitle)
        
        layout.add_widget(header)
        
        # 统计栏
        self.stats_bar = self._create_stats_bar()
        layout.add_widget(self.stats_bar)
        
        # 花园网格（滚动）
        scroll = ScrollView(size_hint=(1, 1))
        self.garden_grid = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            padding=[0, dp(5), 0, dp(5)],
        )
        self.garden_grid.bind(minimum_height=self.garden_grid.setter('height'))
        scroll.add_widget(self.garden_grid)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        
        # 加载数据
        Clock.schedule_once(lambda dt: self.refresh(), 0.1)
    
    def _create_stats_bar(self):
        """创建统计栏"""
        bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(70),
            padding=[dp(15), dp(10), dp(15), dp(10)],
        )
        
        # 背景
        with bar.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            bar.bg_rect = RoundedRectangle(pos=bar.pos, size=bar.size, radius=[dp(12)])
        bar.bind(pos=lambda *a: setattr(bar.bg_rect, 'pos', bar.pos))
        bar.bind(size=lambda *a: setattr(bar.bg_rect, 'size', bar.size))
        
        self.stats_labels = {}
        stats_items = [
            ('total', '🌿', '植物'),
            ('healthy', '💚', '健康'),
            ('health_rate', '📊', '健康度'),
        ]
        
        for key, icon, label in stats_items:
            item = BoxLayout(orientation='vertical', spacing=dp(2))
            
            value_row = BoxLayout(orientation='horizontal', size_hint_y=0.6)
            icon_lbl = Label(text=icon, font_size='16sp', size_hint_x=0.3)
            value_lbl = Label(
                text='0',
                font_size='18sp',
                bold=True,
                color=get_color_from_hex('#2E7D32'),
                size_hint_x=0.7,
                halign='left',
            )
            value_lbl.bind(size=value_lbl.setter('text_size'))
            self.stats_labels[key] = value_lbl
            value_row.add_widget(icon_lbl)
            value_row.add_widget(value_lbl)
            item.add_widget(value_row)
            
            label_lbl = Label(
                text=label,
                font_size='10sp',
                color=get_color_from_hex('#888888'),
                size_hint_y=0.4,
                halign='center',
            )
            label_lbl.bind(size=label_lbl.setter('text_size'))
            item.add_widget(label_lbl)
            
            bar.add_widget(item)
        
        return bar
    
    def refresh(self, *args):
        """刷新数据"""
        overview = self.garden_manager.get_garden_overview()
        plants = overview['plants']
        
        today_status = self.habit_manager.get_today_status()
        status_map = {r['habit_id']: r.get('completed_today', False) for r in today_status}
        
        # 更新统计
        self.stats_labels['total'].text = str(overview['total_plants'])
        self.stats_labels['healthy'].text = str(overview['healthy_plants'])
        self.stats_labels['health_rate'].text = f"{overview['garden_health']}%"
        
        # 清空网格
        self.garden_grid.clear_widgets()
        
        if not plants:
            empty = Label(
                text='🌱 花园还是空的\n添加第一个习惯吧！',
                font_size='14sp',
                color=get_color_from_hex('#888888'),
                halign='center',
                size_hint_y=None,
                height=dp(100),
            )
            empty.bind(size=empty.setter('text_size'))
            self.garden_grid.add_widget(empty)
        else:
            for plant in plants:
                plant['is_completed_today'] = status_map.get(plant['habit_id'], False)
                card = PlantCard(plant, on_check_in=self.on_check_in)
                self.garden_grid.add_widget(card)
        
        # 添加按钮
        add_card = AddPlantCard(on_add=self.on_add_habit)
        self.garden_grid.add_widget(add_card)
    
    def on_check_in(self, habit_id):
        """打卡"""
        result = self.habit_manager.check_in(habit_id)
        
        if result['success']:
            # 显示成功提示
            popup = Popup(
                title='🎉 打卡成功！',
                content=Label(text='继续保持！'),
                size_hint=(0.8, 0.3),
            )
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
            
            # 刷新
            Clock.schedule_once(lambda dt: self.refresh(), 0.5)
            
            # 检查成就
            if result.get('unlocked_achievements'):
                for ach in result['unlocked_achievements']:
                    ach_popup = Popup(
                        title='🏆 成就解锁！',
                        content=Label(text=f"{ach['icon']} {ach['title']}"),
                        size_hint=(0.8, 0.3),
                    )
                    Clock.schedule_once(lambda dt, p=ach_popup: p.open(), 1.5)
    
    def on_add_habit(self):
        """添加习惯 - 切换到习惯页面"""
        self.manager.current = 'habit'
    
    def on_enter(self):
        """进入页面时刷新"""
        self.refresh()
