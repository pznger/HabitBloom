"""花园屏幕"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.app import App

from ..base import BaseScreen, Card, StatCard, COLORS, RoundedButton
from ..fonts import CLabel, CButton, CTextInput
from kivy_ui.widgets.plant_widget import PlantCard


class GardenScreen(BaseScreen):
    """花园主屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
    
    def _build_ui(self):
        """构建UI"""
        # 标题区域
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(60), 
                          padding=[dp(5), 0])
        
        greeting_lbl = CLabel(
            text=self._get_greeting(),
            font_size=dp(20),
            bold=True,
            halign='left',
            valign='middle',
            color=COLORS['text'],
            size_hint_y=0.6
        )
        greeting_lbl.bind(size=greeting_lbl.setter('text_size'))
        header.add_widget(greeting_lbl)
        
        subtitle_lbl = CLabel(
            text='看看你的习惯花园',
            font_size=dp(13),
            halign='left',
            valign='top',
            color=COLORS['text_secondary'],
            size_hint_y=0.4
        )
        subtitle_lbl.bind(size=subtitle_lbl.setter('text_size'))
        header.add_widget(subtitle_lbl)
        
        self.content.add_widget(header)
        
        # 统计栏 - 使用文字符号替代 emoji
        stats_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70),
                             spacing=dp(8))
        
        self.total_stat = StatCard(icon='♣', value='0', label='植物')
        self.healthy_stat = StatCard(icon='♥', value='0', label='健康')
        self.rate_stat = StatCard(icon='%', value='0%', label='健康度')
        
        stats_row.add_widget(self.total_stat)
        stats_row.add_widget(self.healthy_stat)
        stats_row.add_widget(self.rate_stat)
        
        self.content.add_widget(stats_row)
        
        # 花园网格（滚动）
        scroll = ScrollView(size_hint=(1, 1))
        
        self.garden_grid = GridLayout(
            cols=2,
            spacing=dp(10),
            padding=[0, dp(10)],
            size_hint_y=None
        )
        self.garden_grid.bind(minimum_height=self.garden_grid.setter('height'))
        
        scroll.add_widget(self.garden_grid)
        self.content.add_widget(scroll)
    
    def _get_greeting(self):
        from datetime import datetime
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "早上好！"
        elif 12 <= hour < 14:
            return "中午好！"
        elif 14 <= hour < 18:
            return "下午好！"
        elif 18 <= hour < 22:
            return "晚上好！"
        else:
            return "夜深了！"
    
    def refresh(self):
        """刷新花园数据"""
        app = App.get_running_app()
        if not app:
            return
        
        # 获取数据
        overview = app.garden_manager.get_garden_overview()
        plants = overview['plants']
        
        # 获取今日状态
        today_status = app.habit_manager.get_today_status()
        status_map = {r['habit_id']: r.get('completed_today', False) for r in today_status}
        
        # 更新统计
        self.total_stat.set_value(overview['total_plants'])
        self.healthy_stat.set_value(overview['healthy_plants'])
        self.rate_stat.set_value(f"{overview['garden_health']}%")
        
        # 清空网格
        self.garden_grid.clear_widgets()
        
        if not plants:
            # 空状态
            empty_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(150))
            empty_lbl = CLabel(
                text='花园还是空的\n添加第一个习惯吧！',
                font_size=dp(14),
                halign='center',
                color=COLORS['text_secondary']
            )
            empty_box.add_widget(empty_lbl)
            self.garden_grid.add_widget(empty_box)
            
            # 添加按钮
            add_card = self._create_add_card()
            self.garden_grid.add_widget(add_card)
            return
        
        # 添加植物卡片
        for plant in plants:
            plant['is_completed_today'] = status_map.get(plant['habit_id'], False)
            card = PlantCard(plant_data=plant)
            card.bind(on_check_in=self.on_check_in)
            self.garden_grid.add_widget(card)
        
        # 添加新增按钮
        add_card = self._create_add_card()
        self.garden_grid.add_widget(add_card)
    
    def _create_add_card(self):
        """创建添加按钮卡片"""
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(160),
                        padding=[dp(10), dp(10)])
        
        with card.canvas.before:
            Color(0.96, 0.96, 0.96, 1)
            card.bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(16)])
        card.bind(pos=lambda w, p: setattr(card.bg_rect, 'pos', p),
                 size=lambda w, s: setattr(card.bg_rect, 'size', s))
        
        icon = CLabel(text='+', font_size=dp(36), size_hint_y=0.6)
        card.add_widget(icon)
        
        text = CLabel(text='添加习惯', font_size=dp(12), color=COLORS['text_secondary'],
                    size_hint_y=0.4)
        card.add_widget(text)
        
        card.bind(on_touch_down=self._on_add_touch)
        
        return card
    
    def _on_add_touch(self, widget, touch):
        if widget.collide_point(*touch.pos):
            app = App.get_running_app()
            if app:
                app.switch_screen('habits')
            return True
        return False
    
    def on_check_in(self, widget, habit_id):
        """打卡事件"""
        app = App.get_running_app()
        if not app:
            return
        
        # 显示打卡对话框
        self._show_checkin_popup(habit_id)
    
    def _show_checkin_popup(self, habit_id):
        """显示打卡弹窗"""
        app = App.get_running_app()
        habit = app.habit_manager.get_habit(habit_id)
        if not habit:
            return
        
        content = BoxLayout(orientation='vertical', padding=[dp(20)], spacing=dp(15))
        
        title = CLabel(text=f'太棒了！完成「{habit.name}」', font_size=dp(16), bold=True,
                     size_hint_y=None, height=dp(40), color=COLORS['text'])
        content.add_widget(title)
        
        note_input = CTextInput(
            hint_text='写点什么？（可选）',
            multiline=True,
            size_hint_y=None,
            height=dp(80)
        )
        content.add_widget(note_input)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=dp(10),
                              size_hint_y=None, height=dp(45))
        
        popup = Popup(title='', content=content, size_hint=(0.9, None), height=dp(250),
                     separator_height=0)
        
        skip_btn = CButton(text='跳过', background_color=COLORS['border'])
        skip_btn.bind(on_press=lambda x: self._do_checkin(popup, habit_id, ''))
        btn_layout.add_widget(skip_btn)
        
        save_btn = CButton(text='保存 ★', background_color=COLORS['primary_light'])
        save_btn.bind(on_press=lambda x: self._do_checkin(popup, habit_id, note_input.text))
        btn_layout.add_widget(save_btn)
        
        content.add_widget(btn_layout)
        popup.open()
    
    def _do_checkin(self, popup, habit_id, note):
        """执行打卡"""
        popup.dismiss()
        
        app = App.get_running_app()
        result = app.habit_manager.check_in(habit_id, notes=note)
        
        if result['success']:
            # 显示成功提示
            if result.get('unlocked_achievements'):
                for ach in result['unlocked_achievements']:
                    self._show_achievement_popup(ach)
            
            # 刷新
            Clock.schedule_once(lambda dt: self.refresh(), 0.3)
    
    def _show_achievement_popup(self, ach):
        """显示成就解锁弹窗"""
        content = BoxLayout(orientation='vertical', padding=[dp(20)])
        
        icon = CLabel(text=ach['icon'], font_size=dp(48), size_hint_y=0.5)
        content.add_widget(icon)
        
        title = CLabel(text=f"★ {ach['title']}", font_size=dp(18), bold=True,
                     size_hint_y=0.3, color=COLORS['text'])
        content.add_widget(title)
        
        btn = CButton(text='太棒了！', size_hint_y=0.2, background_color=COLORS['primary_light'])
        
        popup = Popup(title='成就解锁！', content=content, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        
        popup.open()
