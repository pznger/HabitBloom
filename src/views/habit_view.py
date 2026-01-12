"""习惯管理视图 - 手机适配"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QDialog,
    QLineEdit, QComboBox, QSpinBox, QMessageBox,
    QTabWidget, QCalendarWidget
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QFont

from .components.habit_card import HabitCard, CompactHabitCard
from ..managers.habit_manager import HabitManager
from ..database.db_manager import DatabaseManager
from ..utils.constants import CATEGORIES, PLANT_TYPES, DIFFICULTY_LEVELS


class AddHabitDialog(QDialog):
    """添加习惯对话框 - 手机适配"""
    
    def __init__(self, habit_data: dict = None, parent=None):
        super().__init__(parent)
        self.habit_data = habit_data
        self.setWindowTitle("编辑习惯" if habit_data else "添加习惯")
        self.setFixedSize(360, 480)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("🌱 " + ("编辑习惯" if self.habit_data else "新习惯"))
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        layout.addWidget(title)
        
        # 名称
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("习惯名称（如：每日阅读）")
        self.name_input.setStyleSheet("padding: 12px; font-size: 14px; border-radius: 8px; border: 1px solid #E0E0E0;")
        if self.habit_data:
            self.name_input.setText(self.habit_data.get('name', ''))
        layout.addWidget(self.name_input)
        
        # 图标选择
        icon_layout = QHBoxLayout()
        icon_label = QLabel("图标")
        icon_label.setStyleSheet("font-weight: bold;")
        icon_layout.addWidget(icon_label)
        
        self.icon_combo = QComboBox()
        icons = ['🌱', '📚', '🏃', '💧', '🧘', '✍️', '💪', '🎯', '⏰', '🎵']
        for icon in icons:
            self.icon_combo.addItem(icon, icon)
        if self.habit_data and self.habit_data.get('icon') in icons:
            self.icon_combo.setCurrentIndex(icons.index(self.habit_data.get('icon')))
        self.icon_combo.setStyleSheet("padding: 8px; font-size: 18px;")
        icon_layout.addWidget(self.icon_combo, 1)
        layout.addLayout(icon_layout)
        
        # 类别
        cat_layout = QHBoxLayout()
        cat_label = QLabel("类别")
        cat_label.setStyleSheet("font-weight: bold;")
        cat_layout.addWidget(cat_label)
        
        self.category_combo = QComboBox()
        for key, info in CATEGORIES.items():
            self.category_combo.addItem(f"{info['icon']} {info['name']}", key)
        if self.habit_data:
            for i in range(self.category_combo.count()):
                if self.category_combo.itemData(i) == self.habit_data.get('category'):
                    self.category_combo.setCurrentIndex(i)
                    break
        self.category_combo.setStyleSheet("padding: 8px;")
        cat_layout.addWidget(self.category_combo, 1)
        layout.addLayout(cat_layout)
        
        # 植物类型
        plant_layout = QHBoxLayout()
        plant_label = QLabel("植物")
        plant_label.setStyleSheet("font-weight: bold;")
        plant_layout.addWidget(plant_label)
        
        self.plant_combo = QComboBox()
        for key, info in PLANT_TYPES.items():
            self.plant_combo.addItem(f"{info['icon']} {info['name']}", key)
        if self.habit_data:
            for i in range(self.plant_combo.count()):
                if self.plant_combo.itemData(i) == self.habit_data.get('plant_type'):
                    self.plant_combo.setCurrentIndex(i)
                    break
        self.plant_combo.setStyleSheet("padding: 8px;")
        plant_layout.addWidget(self.plant_combo, 1)
        layout.addLayout(plant_layout)
        
        # 频率和难度
        row_layout = QHBoxLayout()
        
        freq_layout = QVBoxLayout()
        freq_label = QLabel("每周目标")
        freq_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        freq_layout.addWidget(freq_label)
        self.freq_spin = QSpinBox()
        self.freq_spin.setRange(1, 7)
        self.freq_spin.setValue(self.habit_data.get('target_frequency', 7) if self.habit_data else 7)
        self.freq_spin.setStyleSheet("padding: 8px;")
        freq_layout.addWidget(self.freq_spin)
        row_layout.addLayout(freq_layout)
        
        diff_layout = QVBoxLayout()
        diff_label = QLabel("难度")
        diff_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        diff_layout.addWidget(diff_label)
        self.diff_combo = QComboBox()
        for level, info in DIFFICULTY_LEVELS.items():
            self.diff_combo.addItem(f"{'⭐' * level}", level)
        if self.habit_data:
            self.diff_combo.setCurrentIndex(self.habit_data.get('difficulty', 1) - 1)
        self.diff_combo.setStyleSheet("padding: 8px;")
        diff_layout.addWidget(self.diff_combo)
        row_layout.addLayout(diff_layout)
        
        layout.addLayout(row_layout)
        layout.addStretch()
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("background-color: #E0E0E0; color: #333; padding: 12px; border-radius: 20px;")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("保存")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 12px; border-radius: 20px; font-weight: bold;")
        save_btn.clicked.connect(self._on_save)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def _on_save(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "提示", "请输入习惯名称")
            return
        self.accept()
    
    def get_data(self) -> dict:
        return {
            'name': self.name_input.text().strip(),
            'icon': self.icon_combo.currentData(),
            'category': self.category_combo.currentData(),
            'plant_type': self.plant_combo.currentData(),
            'target_frequency': self.freq_spin.value(),
            'difficulty': self.diff_combo.currentData()
        }


class HabitView(QWidget):
    """习惯管理视图 - 手机适配"""
    
    habit_updated = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_manager = HabitManager()
        self._init_ui()
        self.refresh()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)
        
        # 顶部
        header = QHBoxLayout()
        
        title = QLabel("📋 我的习惯")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        header.addWidget(title)
        
        header.addStretch()
        
        add_btn = QPushButton("➕")
        add_btn.setFixedSize(40, 40)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; color: white;
                border-radius: 20px; font-size: 18px;
            }
        """)
        add_btn.clicked.connect(self._add_habit)
        header.addWidget(add_btn)
        
        layout.addLayout(header)
        
        # 标签页
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; }
            QTabBar::tab {
                padding: 8px 20px;
                border-radius: 15px;
                background: #E8E8E8;
                margin-right: 5px;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background: #4CAF50;
                color: white;
                font-weight: bold;
            }
        """)
        
        self.today_tab = QWidget()
        self._create_today_tab()
        self.tabs.addTab(self.today_tab, "今日")
        
        self.all_tab = QWidget()
        self._create_all_tab()
        self.tabs.addTab(self.all_tab, "全部")
        
        layout.addWidget(self.tabs)
    
    def _create_today_tab(self):
        layout = QVBoxLayout(self.today_tab)
        layout.setContentsMargins(0, 10, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        self.today_container = QWidget()
        self.today_layout = QVBoxLayout(self.today_container)
        self.today_layout.setSpacing(10)
        self.today_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll.setWidget(self.today_container)
        layout.addWidget(scroll)
    
    def _create_all_tab(self):
        layout = QVBoxLayout(self.all_tab)
        layout.setContentsMargins(0, 10, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        self.all_container = QWidget()
        self.all_layout = QVBoxLayout(self.all_container)
        self.all_layout.setSpacing(10)
        self.all_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll.setWidget(self.all_container)
        layout.addWidget(scroll)
    
    def refresh(self):
        self._refresh_today()
        self._refresh_all()
    
    def _refresh_today(self):
        while self.today_layout.count():
            item = self.today_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        today_data = self.habit_manager.get_today_status()
        
        if not today_data:
            empty = QLabel("🌱 还没有习惯\n点击右上角添加")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("color: #888; font-size: 14px; padding: 40px;")
            self.today_layout.addWidget(empty)
            return
        
        pending = [h for h in today_data if not h.get('completed_today')]
        completed = [h for h in today_data if h.get('completed_today')]
        
        if pending:
            label = QLabel(f"⏳ 待完成 ({len(pending)})")
            label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
            label.setStyleSheet("color: #FF9800;")
            self.today_layout.addWidget(label)
            
            for habit in pending:
                card = CompactHabitCard(habit)
                card.check_in.connect(self._check_in)
                self.today_layout.addWidget(card)
        
        if completed:
            label = QLabel(f"✅ 已完成 ({len(completed)})")
            label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
            label.setStyleSheet("color: #4CAF50; margin-top: 10px;")
            self.today_layout.addWidget(label)
            
            for habit in completed:
                card = CompactHabitCard(habit)
                self.today_layout.addWidget(card)
        
        self.today_layout.addStretch()
    
    def _refresh_all(self):
        while self.all_layout.count():
            item = self.all_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        habits = self.habit_manager.get_all_habits()
        today_data = self.habit_manager.get_today_status()
        status_map = {h['habit_id']: h.get('completed_today', False) for h in today_data}
        
        if not habits:
            empty = QLabel("🌱 还没有习惯")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("color: #888; font-size: 14px; padding: 40px;")
            self.all_layout.addWidget(empty)
            return
        
        for habit in habits:
            habit_dict = habit.to_dict()
            habit_dict['completed_today'] = status_map.get(habit.habit_id, False)
            
            card = HabitCard(habit_dict, mobile=True)
            card.check_in.connect(self._check_in)
            card.edit.connect(self._edit_habit)
            card.delete.connect(self._delete_habit)
            self.all_layout.addWidget(card)
        
        self.all_layout.addStretch()
    
    def _add_habit(self):
        dialog = AddHabitDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if self.habit_manager.create_habit(**data):
                self.refresh()
                self.habit_updated.emit()
                QMessageBox.information(self, "成功", "习惯创建成功！🌱")
    
    def _edit_habit(self, habit_id: int):
        habit = self.habit_manager.get_habit(habit_id)
        if not habit:
            return
        
        dialog = AddHabitDialog(habit.to_dict(), parent=self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if self.habit_manager.update_habit(habit_id, **data):
                self.refresh()
                self.habit_updated.emit()
    
    def _delete_habit(self, habit_id: int):
        reply = QMessageBox.question(
            self, "确认删除", 
            "确定要删除这个习惯吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.habit_manager.delete_habit(habit_id):
                self.refresh()
                self.habit_updated.emit()
    
    def _check_in(self, habit_id: int):
        result = self.habit_manager.check_in(habit_id)
        if result['success']:
            self.refresh()
            self.habit_updated.emit()
            
            if result.get('unlocked_achievements'):
                for ach in result['unlocked_achievements']:
                    QMessageBox.information(self, "🏆 成就解锁！", f"{ach['icon']} {ach['title']}")
