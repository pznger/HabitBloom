"""全局样式定义"""

# 主题颜色
COLORS = {
    'primary': '#2E7D32',        # 深绿色
    'primary_light': '#4CAF50',  # 主绿色
    'primary_dark': '#1B5E20',   # 墨绿色
    'secondary': '#81C784',      # 浅绿色
    'accent': '#FFB74D',         # 橙黄色强调
    'background': '#F1F8E9',     # 浅绿背景
    'surface': '#FFFFFF',        # 白色表面
    'text_primary': '#1B5E20',   # 主文字
    'text_secondary': '#558B2F', # 次要文字
    'text_light': '#7CB342',     # 浅色文字
    'error': '#D32F2F',          # 错误红
    'success': '#388E3C',        # 成功绿
    'border': '#C8E6C9',         # 边框色
    'shadow': 'rgba(0, 0, 0, 0.1)'
}

# 深色主题
DARK_COLORS = {
    'primary': '#4CAF50',
    'primary_light': '#81C784',
    'primary_dark': '#2E7D32',
    'secondary': '#A5D6A7',
    'accent': '#FFB74D',
    'background': '#1A1A2E',
    'surface': '#16213E',
    'text_primary': '#E8F5E9',
    'text_secondary': '#A5D6A7',
    'text_light': '#81C784',
    'error': '#EF5350',
    'success': '#66BB6A',
    'border': '#2E7D32',
    'shadow': 'rgba(0, 0, 0, 0.3)'
}


