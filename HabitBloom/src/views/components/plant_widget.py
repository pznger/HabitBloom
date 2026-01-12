"""植物组件 - 支持手机模式"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor

from ...utils.constants import PLANT_TYPES, GROWTH_STAGES


class PlantWidget(QFrame):
    """植物展示组件"""
    
    clicked = pyqtSignal(int)
    check_in_clicked = pyqtSignal(int)
    
    def __init__(self, plant_data: dict, mobile: bool = False, parent=None):
        super().__init__(parent)
        self.plant_data = plant_data
        self.habit_id = plant_data.get('habit_id', 0)
        self.mobile = mobile
        self._init_ui()
        self._apply_style()
    
    def _init_ui(self):
        # 手机模式使用更小的尺寸
        if self.mobile:
            self.setFixedSize(165, 180)
        else:
            self.setFixedSize(180, 220)
        
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        margins = 10 if self.mobile else 15
        layout.setContentsMargins(margins, margins, margins, margins)
        layout.setSpacing(6 if self.mobile else 8)
        
        # 植物图标
        icon_size = 36 if self.mobile else 48
        self.plant_icon = QLabel(self.plant_data.get('plant_icon', '🌱'))
        self.plant_icon.setFont(QFont("Segoe UI Emoji", icon_size))
        self.plant_icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.plant_icon)
        
        # 习惯名称
        font_size = 11 if self.mobile else 12
        self.name_label = QLabel(self.plant_data.get('name', '习惯'))
        self.name_label.setFont(QFont("Microsoft YaHei", font_size, QFont.Bold))
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label)
        
        # 状态标签
        status = self._get_status_text()
        self.status_label = QLabel(status)
        self.status_label.setFont(QFont("Microsoft YaHei", 9 if self.mobile else 10))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #666;")
        layout.addWidget(self.status_label)
        
        # 健康度进度条
        self.health_bar = QProgressBar()
        self.health_bar.setRange(0, 100)
        self.health_bar.setValue(self.plant_data.get('health', 100))
        self.health_bar.setTextVisible(False)
        self.health_bar.setFixedHeight(5)
        layout.addWidget(self.health_bar)
        
        # 打卡按钮
        if not self.plant_data.get('is_completed_today'):
            self.check_btn = QPushButton("浇灌 💧")
            self.check_btn.setFixedHeight(28 if self.mobile else 32)
            self.check_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 14px;
                    font-size: 11px;
                    font-weight: bold;
                }
                QPushButton:pressed {
                    background-color: #388E3C;
                }
            """)
            self.check_btn.clicked.connect(self._on_check_in)
            layout.addWidget(self.check_btn)
        else:
            done_label = QLabel("✅ 已完成")
            done_label.setAlignment(Qt.AlignCenter)
            done_label.setStyleSheet("color: #388E3C; font-weight: bold; font-size: 11px;")
            layout.addWidget(done_label)
        
        # 阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)
    
    def _get_status_text(self) -> str:
        streak = self.plant_data.get('current_streak', 0)
        stage_name = self.plant_data.get('stage_name', '种子')
        
        if self.plant_data.get('needs_water'):
            return "🔔 需要浇灌"
        elif streak > 0:
            return f"🔥 {streak}天 · {stage_name}"
        else:
            return f"🌱 {stage_name}"
    
    def _apply_style(self):
        health = self.plant_data.get('health', 100)
        
        if health >= 80:
            border_color = "#4CAF50"
            bar_color = "#4CAF50"
        elif health >= 50:
            border_color = "#FFC107"
            bar_color = "#FFC107"
        else:
            border_color = "#FF5722"
            bar_color = "#FF5722"
        
        self.setStyleSheet(f"""
            PlantWidget {{
                background-color: white;
                border-radius: 16px;
                border: 2px solid {border_color};
            }}
            QProgressBar {{
                background-color: #E8E8E8;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background-color: {bar_color};
                border-radius: 2px;
            }}
        """)
    
    def _on_check_in(self):
        self.check_in_clicked.emit(self.habit_id)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.habit_id)
        super().mousePressEvent(event)
    
    def play_water_animation(self):
        self._scale_animation = QPropertyAnimation(self, b"geometry")
        self._scale_animation.setDuration(300)
        
        current_geo = self.geometry()
        expanded_geo = current_geo.adjusted(-3, -3, 3, 3)
        
        self._scale_animation.setStartValue(current_geo)
        self._scale_animation.setKeyValueAt(0.5, expanded_geo)
        self._scale_animation.setEndValue(current_geo)
        self._scale_animation.setEasingCurve(QEasingCurve.OutElastic)
        self._scale_animation.start()
        
        original_icon = self.plant_icon.text()
        self.plant_icon.setText("💧")
        QTimer.singleShot(500, lambda: self.plant_icon.setText(original_icon))
    
    def update_data(self, plant_data: dict):
        self.plant_data = plant_data
        self.plant_icon.setText(plant_data.get('plant_icon', '🌱'))
        self.name_label.setText(plant_data.get('name', '习惯'))
        self.status_label.setText(self._get_status_text())
        self.health_bar.setValue(plant_data.get('health', 100))
        self._apply_style()


class MiniPlantWidget(QFrame):
    """迷你植物组件（用于列表显示）"""
    
    clicked = pyqtSignal(int)
    
    def __init__(self, plant_data: dict, parent=None):
        super().__init__(parent)
        self.plant_data = plant_data
        self.habit_id = plant_data.get('habit_id', 0)
        self._init_ui()
    
    def _init_ui(self):
        self.setFixedHeight(55)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        icon_label = QLabel(self.plant_data.get('plant_icon', '🌱'))
        icon_label.setFont(QFont("Segoe UI Emoji", 20))
        layout.addWidget(icon_label)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(1)
        
        name_label = QLabel(self.plant_data.get('name', ''))
        name_label.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        info_layout.addWidget(name_label)
        
        status = f"连续{self.plant_data.get('current_streak', 0)}天"
        status_label = QLabel(status)
        status_label.setStyleSheet("color: #666; font-size: 10px;")
        info_layout.addWidget(status_label)
        
        layout.addLayout(info_layout, 1)
        
        if self.plant_data.get('is_completed_today'):
            done = QLabel("✅")
            done.setFont(QFont("Segoe UI Emoji", 16))
            layout.addWidget(done)
        
        self.setStyleSheet("""
            MiniPlantWidget {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E0E0E0;
            }
        """)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.habit_id)
        super().mousePressEvent(event)
