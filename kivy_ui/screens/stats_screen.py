"""统计屏幕"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line
from kivy.metrics import dp
from kivy.app import App
from datetime import date

from ..base import BaseScreen, Card, StatCard, COLORS
from ..fonts import CLabel


class ProgressRing(Widget):
    """进度环"""
    
    def __init__(self, value=0, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.size_hint = (None, None)
        self.size = (dp(80), dp(80))
        self.bind(pos=self._draw, size=self._draw)
        self._draw()
    
    def _draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            # 背景环
            Color(0.91, 0.91, 0.91, 1)
            Line(circle=(self.center_x, self.center_y, dp(32)), width=dp(6), cap='round')
            
            # 进度环
            if self.value > 0:
                Color(*COLORS['primary_light'])
                angle = 360 * (self.value / 100)
                Line(circle=(self.center_x, self.center_y, dp(32), 90, 90 - angle), 
                     width=dp(6), cap='round')
    
    def set_value(self, value):
        self.value = value
        self._draw()


class WeeklyBar(BoxLayout):
    """周统计柱状图"""
    
    def __init__(self, day_data, max_val, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_x = 1/7
        self.spacing = dp(3)
        
        # 数值
        count = CLabel(text=str(day_data['completed']), font_size=dp(9),
                     size_hint_y=0.15, color=COLORS['text_secondary'])
        self.add_widget(count)
        
        # 柱子容器
        bar_container = BoxLayout(size_hint_y=0.65)
        bar_height = max(0.1, day_data['completed'] / max_val) if max_val > 0 else 0.1
        
        bar = Widget(size_hint=(0.6, bar_height))
        is_today = day_data.get('date') == date.today()
        
        with bar.canvas:
            Color(*COLORS['primary_light'] if is_today else COLORS['secondary'])
            bar.rect = RoundedRectangle(pos=bar.pos, size=bar.size, radius=[dp(4)])
        bar.bind(pos=lambda w, p: setattr(bar.rect, 'pos', p),
                size=lambda w, s: setattr(bar.rect, 'size', s))
        
        bar_container.add_widget(Widget())  # 底部空间
        bar_container.add_widget(bar)
        self.add_widget(bar_container)
        
        # 星期
        day_name = day_data.get('day_name', '')[:1]
        day_lbl = CLabel(text=day_name, font_size=dp(10), size_hint_y=0.2,
                       color=COLORS['primary_light'] if is_today else COLORS['text_secondary'])
        self.add_widget(day_lbl)


class StatsScreen(BaseScreen):
    """统计屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
    
    def _build_ui(self):
        # 标题
        header = BoxLayout(size_hint_y=None, height=dp(40))
        
        title = CLabel(text='统计', font_size=dp(18), bold=True,
                     halign='left', color=COLORS['text'])
        title.bind(size=title.setter('text_size'))
        header.add_widget(title)
        
        today = date.today()
        month_lbl = CLabel(text=f'{today.month}月', font_size=dp(13),
                         halign='right', color=COLORS['text_secondary'])
        month_lbl.bind(size=month_lbl.setter('text_size'))
        header.add_widget(month_lbl)
        
        self.content.add_widget(header)
        
        # 滚动内容
        scroll = ScrollView(size_hint=(1, 1))
        
        self.stats_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            size_hint_y=None,
            padding=[0, dp(5)]
        )
        self.stats_layout.bind(minimum_height=self.stats_layout.setter('height'))
        
        scroll.add_widget(self.stats_layout)
        self.content.add_widget(scroll)
    
    def refresh(self):
        """刷新统计"""
        app = App.get_running_app()
        if not app:
            return
        
        overview = app.stats_manager.get_overview_stats()
        weekly = app.stats_manager.get_weekly_stats()
        monthly = app.stats_manager.get_monthly_stats()
        achievements = app.stats_manager.get_achievements()
        
        self.stats_layout.clear_widgets()
        
        # 概览卡片（用文字符号替代 emoji）
        stats_grid = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(200))
        
        stats_grid.add_widget(StatCard(icon='#', value=str(overview['total_habits']), 
                                       label='习惯', color=(0.13, 0.59, 0.95, 1)))
        stats_grid.add_widget(StatCard(icon='√', value=str(overview['completed_today']),
                                       label='今日', color=COLORS['primary_light']))
        stats_grid.add_widget(StatCard(icon='★', value=str(overview['current_max_streak']),
                                       label='连续', color=COLORS['accent']))
        stats_grid.add_widget(StatCard(icon='♛', value=str(overview['longest_ever_streak']),
                                       label='最长', color=(0.61, 0.15, 0.69, 1)))
        
        self.stats_layout.add_widget(stats_grid)
        
        # 月度完成率卡片
        rate_card = Card()
        rate_card.size_hint_y = None
        rate_card.height = dp(100)
        rate_card.orientation = 'horizontal'
        
        # 进度环
        ring_box = BoxLayout(size_hint_x=0.35)
        ring = ProgressRing(value=int(monthly['completion_rate']))
        ring_box.add_widget(ring)
        rate_card.add_widget(ring_box)
        
        # 详情
        details = BoxLayout(orientation='vertical', size_hint_x=0.65, spacing=dp(5))
        
        rate_title = CLabel(text='本月完成率', font_size=dp(14), bold=True,
                          halign='left', color=COLORS['text'])
        rate_title.bind(size=rate_title.setter('text_size'))
        details.add_widget(rate_title)
        
        rate_value = CLabel(text=f"{int(monthly['completion_rate'])}%", 
                          font_size=dp(24), bold=True,
                          halign='left', color=COLORS['primary_light'])
        rate_value.bind(size=rate_value.setter('text_size'))
        details.add_widget(rate_value)
        
        completed_text = CLabel(text=f"完成 {monthly['total_completed']}/{monthly['expected_completions']}",
                              font_size=dp(11), halign='left', color=COLORS['text_secondary'])
        completed_text.bind(size=completed_text.setter('text_size'))
        details.add_widget(completed_text)
        
        rate_card.add_widget(details)
        self.stats_layout.add_widget(rate_card)
        
        # 周统计图
        if weekly.get('daily_data'):
            weekly_card = Card()
            weekly_card.size_hint_y = None
            weekly_card.height = dp(140)
            
            weekly_title = CLabel(text='本周', font_size=dp(13), bold=True,
                                size_hint_y=0.2, halign='left', color=COLORS['text'])
            weekly_title.bind(size=weekly_title.setter('text_size'))
            weekly_card.add_widget(weekly_title)
            
            chart_box = BoxLayout(orientation='horizontal', size_hint_y=0.8, spacing=dp(5))
            
            max_val = max((d['completed'] for d in weekly['daily_data']), default=1)
            for day_data in weekly['daily_data']:
                bar = WeeklyBar(day_data, max_val)
                chart_box.add_widget(bar)
            
            weekly_card.add_widget(chart_box)
            self.stats_layout.add_widget(weekly_card)
        
        # 成就
        ach_label = CLabel(
            text=f"成就 ({achievements['unlocked_count']}/{achievements['total']})",
            font_size=dp(13), bold=True, size_hint_y=None, height=dp(30),
            halign='left', color=COLORS['text']
        )
        ach_label.bind(size=ach_label.setter('text_size'))
        self.stats_layout.add_widget(ach_label)
        
        ach_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80), spacing=dp(8))
        
        all_achs = achievements['unlocked'] + achievements['locked']
        for ach in all_achs[:4]:
            ach_card = self._create_ach_card(ach)
            ach_box.add_widget(ach_card)
        
        self.stats_layout.add_widget(ach_box)
    
    def _create_ach_card(self, ach):
        """创建成就卡片"""
        card = BoxLayout(orientation='vertical', size_hint_x=0.25)
        is_unlocked = ach.is_unlocked
        
        with card.canvas.before:
            Color(1, 0.97, 0.88, 1) if is_unlocked else Color(0.96, 0.96, 0.96, 1)
            card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(10)])
        card.bind(pos=lambda w, p: setattr(card.rect, 'pos', p),
                 size=lambda w, s: setattr(card.rect, 'size', s))
        
        # 使用文字符号替代 emoji
        icon_text = ach.badge_icon if is_unlocked else '?'
        if icon_text and len(icon_text) > 0 and ord(icon_text[0]) > 127:
            icon_text = '★'  # 用星号替代 emoji
        icon = CLabel(text=icon_text, font_size=dp(24), size_hint_y=0.6)
        card.add_widget(icon)
        
        title = CLabel(text=ach.title[:4] if len(ach.title) > 4 else ach.title,
                     font_size=dp(9), size_hint_y=0.4,
                     color=COLORS['text'] if is_unlocked else COLORS['text_secondary'])
        card.add_widget(title)
        
        return card