def get_main_stylesheet(dark_mode=False):
    """获取主样式表"""
    c = DARK_COLORS if dark_mode else COLORS
    
    return f"""
    /* 全局样式 */
    QWidget {{
        font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
        font-size: 14px;
        color: {c['text_primary']};
    }}
    
    QMainWindow {{
        background-color: {c['background']};
    }}
    
    /* 导航栏 */
    #navbar {{
        background-color: {c['surface']};
        border-right: 1px solid {c['border']};
        padding: 10px 5px;
    }}
    
    #navbar QPushButton {{
        background-color: transparent;
        border: none;
        border-radius: 12px;
        padding: 15px;
        margin: 5px;
        font-size: 20px;
        min-width: 50px;
        min-height: 50px;
    }}
    
    #navbar QPushButton:hover {{
        background-color: {c['secondary']};
    }}
    
    #navbar QPushButton:checked {{
        background-color: {c['primary']};
        color: white;
    }}
    
    /* 内容区域 */
    #content {{
        background-color: {c['background']};
        padding: 20px;
    }}
    
    /* 卡片样式 */
    .card {{
        background-color: {c['surface']};
        border-radius: 16px;
        padding: 20px;
        border: 1px solid {c['border']};
    }}
    
    /* 标题样式 */
    .title {{
        font-size: 24px;
        font-weight: bold;
        color: {c['text_primary']};
        margin-bottom: 10px;
    }}
    
    .subtitle {{
        font-size: 16px;
        color: {c['text_secondary']};
    }}
    
    /* 按钮样式 */
    QPushButton {{
        background-color: {c['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: bold;
    }}
    
    QPushButton:hover {{
        background-color: {c['primary_dark']};
    }}
    
    QPushButton:pressed {{
        background-color: {c['primary_dark']};
    }}
    
    QPushButton:disabled {{
        background-color: {c['border']};
        color: {c['text_light']};
    }}
    
    QPushButton.secondary {{
        background-color: {c['secondary']};
        color: {c['text_primary']};
    }}
    
    QPushButton.secondary:hover {{
        background-color: {c['primary_light']};
    }}
    
    QPushButton.outline {{
        background-color: transparent;
        border: 2px solid {c['primary']};
        color: {c['primary']};
    }}
    
    QPushButton.outline:hover {{
        background-color: {c['primary']};
        color: white;
    }}
    
    /* 输入框样式 */
    QLineEdit, QTextEdit {{
        background-color: {c['surface']};
        border: 2px solid {c['border']};
        border-radius: 8px;
        padding: 10px;
        font-size: 14px;
        color: {c['text_primary']};
    }}
    
    QLineEdit:focus, QTextEdit:focus {{
        border-color: {c['primary']};
    }}
    
    /* 下拉框样式 */
    QComboBox {{
        background-color: {c['surface']};
        border: 2px solid {c['border']};
        border-radius: 8px;
        padding: 10px;
        font-size: 14px;
        color: {c['text_primary']};
        min-width: 120px;
    }}
    
    QComboBox:hover {{
        border-color: {c['primary']};
    }}
    
    QComboBox::drop-down {{
        border: none;
        padding-right: 10px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        selection-background-color: {c['secondary']};
    }}
    
    /* 滚动条样式 */
    QScrollArea {{
        border: none;
        background-color: transparent;
    }}
    
    QScrollBar:vertical {{
        background-color: {c['background']};
        width: 10px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {c['border']};
        border-radius: 5px;
        min-height: 30px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {c['primary_light']};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    /* 进度条样式 */
    QProgressBar {{
        background-color: {c['border']};
        border-radius: 10px;
        height: 20px;
        text-align: center;
    }}
    
    QProgressBar::chunk {{
        background-color: {c['primary']};
        border-radius: 10px;
    }}
    
    /* 标签页样式 */
    QTabWidget::pane {{
        border: 1px solid {c['border']};
        border-radius: 8px;
        background-color: {c['surface']};
    }}
    
    QTabBar::tab {{
        background-color: {c['background']};
        border: none;
        padding: 10px 20px;
        margin-right: 5px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {c['surface']};
        color: {c['primary']};
        font-weight: bold;
    }}
    
    QTabBar::tab:hover {{
        background-color: {c['secondary']};
    }}
    
    /* 列表样式 */
    QListWidget {{
        background-color: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        padding: 5px;
    }}
    
    QListWidget::item {{
        padding: 10px;
        border-radius: 8px;
        margin: 2px;
    }}
    
    QListWidget::item:selected {{
        background-color: {c['secondary']};
    }}
    
    QListWidget::item:hover {{
        background-color: {c['background']};
    }}
    
    /* 消息框样式 */
    QMessageBox {{
        background-color: {c['surface']};
    }}
    
    QMessageBox QPushButton {{
        min-width: 80px;
    }}
    
    /* 工具提示 */
    QToolTip {{
        background-color: {c['surface']};
        color: {c['text_primary']};
        border: 1px solid {c['border']};
        border-radius: 4px;
        padding: 5px;
    }}
    
    /* 分隔线 */
    QFrame[frameShape="4"] {{
        background-color: {c['border']};
        max-height: 1px;
    }}
    
    /* 复选框样式 */
    QCheckBox {{
        spacing: 10px;
    }}
    
    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border-radius: 4px;
        border: 2px solid {c['border']};
        background-color: {c['surface']};
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {c['primary']};
        border-color: {c['primary']};
    }}
    
    /* 滑块样式 */
    QSlider::groove:horizontal {{
        background-color: {c['border']};
        height: 8px;
        border-radius: 4px;
    }}
    
    QSlider::handle:horizontal {{
        background-color: {c['primary']};
        width: 20px;
        height: 20px;
        margin: -6px 0;
        border-radius: 10px;
    }}
    
    QSlider::sub-page:horizontal {{
        background-color: {c['primary']};
        border-radius: 4px;
    }}
    
    /* 自定义类 */
    .habit-card {{
        background-color: {c['surface']};
        border-radius: 16px;
        padding: 15px;
        border: 2px solid {c['border']};
    }}
    
    .habit-card:hover {{
        border-color: {c['primary_light']};
    }}
    
    .plant-widget {{
        background-color: {c['background']};
        border-radius: 20px;
        padding: 10px;
    }}
    
    .stats-card {{
        background-color: {c['surface']};
        border-radius: 12px;
        padding: 20px;
        border: 1px solid {c['border']};
    }}
    
    .achievement-badge {{
        background-color: {c['accent']};
        border-radius: 50%;
        padding: 10px;
    }}
    """


def get_splash_stylesheet():
    """获取启动页样式"""
    return """
    QWidget {
        background-color: #4CAF50;
    }
    
    QLabel {
        color: white;
        font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
    }
    
    #splash_icon {
        font-size: 72px;
    }
    
    #splash_title {
        font-size: 36px;
        font-weight: bold;
    }
    
    #splash_subtitle {
        font-size: 16px;
        opacity: 0.9;
    }
    """
