"""植物卡片组件"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import DictProperty
from kivy.metrics import dp
from kivy.animation import Animation

from ..base import COLORS
from ..fonts import CLabel, CButton


class PlantCard(BoxLayout):
    """植物卡片"""
    
    plant_data = DictProperty({})
    
    def __init__(self, plant_data=None, **kwargs):
        super().__init__(**kwargs)
        self.plant_data = plant_data or {}
        self.register_event_type('on_check_in')
        
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(160)
        self.padding = [dp(10), dp(10)]
        self.spacing = dp(5)
        
        self._build_ui()
        self._update_style()
    
    def _build_ui(self):
        """构建UI"""
        # 背景
        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # 植物图标（使用文字符号替代 emoji）
        icon_text = self.plant_data.get('plant_icon', '○')
        if icon_text and len(icon_text) > 0 and ord(icon_text[0]) > 127:
            # 根据生长阶段使用不同符号
            stage = self.plant_data.get('growth_stage', 0)
            icons = ['○', '◐', '●', '✿', '❀']
            icon_text = icons[min(stage, len(icons)-1)]
        
        self.icon_lbl = CLabel(
            text=icon_text,
            font_size=dp(36),
            size_hint_y=0.35
        )
        self.add_widget(self.icon_lbl)
        
        # 习惯名称
        self.name_lbl = CLabel(
            text=self.plant_data.get('name', '习惯'),
            font_size=dp(12),
            bold=True,
            size_hint_y=0.15,
            color=COLORS['text']
        )
        self.add_widget(self.name_lbl)
        
        # 状态
        status = self._get_status_text()
        self.status_lbl = CLabel(
            text=status,
            font_size=dp(10),
            size_hint_y=0.12,
            color=COLORS['text_secondary']
        )
        self.add_widget(self.status_lbl)
        
        # 健康条
        health_box = BoxLayout(size_hint_y=0.08, padding=[dp(5), 0])
        self.health_bar = ProgressBar(
            max=100,
            value=self.plant_data.get('health', 100)
        )
        health_box.add_widget(self.health_bar)
        self.add_widget(health_box)
        
        # 打卡按钮或完成标签
        btn_box = BoxLayout(size_hint_y=0.3, padding=[dp(10), dp(5)])
        
        if not self.plant_data.get('is_completed_today'):
            self.check_btn = CButton(
                text='浇灌 ★',
                font_size=dp(11),
                background_color=COLORS['primary_light'],
                background_normal='',
                color=(1, 1, 1, 1)
            )
            self.check_btn.bind(on_press=self._on_check_press)
            
            # 圆角
            with self.check_btn.canvas.before:
                Color(*COLORS['primary_light'])
                self.btn_bg = RoundedRectangle(pos=self.check_btn.pos, 
                                               size=self.check_btn.size, radius=[dp(14)])
            self.check_btn.bind(pos=lambda w, p: setattr(self.btn_bg, 'pos', p),
                               size=lambda w, s: setattr(self.btn_bg, 'size', s))
            
            btn_box.add_widget(self.check_btn)
        else:
            done_lbl = CLabel(
                text='√ 已完成',
                font_size=dp(11),
                bold=True,
                color=COLORS['primary']
            )
            btn_box.add_widget(done_lbl)
        
        self.add_widget(btn_box)
    
    def _get_status_text(self):
        streak = self.plant_data.get('current_streak', 0)
        stage_name = self.plant_data.get('stage_name', '种子')
        
        if self.plant_data.get('needs_water'):
            return "! 需要浇灌"
        elif streak > 0:
            return f"★ {streak}天 · {stage_name}"
        else:
            return f"○ {stage_name}"
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def _update_style(self):
        """根据健康度更新样式"""
        health = self.plant_data.get('health', 100)
        
        if health >= 80:
            border_color = COLORS['primary_light']
        elif health >= 50:
            border_color = COLORS['accent']
        else:
            border_color = (1.0, 0.34, 0.13, 1)  # 橙红色
        
        # 更新边框颜色（这里简化处理，只改背景）
        self.bg_color.rgba = (1, 1, 1, 1)
    
    def _on_check_press(self, *args):
        """打卡按钮点击"""
        habit_id = self.plant_data.get('habit_id', 0)
        self.dispatch('on_check_in', habit_id)
        
        # 播放动画
        self._play_animation()
    
    def _play_animation(self):
        """播放浇水动画"""
        original_icon = self.icon_lbl.text
        self.icon_lbl.text = '~'  # 使用波浪符号替代水滴 emoji
        
        anim = Animation(font_size=dp(42), duration=0.15) + Animation(font_size=dp(36), duration=0.15)
        anim.bind(on_complete=lambda *args: setattr(self.icon_lbl, 'text', original_icon))
        anim.start(self.icon_lbl)
    
    def on_check_in(self, habit_id):
        """打卡事件（供绑定）"""
        pass
    
    def update_data(self, plant_data):
        """更新数据"""
        self.plant_data = plant_data
        
        # 更新图标
        icon_text = plant_data.get('plant_icon', '○')
        if icon_text and len(icon_text) > 0 and ord(icon_text[0]) > 127:
            stage = plant_data.get('growth_stage', 0)
            icons = ['○', '◐', '●', '✿', '❀']
            icon_text = icons[min(stage, len(icons)-1)]
        self.icon_lbl.text = icon_text
        
        self.name_lbl.text = plant_data.get('name', '习惯')
        self.status_lbl.text = self._get_status_text()
        self.health_bar.value = plant_data.get('health', 100)
        self._update_style()
