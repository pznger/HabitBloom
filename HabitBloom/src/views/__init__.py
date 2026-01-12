"""视图模块"""
from .main_window import MainWindow
from .garden_view import GardenView
from .habit_view import HabitView
from .stats_view import StatsView
from .settings_view import SettingsView
from .styles import get_main_stylesheet, get_splash_stylesheet, COLORS, DARK_COLORS

__all__ = [
    'MainWindow',
    'GardenView',
    'HabitView',
    'StatsView',
    'SettingsView',
    'get_main_stylesheet',
    'get_splash_stylesheet',
    'COLORS',
    'DARK_COLORS',
]
