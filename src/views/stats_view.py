"""统计视图 - 手机适配"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QScrollArea, QFrame, QProgressBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QColor, QPen
from datetime import date

from ..managers.stats_manager import StatsManager
from ..utils.constants import CATEGORIES


class StatCard(QFrame):
    """统计卡片"""
    
    def __init__(self, icon: str, value: str, label: str, color: str = "#4CAF50", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E8E8E8;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(5)
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 20))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        
        label_label = QLabel(label)
        label_label.setStyleSheet("color: #666; font-size: 10px;")
        label_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_label)


class ProgressRing(QWidget):
    """进度环"""
    
    def __init__(self, value: int, max_value: int = 100, parent=None):
        super().__init__(parent)
        self.value = value
        self.max_value = max_value
        self.setFixedSize(90, 90)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor("#E8E8E8"))
        pen.setWidth(8)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawArc(10, 10, 70, 70, 0, 360 * 16)
        
        if self.value > 0:
            pen.setColor(QColor("#4CAF50"))
            painter.setPen(pen)
            span = int((self.value / self.max_value) * 360 * 16)
            painter.drawArc(10, 10, 70, 70, 90 * 16, -span)
        
        painter.setPen(QColor("#333"))
        painter.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.value}%")


class WeeklyChart(QFrame):
    """周统计图表"""
    
    def __init__(self, data: list, parent=None):
        super().__init__(parent)
        self.data = data
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E8E8E8;
            }
        """)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(10)
        
        title = QLabel("📊 本周")
        title.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        layout.addWidget(title)
        
        chart_layout = QHBoxLayout()
        chart_layout.setSpacing(8)
        
        max_val = max((d['completed'] for d in self.data), default=1)
        
        for day_data in self.data:
            day_layout = QVBoxLayout()
            day_layout.setAlignment(Qt.AlignBottom)
            day_layout.setSpacing(3)
            
            count = QLabel(str(day_data['completed']))
            count.setAlignment(Qt.AlignCenter)
            count.setStyleSheet("color: #666; font-size: 9px;")
            day_layout.addWidget(count)
            
            bar = QFrame()
            height = max(8, int((day_data['completed'] / max_val) * 60)) if max_val > 0 else 8
            bar.setFixedSize(24, height)
            
            is_today = day_data['date'] == date.today()
            bar.setStyleSheet(f"""
                QFrame {{
                    background-color: {'#4CAF50' if is_today else '#81C784'};
                    border-radius: 4px;
                }}
            """)
            day_layout.addWidget(bar, alignment=Qt.AlignCenter)
            
            day_name = QLabel(day_data['day_name'][:1])
            day_name.setAlignment(Qt.AlignCenter)
            day_name.setStyleSheet(f"font-size: 10px; color: {'#4CAF50' if is_today else '#888'};")
            day_layout.addWidget(day_name)
            
            chart_layout.addLayout(day_layout)
        
        layout.addLayout(chart_layout)


class AchievementCard(QFrame):
    """成就卡片"""
    
    def __init__(self, achievement, parent=None):
        super().__init__(parent)
        self.achievement = achievement
        self._init_ui()
    
    def _init_ui(self):
        self.setFixedSize(80, 90)
        
        is_unlocked = self.achievement.is_unlocked
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {'#FFF8E1' if is_unlocked else '#F5F5F5'};
                border-radius: 12px;
                border: 2px solid {'#FFB74D' if is_unlocked else '#E0E0E0'};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)
        
        icon = QLabel(self.achievement.badge_icon if is_unlocked else "🔒")
        icon.setFont(QFont("Segoe UI Emoji", 22))
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)
        
        title = QLabel(self.achievement.title[:4] + "..." if len(self.achievement.title) > 4 else self.achievement.title)
        title.setFont(QFont("Microsoft YaHei", 9))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {'#333' if is_unlocked else '#999'};")
        layout.addWidget(title)


class StatsView(QWidget):
    """统计视图 - 手机适配"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stats_manager = StatsManager()
        self._init_ui()
        self.refresh()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)
        
        header = QHBoxLayout()
        title = QLabel("📊 统计")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        header.addWidget(title)
        header.addStretch()
        
        today = date.today()
        month_label = QLabel(f"{today.month}月")
        month_label.setStyleSheet("color: #666; font-size: 13px;")
        header.addWidget(month_label)
        
        layout.addLayout(header)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(12)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def refresh(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
        
        overview = self.stats_manager.get_overview_stats()
        weekly = self.stats_manager.get_weekly_stats()
        monthly = self.stats_manager.get_monthly_stats()
        achievements = self.stats_manager.get_achievements()
        
        # 概览卡片 (2x2网格)
        grid1 = QHBoxLayout()
        grid1.setSpacing(8)
        grid1.addWidget(StatCard("📋", str(overview['total_habits']), "习惯", "#2196F3"))
        grid1.addWidget(StatCard("✅", str(overview['completed_today']), "今日", "#4CAF50"))
        self.content_layout.addLayout(grid1)
        
        grid2 = QHBoxLayout()
        grid2.setSpacing(8)
        grid2.addWidget(StatCard("🔥", str(overview['current_max_streak']), "连续", "#FF9800"))
        grid2.addWidget(StatCard("🏆", str(overview['longest_ever_streak']), "最长", "#9C27B0"))
        self.content_layout.addLayout(grid2)
        
        # 月度完成率
        rate_frame = QFrame()
        rate_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E8E8E8;
            }
        """)
        rate_layout = QHBoxLayout(rate_frame)
        rate_layout.setContentsMargins(15, 15, 15, 15)
        
        ring = ProgressRing(int(monthly['completion_rate']))
        rate_layout.addWidget(ring)
        
        details = QVBoxLayout()
        details.setSpacing(5)
        
        rate_title = QLabel("本月完成率")
        rate_title.setFont(QFont("Microsoft YaHei", 13, QFont.Bold))
        details.addWidget(rate_title)
        
        completed_text = QLabel(f"完成 {monthly['total_completed']}/{monthly['expected_completions']}")
        completed_text.setStyleSheet("color: #666; font-size: 11px;")
        details.addWidget(completed_text)
        
        trend_icon = "📈" if monthly.get('trend') == 'up' else ("📉" if monthly.get('trend') == 'down' else "➡️")
        trend = QLabel(f"{trend_icon} {'上升' if monthly.get('trend') == 'up' else ('下降' if monthly.get('trend') == 'down' else '稳定')}")
        trend.setStyleSheet("color: #4CAF50;" if monthly.get('trend') == 'up' else "color: #666;")
        details.addWidget(trend)
        
        rate_layout.addLayout(details, 1)
        self.content_layout.addWidget(rate_frame)
        
        # 周统计
        if weekly.get('daily_data'):
            weekly_chart = WeeklyChart(weekly['daily_data'])
            self.content_layout.addWidget(weekly_chart)
        
        # 成就
        ach_label = QLabel(f"🏆 成就 ({achievements['unlocked_count']}/{achievements['total']})")
        ach_label.setFont(QFont("Microsoft YaHei", 13, QFont.Bold))
        self.content_layout.addWidget(ach_label)
        
        ach_layout = QHBoxLayout()
        ach_layout.setSpacing(8)
        
        all_achs = achievements['unlocked'] + achievements['locked']
        for ach in all_achs[:4]:
            card = AchievementCard(ach)
            ach_layout.addWidget(card)
        
        ach_layout.addStretch()
        self.content_layout.addLayout(ach_layout)
        
        self.content_layout.addStretch()
    
    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
