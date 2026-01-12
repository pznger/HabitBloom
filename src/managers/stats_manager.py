"""统计管理器"""
from datetime import date, datetime, timedelta
from typing import List, Dict, Any
from calendar import monthrange

from ..database.db_manager import DatabaseManager
from ..database.models import Achievement
from ..utils.constants import ACHIEVEMENTS


class StatsManager:
    """统计管理器 - 处理统计和成就相关的业务逻辑"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_overview_stats(self, user_id: int = 1) -> Dict[str, Any]:
        """获取总体统计概览"""
        habits = self.db.get_all_habits(user_id)
        today = date.today()
        
        # 基本统计
        total_habits = len(habits)
        total_completed = sum(h.total_completed for h in habits)
        current_max_streak = max((h.current_streak for h in habits), default=0)
        longest_ever_streak = max((h.longest_streak for h in habits), default=0)
        
        # 今日完成情况
        today_records = self.db.get_today_records(user_id)
        completed_today = sum(1 for r in today_records if r.get('completed_today'))
        
        # 本月统计
        monthly = self.db.get_monthly_stats(user_id, today.year, today.month)
        
        # 成就统计
        achievements = self.db.get_achievements(user_id, unlocked_only=True)
        
        return {
            'total_habits': total_habits,
            'total_completed': total_completed,
            'current_max_streak': current_max_streak,
            'longest_ever_streak': longest_ever_streak,
            'completed_today': completed_today,
            'habits_today': len(today_records),
            'monthly_completion_rate': monthly['completion_rate'],
            'achievements_count': len(achievements)
        }
    
    def get_weekly_stats(self, user_id: int = 1, weeks_ago: int = 0) -> Dict[str, Any]:
        """获取周统计"""
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday() + weeks_ago * 7)
        end_of_week = start_of_week + timedelta(days=6)
        
        habits = self.db.get_all_habits(user_id)
        
        daily_data = []
        for i in range(7):
            day = start_of_week + timedelta(days=i)
            day_completed = 0
            day_total = len(habits)
            
            for habit in habits:
                record = self.db.get_record(habit.habit_id, day)
                if record and record.completed:
                    day_completed += 1
            
            daily_data.append({
                'date': day,
                'day_name': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][i],
                'completed': day_completed,
                'total': day_total,
                'rate': round(day_completed / day_total * 100) if day_total > 0 else 0
            })
        
        total_completed = sum(d['completed'] for d in daily_data)
        total_possible = sum(d['total'] for d in daily_data)
        
        return {
            'start_date': start_of_week,
            'end_date': end_of_week,
            'daily_data': daily_data,
            'total_completed': total_completed,
            'total_possible': total_possible,
            'weekly_rate': round(total_completed / total_possible * 100) if total_possible > 0 else 0
        }
    
    def get_monthly_stats(self, user_id: int = 1, year: int = None, 
                          month: int = None) -> Dict[str, Any]:
        """获取月度统计"""
        if year is None:
            year = date.today().year
        if month is None:
            month = date.today().month
        
        basic_stats = self.db.get_monthly_stats(user_id, year, month)
        
        # 获取每日详细数据
        days_in_month = monthrange(year, month)[1]
        habits = self.db.get_all_habits(user_id)
        
        daily_data = []
        for day in range(1, days_in_month + 1):
            current_date = date(year, month, day)
            if current_date > date.today():
                break
            
            day_completed = 0
            for habit in habits:
                record = self.db.get_record(habit.habit_id, current_date)
                if record and record.completed:
                    day_completed += 1
            
            daily_data.append({
                'day': day,
                'date': current_date,
                'completed': day_completed,
                'total': len(habits),
                'rate': round(day_completed / len(habits) * 100) if habits else 0
            })
        
        # 计算趋势
        if len(daily_data) >= 7:
            first_week_avg = sum(d['rate'] for d in daily_data[:7]) / 7
            last_week_avg = sum(d['rate'] for d in daily_data[-7:]) / 7
            trend = 'up' if last_week_avg > first_week_avg else ('down' if last_week_avg < first_week_avg else 'stable')
        else:
            trend = 'stable'
        
        basic_stats.update({
            'daily_data': daily_data,
            'trend': trend
        })
        
        return basic_stats
    
    def get_habit_ranking(self, user_id: int = 1) -> List[Dict]:
        """获取习惯排行榜（按连续天数）"""
        habits = self.db.get_all_habits(user_id)
        
        ranking = []
        for habit in habits:
            ranking.append({
                'habit_id': habit.habit_id,
                'name': habit.name,
                'icon': habit.icon,
                'current_streak': habit.current_streak,
                'longest_streak': habit.longest_streak,
                'total_completed': habit.total_completed
            })
        
        # 按当前连续天数排序
        ranking.sort(key=lambda x: x['current_streak'], reverse=True)
        
        # 添加排名
        for i, item in enumerate(ranking):
            item['rank'] = i + 1
        
        return ranking
    
    def get_achievements(self, user_id: int = 1) -> Dict[str, List[Achievement]]:
        """获取成就列表（已解锁和未解锁）"""
        all_achievements = self.db.get_achievements(user_id)
        unlocked_types = {a.achievement_type for a in all_achievements if a.is_unlocked}
        
        # 创建所有可能的成就
        all_possible = []
        for ach_type, info in ACHIEVEMENTS.items():
            existing = next((a for a in all_achievements if a.achievement_type == ach_type), None)
            
            if existing:
                all_possible.append(existing)
            else:
                all_possible.append(Achievement(
                    user_id=user_id,
                    achievement_type=ach_type,
                    title=info['title'],
                    description=info['desc'],
                    badge_icon=info['icon'],
                    requirement_value=info.get('days', 0)
                ))
        
        unlocked = [a for a in all_possible if a.is_unlocked]
        locked = [a for a in all_possible if not a.is_unlocked]
        
        return {
            'unlocked': unlocked,
            'locked': locked,
            'total': len(all_possible),
            'unlocked_count': len(unlocked)
        }
    
    def get_category_stats(self, user_id: int = 1) -> Dict[str, Dict]:
        """按类别获取统计"""
        from ..utils.constants import CATEGORIES
        
        habits = self.db.get_all_habits(user_id)
        
        stats = {}
        for cat_key, cat_info in CATEGORIES.items():
            cat_habits = [h for h in habits if h.category == cat_key]
            
            if cat_habits:
                total_completed = sum(h.total_completed for h in cat_habits)
                avg_streak = sum(h.current_streak for h in cat_habits) / len(cat_habits)
            else:
                total_completed = 0
                avg_streak = 0
            
            stats[cat_key] = {
                'name': cat_info['name'],
                'icon': cat_info['icon'],
                'color': cat_info['color'],
                'habit_count': len(cat_habits),
                'total_completed': total_completed,
                'avg_streak': round(avg_streak, 1)
            }
        
        return stats
    
    def check_and_unlock_achievements(self, user_id: int = 1) -> List[Achievement]:
        """检查并解锁所有符合条件的成就"""
        habits = self.db.get_all_habits(user_id)
        unlocked = []
        
        # 检查连续打卡成就
        max_streak = max((h.current_streak for h in habits), default=0)
        
        streak_achievements = [
            ('streak_7', 7),
            ('streak_21', 21),
            ('streak_66', 66),
            ('streak_100', 100)
        ]
        
        for ach_type, required_days in streak_achievements:
            if max_streak >= required_days:
                if self.db.unlock_achievement(ach_type, user_id):
                    ach_info = ACHIEVEMENTS[ach_type]
                    unlocked.append(Achievement(
                        achievement_type=ach_type,
                        title=ach_info['title'],
                        badge_icon=ach_info['icon'],
                        unlocked_at=datetime.now()
                    ))
        
        # 检查习惯收藏家成就
        if len(habits) >= 5:
            if self.db.unlock_achievement('habit_master', user_id):
                ach_info = ACHIEVEMENTS['habit_master']
                unlocked.append(Achievement(
                    achievement_type='habit_master',
                    title=ach_info['title'],
                    badge_icon=ach_info['icon'],
                    unlocked_at=datetime.now()
                ))
        
        return unlocked
    
    def get_streak_calendar(self, habit_id: int, year: int, month: int) -> Dict[int, str]:
        """获取打卡日历数据"""
        calendar_data = self.db.get_habit_calendar_data(habit_id, year, month)
        
        # 转换为状态映射
        result = {}
        for day, completed in calendar_data.items():
            if completed:
                result[day] = 'completed'
            else:
                result[day] = 'missed'
        
        return result
