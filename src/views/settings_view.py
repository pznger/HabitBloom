"""设置视图 - 手机适配"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QLineEdit,
    QFileDialog, QMessageBox, QCheckBox, QTimeEdit
)
from PyQt5.QtCore import Qt, pyqtSignal, QTime
from PyQt5.QtGui import QFont
import os
from datetime import datetime

from ..database.db_manager import DatabaseManager
from ..utils.helpers import get_backup_dir, export_data_to_json, import_data_from_json
from ..utils.constants import APP_NAME, APP_VERSION


class SettingsSection(QFrame):
    """设置区块"""
    
    def __init__(self, title: str, icon: str = "", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E8E8E8;
            }
        """)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 12, 15, 12)
        self.main_layout.setSpacing(10)
        
        title_label = QLabel(f"{icon} {title}" if icon else title)
        title_label.setFont(QFont("Microsoft YaHei", 13, QFont.Bold))
        self.main_layout.addWidget(title_label)
    
    def add_widget(self, widget):
        self.main_layout.addWidget(widget)
    
    def add_layout(self, layout):
        self.main_layout.addLayout(layout)


class SettingsView(QWidget):
    """设置视图 - 手机适配"""
    
    theme_changed = pyqtSignal(bool)
    data_imported = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)
        
        title = QLabel("⚙️ 设置")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(12)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        self._create_user_section(content_layout)
        self._create_theme_section(content_layout)
        self._create_data_section(content_layout)
        self._create_about_section(content_layout)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def _create_user_section(self, parent_layout):
        """用户设置"""
        section = SettingsSection("用户信息", "👤")
        
        name_layout = QHBoxLayout()
        name_label = QLabel("昵称")
        name_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        user = self.db.get_user()
        if user:
            self.name_input.setText(user.username)
        self.name_input.setPlaceholderText("输入昵称")
        self.name_input.setStyleSheet("padding: 8px; border-radius: 6px; border: 1px solid #E0E0E0;")
        name_layout.addWidget(self.name_input, 1)
        
        section.add_layout(name_layout)
        
        save_btn = QPushButton("保存")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; color: white;
                padding: 10px; border-radius: 20px;
            }
        """)
        save_btn.clicked.connect(self._save_user)
        section.add_widget(save_btn)
        
        parent_layout.addWidget(section)
    
    def _create_theme_section(self, parent_layout):
        """主题设置"""
        section = SettingsSection("外观", "🎨")
        
        dark_layout = QHBoxLayout()
        dark_label = QLabel("深色模式")
        dark_layout.addWidget(dark_label)
        dark_layout.addStretch()
        
        self.dark_check = QCheckBox()
        self.dark_check.stateChanged.connect(self._toggle_dark_mode)
        dark_layout.addWidget(self.dark_check)
        
        section.add_layout(dark_layout)
        parent_layout.addWidget(section)
    
    def _create_data_section(self, parent_layout):
        """数据管理"""
        section = SettingsSection("数据管理", "💾")
        
        # 导出
        export_layout = QHBoxLayout()
        export_label = QLabel("导出数据")
        export_layout.addWidget(export_label)
        export_layout.addStretch()
        
        export_btn = QPushButton("导出")
        export_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px 16px; border-radius: 15px;")
        export_btn.clicked.connect(self._export_data)
        export_layout.addWidget(export_btn)
        
        section.add_layout(export_layout)
        
        # 导入
        import_layout = QHBoxLayout()
        import_label = QLabel("恢复数据")
        import_layout.addWidget(import_label)
        import_layout.addStretch()
        
        import_btn = QPushButton("导入")
        import_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 8px 16px; border-radius: 15px;")
        import_btn.clicked.connect(self._import_data)
        import_layout.addWidget(import_btn)
        
        section.add_layout(import_layout)
        
        # 清除
        clear_layout = QHBoxLayout()
        clear_label = QLabel("清除所有数据")
        clear_label.setStyleSheet("color: #F44336;")
        clear_layout.addWidget(clear_label)
        clear_layout.addStretch()
        
        clear_btn = QPushButton("清除")
        clear_btn.setStyleSheet("background-color: #F44336; color: white; padding: 8px 16px; border-radius: 15px;")
        clear_btn.clicked.connect(self._clear_data)
        clear_layout.addWidget(clear_btn)
        
        section.add_layout(clear_layout)
        
        parent_layout.addWidget(section)
    
    def _create_about_section(self, parent_layout):
        """关于"""
        section = SettingsSection("关于", "ℹ️")
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        app_name = QLabel(f"🌱 {APP_NAME}")
        app_name.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        info_layout.addWidget(app_name)
        
        version = QLabel(f"版本 {APP_VERSION}")
        version.setStyleSheet("color: #666; font-size: 11px;")
        info_layout.addWidget(version)
        
        desc = QLabel("让习惯如花般绽放")
        desc.setStyleSheet("color: #888; font-size: 11px;")
        info_layout.addWidget(desc)
        
        section.add_layout(info_layout)
        parent_layout.addWidget(section)
    
    def _save_user(self):
        user = self.db.get_user()
        if user:
            user.username = self.name_input.text().strip() or "用户"
            self.db.update_user(user)
            QMessageBox.information(self, "成功", "已保存！")
    
    def _toggle_dark_mode(self, state):
        self.theme_changed.emit(state == Qt.Checked)
    
    def _export_data(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出", 
            os.path.join(get_backup_dir(), f"backup_{datetime.now().strftime('%Y%m%d')}.json"),
            "JSON (*.json)"
        )
        
        if file_path:
            data = self.db.export_all_data()
            if export_data_to_json(data, file_path):
                QMessageBox.information(self, "成功", "导出完成！")
            else:
                QMessageBox.warning(self, "失败", "导出失败")
    
    def _import_data(self):
        reply = QMessageBox.warning(
            self, "警告", "导入将覆盖现有数据！",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", get_backup_dir(), "JSON (*.json)")
        
        if file_path:
            data = import_data_from_json(file_path)
            if data and self.db.import_all_data(data):
                QMessageBox.information(self, "成功", "恢复完成！")
                self.data_imported.emit()
            else:
                QMessageBox.warning(self, "失败", "导入失败")
    
    def _clear_data(self):
        reply = QMessageBox.warning(
            self, "⚠️ 危险", "删除所有数据？\n此操作不可撤销！",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "完成", "已清除")
            self.data_imported.emit()
    
    def refresh(self):
        user = self.db.get_user()
        if user:
            self.name_input.setText(user.username)
