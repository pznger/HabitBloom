"""主窗口 - 手机风格UI"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QStackedWidget, QLabel, QFrame,
    QSizePolicy, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from .styles import get_main_stylesheet, COLORS
from .garden_view import GardenView
from .habit_view import HabitView
from .stats_view import StatsView
from .settings_view import SettingsView
from ..managers.reminder_manager import ReminderManager
from ..managers.garden_manager import GardenManager


class BottomNavButton(QPushButton):
    """底部导航按钮"""
    
    def __init__(self, icon: str, text: str, parent=None):
        super().__init__(parent)
        self.icon_text = icon
        self.label_text = text
        self.setCheckable(True)
        self.setFixedHeight(60)
        self.setCursor(Qt.PointingHandCursor)
        self._update_style(False)
    
    def _update_style(self, checked: bool):
        color = "#4CAF50" if checked else "#888888"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {color};
                font-size: 11px;
                padding: 5px;
            }}
        """)
        self.setText(f"{self.icon_text}\n{self.label_text}")
        font = QFont("Segoe UI Emoji", 9)
        self.setFont(font)
    
    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._update_style(checked)


class StatusBar(QFrame):
    """顶部状态栏（模拟手机状态栏）"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(44)
        self.setStyleSheet("""
            QFrame {
                background-color: #4CAF50;
                border: none;
            }
            QLabel {
                color: white;
                font-size: 13px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # 时间（模拟）
        from datetime import datetime
        time_label = QLabel(datetime.now().strftime("%H:%M"))
        time_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        layout.addWidget(time_label)
        
        layout.addStretch()
        
        # App标题
        title = QLabel("🌱 HabitBloom")
        title.setFont(QFont("Microsoft YaHei", 13, QFont.Bold))
        layout.addWidget(title)
        
        layout.addStretch()
        
        # 电池图标（模拟）
        battery = QLabel("🔋")
        layout.addWidget(battery)


class MainWindow(QMainWindow):
    """主窗口 - 手机App风格"""
    
    # 手机屏幕尺寸 (iPhone 14 比例 9:19.5)
    PHONE_WIDTH = 390
    PHONE_HEIGHT = 844
    
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self._init_managers()
        self._init_ui()
        self._start_services()
    
    def _init_managers(self):
        """初始化管理器"""
        self.reminder_manager = ReminderManager(self)
        self.garden_manager = GardenManager()
        self.reminder_manager.reminder_triggered.connect(self._on_reminder)
    
    def _init_ui(self):
        """初始化UI - 手机风格"""
        self.setWindowTitle("HabitBloom")
        
        # 固定手机尺寸
        self.setFixedSize(self.PHONE_WIDTH, self.PHONE_HEIGHT)
        
        # 应用样式
        self.setStyleSheet(get_main_stylesheet(self.dark_mode))
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 垂直布局：状态栏 + 内容 + 底部导航
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 顶部状态栏
        self.status_bar = StatusBar()
        main_layout.addWidget(self.status_bar)
        
        # 内容区域
        self._create_content_area()
        main_layout.addWidget(self.content_area, 1)
        
        # 底部导航栏
        self._create_bottom_nav()
        main_layout.addWidget(self.bottom_nav)
        
        # 添加圆角效果（模拟手机屏幕）
        self.setStyleSheet(self.styleSheet() + """
            QMainWindow {
                border-radius: 20px;
            }
        """)
    
    def _create_content_area(self):
        """创建内容区域"""
        self.content_area = QFrame()
        self.content_area.setObjectName("content")
        
        layout = QVBoxLayout(self.content_area)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 堆叠部件用于切换视图
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        
        # 创建各个视图（传递手机模式标志）
        self.garden_view = GardenView(self)
        self.habit_view = HabitView(self)
        self.stats_view = StatsView(self)
        self.settings_view = SettingsView(self)
        
        # 连接信号
        self.habit_view.habit_updated.connect(self._on_habit_updated)
        self.settings_view.theme_changed.connect(self._apply_theme)
        self.settings_view.data_imported.connect(self._on_data_imported)
        
        self.stack.addWidget(self.garden_view)
        self.stack.addWidget(self.habit_view)
        self.stack.addWidget(self.stats_view)
        self.stack.addWidget(self.settings_view)
    
    def _create_bottom_nav(self):
        """创建底部导航栏"""
        self.bottom_nav = QFrame()
        self.bottom_nav.setObjectName("bottomNav")
        self.bottom_nav.setFixedHeight(70)
        self.bottom_nav.setStyleSheet("""
            QFrame#bottomNav {
                background-color: white;
                border-top: 1px solid #E0E0E0;
            }
        """)
        
        # 添加阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, -2)
        self.bottom_nav.setGraphicsEffect(shadow)
        
        layout = QHBoxLayout(self.bottom_nav)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(0)
        
        # 导航按钮
        self.nav_buttons = []
        nav_items = [
            ("🏡", "花园", 0),
            ("📋", "习惯", 1),
            ("📊", "统计", 2),
            ("⚙️", "设置", 3)
        ]
        
        for icon, text, index in nav_items:
            btn = BottomNavButton(icon, text)
            btn.clicked.connect(lambda checked, idx=index: self._switch_view(idx))
            self.nav_buttons.append(btn)
            layout.addWidget(btn, 1)
        
        # 默认选中花园
        self.nav_buttons[0].setChecked(True)
    
    def _start_services(self):
        """启动后台服务"""
        self.reminder_manager.start_reminder_service()
        self._update_plants_health()
        
        self.health_timer = QTimer(self)
        self.health_timer.timeout.connect(self._update_plants_health)
        self.health_timer.start(3600000)
    
    def _switch_view(self, index: int):
        """切换视图"""
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        
        self.stack.setCurrentIndex(index)
        
        current_view = self.stack.currentWidget()
        if hasattr(current_view, 'refresh'):
            current_view.refresh()
    
    def _apply_theme(self, dark_mode: bool):
        """应用主题"""
        self.dark_mode = dark_mode
        self.setStyleSheet(get_main_stylesheet(dark_mode))
    
    def _on_reminder(self, reminder_data: dict):
        """处理提醒"""
        QMessageBox.information(
            self,
            f"{reminder_data['habit_icon']} 习惯提醒",
            reminder_data['message'],
            QMessageBox.Ok
        )
        self.activateWindow()
        self.raise_()
    
    def _on_habit_updated(self):
        """习惯更新时刷新花园视图"""
        self.garden_view.refresh()
    
    def _on_data_imported(self):
        """数据导入后刷新所有视图"""
        self.garden_view.refresh()
        self.habit_view.refresh()
        self.stats_view.refresh()
    
    def _update_plants_health(self):
        """更新植物健康状态"""
        self.garden_manager.update_all_plants_health()
    
    def closeEvent(self, event):
        """关闭事件"""
        self.reminder_manager.stop_reminder_service()
        if hasattr(self, 'health_timer'):
            self.health_timer.stop()
        event.accept()
    
    def show_garden(self):
        self._switch_view(0)
    
    def show_habits(self):
        self._switch_view(1)
    
    def show_stats(self):
        self._switch_view(2)
    
    def show_settings(self):
        self._switch_view(3)
