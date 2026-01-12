"""花园视图 - 手机适配"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QGridLayout,
    QMessageBox, QDialog, QTextEdit
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

from .components.plant_widget import PlantWidget
from ..managers.garden_manager import GardenManager
from ..managers.habit_manager import HabitManager
from ..utils.constants import CATEGORIES
from ..utils.helpers import get_greeting


class CheckInDialog(QDialog):
    """打卡对话框"""
    
    def __init__(self, habit_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"✨ 完成 {habit_name}")
        self.setFixedSize(340, 220)
        self._init_ui(habit_name)
    
    def _init_ui(self, habit_name: str):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel(f"🎉 太棒了！")
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        note_label = QLabel("写点什么？（可选）")
        note_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(note_label)
        
        self.note_edit = QTextEdit()
        self.note_edit.setPlaceholderText("今天的感受...")
        self.note_edit.setMaximumHeight(60)
        layout.addWidget(self.note_edit)
        
        btn_layout = QHBoxLayout()
        
        skip_btn = QPushButton("跳过")
        skip_btn.setStyleSheet("background-color: #E0E0E0; color: #333; padding: 10px 25px; border-radius: 20px;")
        skip_btn.clicked.connect(self.accept)
        btn_layout.addWidget(skip_btn)
        
        save_btn = QPushButton("保存 🌟")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 25px; border-radius: 20px; font-weight: bold;")
        save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def get_note(self) -> str:
        return self.note_edit.toPlainText().strip()


class GardenView(QWidget):
    """花园主视图 - 手机适配"""
    
    habit_selected = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.garden_manager = GardenManager()
        self.habit_manager = HabitManager()
        self.plant_widgets = {}
        self._init_ui()
        self.refresh()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)
        
        # 顶部问候
        self._create_header(layout)
        
        # 快速统计
        self._create_stats_bar(layout)
        
        # 花园网格
        self._create_garden_grid(layout)
    
    def _create_header(self, parent_layout):
        """创建顶部"""
        greeting = get_greeting()
        
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(5, 0, 5, 0)
        header_layout.setSpacing(2)
        
        greeting_label = QLabel(f"{greeting}！")
        greeting_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        header_layout.addWidget(greeting_label)
        
        subtitle = QLabel("看看你的习惯花园 🌱")
        subtitle.setStyleSheet("color: #666; font-size: 13px;")
        header_layout.addWidget(subtitle)
        
        parent_layout.addWidget(header_frame)
    
    def _create_stats_bar(self, parent_layout):
        """创建统计栏"""
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E8E8E8;
            }
        """)
        
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setContentsMargins(15, 12, 15, 12)
        
        self.stats_labels = {}
        stats_items = [
            ("total", "🌿", "植物"),
            ("healthy", "💚", "健康"),
            ("health_rate", "📊", "健康度")
        ]
        
        for i, (key, icon, label) in enumerate(stats_items):
            item_widget = QWidget()
            item_layout = QVBoxLayout(item_widget)
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(2)
            
            value_layout = QHBoxLayout()
            value_layout.setSpacing(3)
            
            icon_lbl = QLabel(icon)
            icon_lbl.setFont(QFont("Segoe UI Emoji", 14))
            value_layout.addWidget(icon_lbl)
            
            value_lbl = QLabel("0")
            value_lbl.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
            value_lbl.setStyleSheet("color: #2E7D32;")
            self.stats_labels[key] = value_lbl
            value_layout.addWidget(value_lbl)
            value_layout.addStretch()
            
            item_layout.addLayout(value_layout)
            
            label_lbl = QLabel(label)
            label_lbl.setStyleSheet("color: #888; font-size: 10px;")
            item_layout.addWidget(label_lbl)
            
            stats_layout.addWidget(item_widget, 1)
        
        parent_layout.addWidget(stats_frame)
    
    def _create_garden_grid(self, parent_layout):
        """创建花园网格"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.garden_container = QWidget()
        self.garden_layout = QGridLayout(self.garden_container)
        self.garden_layout.setSpacing(10)
        self.garden_layout.setContentsMargins(0, 5, 0, 5)
        
        scroll.setWidget(self.garden_container)
        parent_layout.addWidget(scroll, 1)
    
    def refresh(self, category: str = None):
        """刷新花园视图"""
        for widget in self.plant_widgets.values():
            widget.deleteLater()
        self.plant_widgets.clear()
        
        while self.garden_layout.count():
            item = self.garden_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        overview = self.garden_manager.get_garden_overview()
        plants = overview['plants']
        
        today_status = self.habit_manager.get_today_status()
        status_map = {r['habit_id']: r.get('completed_today', False) for r in today_status}
        
        if category and category != 'all':
            plants = [p for p in plants if p['category'] == category]
        
        self.stats_labels['total'].setText(str(overview['total_plants']))
        self.stats_labels['healthy'].setText(str(overview['healthy_plants']))
        self.stats_labels['health_rate'].setText(f"{overview['garden_health']}%")
        
        if not plants:
            empty_label = QLabel("🌱 花园还是空的\n添加第一个习惯吧！")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #888; font-size: 14px; padding: 40px;")
            self.garden_layout.addWidget(empty_label, 0, 0, 1, 2)
            
            add_btn = self._create_add_button()
            self.garden_layout.addWidget(add_btn, 1, 0, 1, 2, Qt.AlignCenter)
            return
        
        # 手机屏幕每行2个
        cols = 2
        for i, plant in enumerate(plants):
            plant['is_completed_today'] = status_map.get(plant['habit_id'], False)
            
            widget = PlantWidget(plant, mobile=True)
            widget.clicked.connect(self._on_plant_clicked)
            widget.check_in_clicked.connect(self._on_check_in)
            
            row = i // cols
            col = i % cols
            self.garden_layout.addWidget(widget, row, col)
            self.plant_widgets[plant['habit_id']] = widget
        
        # 添加新增按钮
        add_btn = self._create_add_button()
        next_pos = len(plants)
        self.garden_layout.addWidget(add_btn, next_pos // cols, next_pos % cols)
    
    def _create_add_button(self) -> QFrame:
        """创建添加按钮"""
        frame = QFrame()
        frame.setFixedSize(165, 180)
        frame.setCursor(Qt.PointingHandCursor)
        frame.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border-radius: 16px;
                border: 2px dashed #BDBDBD;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignCenter)
        
        icon = QLabel("➕")
        icon.setFont(QFont("Segoe UI Emoji", 28))
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)
        
        text = QLabel("添加习惯")
        text.setFont(QFont("Microsoft YaHei", 11))
        text.setStyleSheet("color: #666;")
        text.setAlignment(Qt.AlignCenter)
        layout.addWidget(text)
        
        frame.mousePressEvent = lambda e: self._open_add_habit()
        
        return frame
    
    def _on_plant_clicked(self, habit_id: int):
        self.habit_selected.emit(habit_id)
        if hasattr(self.parent(), 'show_habits'):
            self.parent().show_habits()
    
    def _on_check_in(self, habit_id: int):
        habit = self.habit_manager.get_habit(habit_id)
        if not habit:
            return
        
        dialog = CheckInDialog(habit.name, self)
        if dialog.exec_() == QDialog.Accepted:
            note = dialog.get_note()
            result = self.habit_manager.check_in(habit_id, notes=note)
            
            if result['success']:
                if habit_id in self.plant_widgets:
                    self.plant_widgets[habit_id].play_water_animation()
                
                if result.get('unlocked_achievements'):
                    for ach in result['unlocked_achievements']:
                        QMessageBox.information(self, "🏆 成就解锁！", f"{ach['icon']} {ach['title']}")
                
                QTimer.singleShot(600, self.refresh)
            else:
                QMessageBox.warning(self, "提示", result['message'])
    
    def _open_add_habit(self):
        if hasattr(self.parent(), 'show_habits'):
            self.parent().show_habits()
