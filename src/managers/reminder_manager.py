"""提醒管理器"""
from datetime import datetime, time, timedelta
from typing import Optional, List, Dict, Any
import threading

from PyQt5.QtCore import QTimer, QObject, pyqtSignal

from ..database.db_manager import DatabaseManager
from ..database.models import Reminder


class ReminderManager(QObject):
    """提醒管理器 - 处理提醒相关的业务逻辑"""
    
    # 提醒触发信号
    reminder_triggered = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self._timers: Dict[int, QTimer] = {}
        self._check_timer = None
    
    def start_reminder_service(self):
        """启动提醒服务"""
        # 每分钟检查一次提醒
        self._check_timer = QTimer(self)
        self._check_timer.timeout.connect(self._check_reminders)
        self._check_timer.start(60000)  # 60秒
        
        # 立即检查一次
        self._check_reminders()
    
    def stop_reminder_service(self):
        """停止提醒服务"""
        if self._check_timer:
            self._check_timer.stop()
        
        for timer in self._timers.values():
            timer.stop()
        self._timers.clear()
    
    def _check_reminders(self):
        """检查并触发提醒"""
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        current_day = now.isoweekday()  # 1=周一, 7=周日
        
        # 获取所有活跃习惯
        habits = self.db.get_all_habits()
        
        for habit in habits:
            reminders = self.db.get_reminders(habit.habit_id)
            
            for reminder in reminders:
                if not reminder.is_active:
                    continue
                
                # 检查时间是否匹配
                if reminder.reminder_time == current_time:
                    # 检查星期是否匹配
                    active_days = reminder.get_active_days()
                    # 转换: 我们的系统 1=周日，需要转换
                    adjusted_day = current_day % 7 + 1
                    
                    if adjusted_day in active_days or current_day in active_days:
                        # 检查今天是否已完成
                        today_record = self.db.get_record(habit.habit_id, now.date())
                        if not today_record or not today_record.completed:
                            self._trigger_reminder(habit, reminder)
    
    def _trigger_reminder(self, habit, reminder):
        """触发提醒"""
        reminder_data = {
            'habit_id': habit.habit_id,
            'habit_name': habit.name,
            'habit_icon': habit.icon,
            'reminder_time': reminder.reminder_time,
            'message': f"该完成今天的「{habit.name}」了！"
        }
        
        self.reminder_triggered.emit(reminder_data)
    
    def create_reminder(self, habit_id: int, reminder_time: str,
                        days_of_week: str = "1,2,3,4,5,6,7") -> Optional[int]:
        """创建提醒"""
        # 验证时间格式
        try:
            datetime.strptime(reminder_time, '%H:%M')
        except ValueError:
            return None
        
        reminder = Reminder(
            habit_id=habit_id,
            reminder_time=reminder_time,
            days_of_week=days_of_week,
            is_active=True
        )
        
        return self.db.create_reminder(reminder)
    
    def get_reminders(self, habit_id: int) -> List[Reminder]:
        """获取习惯的所有提醒"""
        return self.db.get_reminders(habit_id)
    
    def update_reminder(self, reminder_id: int, **kwargs) -> bool:
        """更新提醒"""
        reminders = []
        habits = self.db.get_all_habits()
        for habit in habits:
            reminders.extend(self.db.get_reminders(habit.habit_id))
        
        reminder = next((r for r in reminders if r.reminder_id == reminder_id), None)
        if not reminder:
            return False
        
        if 'reminder_time' in kwargs:
            try:
                datetime.strptime(kwargs['reminder_time'], '%H:%M')
                reminder.reminder_time = kwargs['reminder_time']
            except ValueError:
                pass
        
        if 'days_of_week' in kwargs:
            reminder.days_of_week = kwargs['days_of_week']
        
        if 'is_active' in kwargs:
            reminder.is_active = kwargs['is_active']
        
        return self.db.update_reminder(reminder)
    
    def delete_reminder(self, reminder_id: int) -> bool:
        """删除提醒"""
        return self.db.delete_reminder(reminder_id)
    
    def toggle_reminder(self, reminder_id: int) -> bool:
        """切换提醒状态"""
        reminders = []
        habits = self.db.get_all_habits()
        for habit in habits:
            reminders.extend(self.db.get_reminders(habit.habit_id))
        
        reminder = next((r for r in reminders if r.reminder_id == reminder_id), None)
        if not reminder:
            return False
        
        reminder.is_active = not reminder.is_active
        return self.db.update_reminder(reminder)
    
    def get_next_reminder(self, habit_id: int) -> Optional[Dict]:
        """获取下一个提醒时间"""
        reminders = self.db.get_reminders(habit_id)
        active_reminders = [r for r in reminders if r.is_active]
        
        if not active_reminders:
            return None
        
        now = datetime.now()
        current_time = now.time()
        
        for reminder in sorted(active_reminders, key=lambda r: r.reminder_time):
            reminder_time = datetime.strptime(reminder.reminder_time, '%H:%M').time()
            if reminder_time > current_time:
                return {
                    'time': reminder.reminder_time,
                    'is_today': True
                }
        
        # 如果今天没有更多提醒，返回明天的第一个
        first_reminder = min(active_reminders, key=lambda r: r.reminder_time)
        return {
            'time': first_reminder.reminder_time,
            'is_today': False
        }
    
    def get_all_scheduled_reminders(self) -> List[Dict]:
        """获取所有已安排的提醒"""
        habits = self.db.get_all_habits()
        all_reminders = []
        
        for habit in habits:
            reminders = self.db.get_reminders(habit.habit_id)
            for reminder in reminders:
                all_reminders.append({
                    'reminder_id': reminder.reminder_id,
                    'habit_id': habit.habit_id,
                    'habit_name': habit.name,
                    'habit_icon': habit.icon,
                    'time': reminder.reminder_time,
                    'days': reminder.days_of_week,
                    'is_active': reminder.is_active
                })
        
        return sorted(all_reminders, key=lambda r: r['time'])
