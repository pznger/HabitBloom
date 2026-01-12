#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HabitBloom - 让习惯如花般绽放
个人习惯养成应用
"""
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor

from src.views.main_window import MainWindow
from src.views.styles import get_splash_stylesheet


class SplashScreen(QSplashScreen):
    """启动画面 - 手机尺寸"""
    
    def __init__(self):
        # 手机尺寸的启动画面
        pixmap = QPixmap(390, 844)
        pixmap.fill(QColor("#4CAF50"))
        
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
    def drawContents(self, painter: QPainter):
        """绘制启动画面内容"""
        painter.setPen(QColor("white"))
        
        # 绘制图标（居中靠上）
        painter.setFont(QFont("Segoe UI Emoji", 72))
        painter.drawText(self.rect().adjusted(0, 280, 0, 0), 
                        Qt.AlignHCenter | Qt.AlignTop, "🌱")
        
        # 绘制标题
        painter.setFont(QFont("Microsoft YaHei", 32, QFont.Bold))
        painter.drawText(self.rect().adjusted(0, 400, 0, 0),
                        Qt.AlignHCenter | Qt.AlignTop, "HabitBloom")
        
        # 绘制副标题
        painter.setFont(QFont("Microsoft YaHei", 16))
        painter.drawText(self.rect().adjusted(0, 460, 0, 0),
                        Qt.AlignHCenter | Qt.AlignTop, "让习惯如花般绽放")
        
        # 绘制加载提示
        painter.setFont(QFont("Microsoft YaHei", 12))
        painter.drawText(self.rect().adjusted(0, 0, 0, -50),
                        Qt.AlignHCenter | Qt.AlignBottom, "正在加载...")


def main():
    """主函数"""
    # 设置高DPI支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("HabitBloom")
    app.setOrganizationName("HabitBloom")
    
    # 设置默认字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    # 显示启动画面
    splash = SplashScreen()
    splash.show()
    app.processEvents()
    
    # 创建主窗口
    window = MainWindow()
    
    # 延迟关闭启动画面并显示主窗口
    def show_main():
        splash.close()
        window.show()
    
    QTimer.singleShot(1500, show_main)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
