"""习惯管理器"""
from datetime import datetime, date, time
from typing import Optional, List, Dict, Any

from ..database.db_manager import DatabaseManager
from ..database.models import Habit, HabitRecord
from ..utils.constants import CATEGORIES, PLANT_TYPES, ACHIEVEMENTS


class HabitManager:
    """习惯管理器 - 处理习惯相关的业务逻辑"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def create_habit(self, name: str, category: str = 'life', icon: str = '🌱',
                     plant_type: str = 'flower', target_frequency: int = 7,
                     difficulty: int = 1, user_id: int = 1) -> Optional[int]:
        """创建新习惯"""
        if not name.strip():
            return None
        
        habit = Habit(
            user_id=user_id,
            name=name.strip(),
            category=category if category in CATEGORIES else 'life',
            icon=icon,
            plant_type=plant_type if plant_type in PLANT_TYPES else 'flower',
            target_frequency=max(1, min(7, target_frequency)),
            difficulty=max(1, min(5, difficulty))
        )
        
        return self.db.create_habit(habit)
    
    def get_habit(self, habit_id: int) -> Optional[Habit]:
        """获取习惯详情"""
        return self.db.get_habit(habit_id)
    
    def get_all_habits(self, user_id: int = 1, active_only: bool = True) -> List[Habit]:
        """获取所有习惯"""
        return self.db.get_all_habits(user_id, active_only)
    
    def get_habits_by_category(self, category: str, user_id: int = 1) -> List[Habit]:
        """按类别获取习惯"""
        habits = self.get_all_habits(user_id)
        return [h for h in habits if h.category == category]
    
    def update_habit(self, habit_id: int, **kwargs) -> bool:
        """更新习惯"""
        habit = self.db.get_habit(habit_id)
        if not habit:
            return False
        
        # 更新允许的字段
        allowed_fields = ['name', 'category', 'icon', 'plant_type', 
                          'target_frequency', 'difficulty', 'is_active']
        for field in allowed_fields:
            if field in kwargs:
                setattr(habit, field, kwargs[field])
        
        return self.db.update_habit(habit)
    
    def delete_habit(self, habit_id: int, hard_delete: bool = False) -> bool:
        """删除习惯"""
        if hard_delete:
            return self.db.hard_delete_habit(habit_id)
        return self.db.delete_habit(habit_id)
    
    def check_in(self, habit_id: int, notes: str = "", 
                 record_date: date = None) -> Dict[str, Any]:
        """
        习惯打卡
        返回打卡结果和可能解锁的成就
        """
        if record_date is None:
            record_date = date.today()
        
        habit = self.db.get_habit(habit_id)
        if not habit:
            return {'success': False, 'message': '习惯不存在'}
        
        # 检查是否已打卡
        existing = self.db.get_record(habit_id, record_date)
        if existing and existing.completed:
            return {
                'success': False, 
                'message': '今日已完成打卡',
                'already_completed': True
            }
        
        # 创建记录
        record = HabitRecord(
            habit_id=habit_id,
            record_date=record_date,
            completed=True,
            completed_time=datetime.now().time(),
            notes=notes,
            plant_growth_stage=habit.current_streak + 1
        )
        
        self.db.create_or_update_record(record)
        
        # 浇灌植物
        self.db.water_plant(habit_id)
        
        # 获取更新后的习惯数据
        updated_habit = self.db.get_habit(habit_id)
        
        # 检查成就
        unlocked_achievements = self._check_achievements(updated_habit)
        
        return {
            'success': True,
            'message': '打卡成功！',
            'habit': updated_habit,
            'current_streak': updated_habit.current_streak,
            'total_completed': updated_habit.total_completed,
            'unlocked_achievements': unlocked_achievements
        }
    
    def undo_check_in(self, habit_id: int, record_date: date = None) -> bool:
        """撤销打卡"""
        if record_date is None:
            record_date = date.today()
        
        record = self.db.get_record(habit_id, record_date)
        if not record:
            return False
        
        record.completed = False
        record.completed_time = None
        self.db.create_or_update_record(record)
        return True
    
    def get_today_status(self, user_id: int = 1) -> List[Dict]:
        """获取今日所有习惯状态"""
        return self.db.get_today_records(user_id)
    
    def get_habit_history(self, habit_id: int, days: int = 30) -> List[HabitRecord]:
        """获取习惯的历史记录"""
        end_date = date.today()
        start_date = date.today().replace(day=1) if days >= 28 else \
                     date.today() - timedelta(days=days)
        from datetime import timedelta
        start_date = date.today() - timedelta(days=days)
        return self.db.get_records_by_date_range(habit_id, start_date, end_date)
    
    def _check_achievements(self, habit: Habit) -> List[Dict]:
        """检查并解锁成就"""
        unlocked = []
        streak = habit.current_streak
        
        # 检查连续打卡成就
        streak_achievements = [
            ('streak_7', 7),
            ('streak_21', 21),
            ('streak_66', 66),
            ('streak_100', 100)
        ]
        
        for ach_type, days in streak_achievements:
            if streak >= days:
                if self.db.unlock_achievement(ach_type, habit.user_id):
                    ach_info = ACHIEVEMENTS.get(ach_type, {})
                    unlocked.append({
                        'type': ach_type,
                        'title': ach_info.get('title', ''),
                        'icon': ach_info.get('icon', '🏆')
                    })
        
        return unlocked
    
    def get_completion_stats(self, habit_id: int, year: int, month: int) -> Dict:
        """获取习惯完成统计"""
        calendar_data = self.db.get_habit_calendar_data(habit_id, year, month)
        habit = self.db.get_habit(habit_id)
        
        if not habit:
            return {}
        
        completed_count = sum(1 for v in calendar_data.values() if v)
        total_days = len(calendar_data)
        
        return {
            'habit': habit,
            'calendar': calendar_data,
            'completed_count': completed_count,
            'total_days': total_days,
            'completion_rate': round(completed_count / total_days * 100, 1) if total_days > 0 else 0,
            'current_streak': habit.current_streak,
            'longest_streak': habit.longest_streak
        }
