"""习惯卡片组件 - 支持手机模式"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QFrame, QGraphicsDropShadowEffect,
    QMenu, QAction
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QCursor

from ...utils.constants import CATEGORIES, DIFFICULTY_LEVELS


class HabitCard(QFrame):
    """习惯卡片组件"""
    
    clicked = pyqtSignal(int)
    check_in = pyqtSignal(int)
    edit = pyqtSignal(int)
    delete = pyqtSignal(int)
    
    def __init__(self, habit_data: dict, mobile: bool = False, parent=None):
        super().__init__(parent)
        self.habit_data = habit_data
        self.habit_id = habit_data.get('habit_id', 0)
        self.mobile = mobile
        self._init_ui()
        self._apply_style()
    
    def _init_ui(self):
        self.setCursor(Qt.PointingHandCursor)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        
        layout = QVBoxLayout(self)
        padding = 12 if self.mobile else 20
        layout.setContentsMargins(padding, padding, padding, padding)
        layout.setSpacing(10)
        
        # 顶部
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(self.habit_data.get('icon', '🌱'))
        icon_label.setFont(QFont("Segoe UI Emoji", 22 if self.mobile else 28))
        top_layout.addWidget(icon_label)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        name_label = QLabel(self.habit_data.get('name', ''))
        name_label.setFont(QFont("Microsoft YaHei", 13 if self.mobile else 14, QFont.Bold))
        info_layout.addWidget(name_label)
        
        category = self.habit_data.get('category', 'life')
        cat_info = CATEGORIES.get(category, CATEGORIES['life'])
        cat_label = QLabel(f"{cat_info['icon']} {cat_info['name']}")
        cat_label.setStyleSheet(f"color: {cat_info['color']}; font-size: 11px;")
        info_layout.addWidget(cat_label)
        
        top_layout.addLayout(info_layout, 1)
        
        difficulty = self.habit_data.get('difficulty', 1)
        diff_info = DIFFICULTY_LEVELS.get(difficulty, DIFFICULTY_LEVELS[1])
        diff_label = QLabel('⭐' * difficulty)
        diff_label.setStyleSheet(f"font-size: 10px;")
        top_layout.addWidget(diff_label)
        
        layout.addLayout(top_layout)
        
        # 统计
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        streak = self.habit_data.get('current_streak', 0)
        streak_widget = self._create_stat("🔥", f"{streak}天", "连续")
        stats_layout.addWidget(streak_widget)
        
        total = self.habit_data.get('total_completed', 0)
        total_widget = self._create_stat("✅", str(total), "总次数")
        stats_layout.addWidget(total_widget)
        
        longest = self.habit_data.get('longest_streak', 0)
        longest_widget = self._create_stat("🏆", f"{longest}天", "最长")
        stats_layout.addWidget(longest_widget)
        
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        # 底部
        bottom_layout = QHBoxLayout()
        
        target = self.habit_data.get('target_frequency', 7)
        completed_this_week = min(streak, target)
        
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(3)
        
        progress_label = QLabel(f"本周 {completed_this_week}/{target}")
        progress_label.setStyleSheet("color: #666; font-size: 10px;")
        progress_layout.addWidget(progress_label)
        
        progress_bar = QProgressBar()
        progress_bar.setRange(0, target)
        progress_bar.setValue(completed_this_week)
        progress_bar.setTextVisible(False)
        progress_bar.setFixedHeight(5)
        progress_bar.setStyleSheet("""
            QProgressBar { background-color: #E8E8E8; border-radius: 2px; }
            QProgressBar::chunk { background-color: #4CAF50; border-radius: 2px; }
        """)
        progress_layout.addWidget(progress_bar)
        
        bottom_layout.addLayout(progress_layout, 1)
        
        self.check_btn = QPushButton()
        is_completed = self.habit_data.get('completed_today', False)
        
        if is_completed:
            self.check_btn.setText("✓")
            self.check_btn.setEnabled(False)
            self.check_btn.setStyleSheet("""
                QPushButton {
                    background-color: #81C784; color: white;
                    border: none; border-radius: 15px;
                    padding: 8px 18px; font-weight: bold;
                }
            """)
        else:
            self.check_btn.setText("打卡")
            self.check_btn.clicked.connect(self._on_check_in)
            self.check_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50; color: white;
                    border: none; border-radius: 15px;
                    padding: 8px 18px; font-weight: bold;
                }
            """)
        
        bottom_layout.addWidget(self.check_btn)
        layout.addLayout(bottom_layout)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
    
    def _create_stat(self, icon: str, value: str, label: str) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        
        value_layout = QHBoxLayout()
        value_layout.setSpacing(3)
        
        icon_lbl = QLabel(icon)
        icon_lbl.setFont(QFont("Segoe UI Emoji", 10))
        value_layout.addWidget(icon_lbl)
        
        value_lbl = QLabel(value)
        value_lbl.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        value_layout.addWidget(value_lbl)
        
        layout.addLayout(value_layout)
        
        label_lbl = QLabel(label)
        label_lbl.setStyleSheet("color: #888; font-size: 9px;")
        layout.addWidget(label_lbl)
        
        return widget
    
    def _apply_style(self):
        self.setStyleSheet("""
            HabitCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E8E8E8;
            }
        """)
    
    def _on_check_in(self):
        self.check_in.emit(self.habit_id)
    
    def _show_context_menu(self, pos):
        menu = QMenu(self)
        
        edit_action = QAction("✏️ 编辑", self)
        edit_action.triggered.connect(lambda: self.edit.emit(self.habit_id))
        menu.addAction(edit_action)
        
        delete_action = QAction("🗑️ 删除", self)
        delete_action.triggered.connect(lambda: self.delete.emit(self.habit_id))
        menu.addAction(delete_action)
        
        menu.exec_(QCursor.pos())
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.habit_id)
        super().mousePressEvent(event)


class CompactHabitCard(QFrame):
    """紧凑型习惯卡片"""
    
    clicked = pyqtSignal(int)
    check_in = pyqtSignal(int)
    
    def __init__(self, habit_data: dict, parent=None):
        super().__init__(parent)
        self.habit_data = habit_data
        self.habit_id = habit_data.get('habit_id', 0)
        self._init_ui()
    
    def _init_ui(self):
        self.setFixedHeight(60)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        
        icon = QLabel(self.habit_data.get('icon', '🌱'))
        icon.setFont(QFont("Segoe UI Emoji", 20))
        layout.addWidget(icon)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(1)
        
        name = QLabel(self.habit_data.get('name', ''))
        name.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        info_layout.addWidget(name)
        
        streak = self.habit_data.get('current_streak', 0)
        status = QLabel(f"🔥 连续{streak}天")
        status.setStyleSheet("color: #666; font-size: 10px;")
        info_layout.addWidget(status)
        
        layout.addLayout(info_layout, 1)
        
        is_completed = self.habit_data.get('completed_today', False)
        btn = QPushButton("✓" if is_completed else "打卡")
        btn.setFixedSize(55, 32)
        
        if is_completed:
            btn.setEnabled(False)
            btn.setStyleSheet("background-color: #81C784; color: white; border: none; border-radius: 16px; font-weight: bold;")
        else:
            btn.clicked.connect(lambda: self.check_in.emit(self.habit_id))
            btn.setStyleSheet("background-color: #4CAF50; color: white; border: none; border-radius: 16px; font-weight: bold; font-size: 11px;")
        
        layout.addWidget(btn)
        
        self.setStyleSheet("""
            CompactHabitCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E8E8E8;
            }
        """)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.habit_id)
        super().mousePressEvent(event)
