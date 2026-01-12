"""数据库管理器"""
import sqlite3
import os
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

from .models import User, Habit, HabitRecord, Reminder, Achievement, GardenState
from ..utils.helpers import get_database_path


class DatabaseManager:
    """SQLite数据库管理器"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.db_path = get_database_path()
        self._init_database()
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _init_database(self):
        """初始化数据库表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 创建用户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    avatar_color TEXT DEFAULT '#4CAF50',
                    daily_goal_time TEXT DEFAULT '08:00',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_login DATETIME
                )
            ''')
            
            # 创建习惯表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS habits (
                    habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT CHECK(category IN ('health', 'study', 'work', 'life')),
                    icon TEXT DEFAULT '🌱',
                    plant_type TEXT CHECK(plant_type IN ('flower', 'tree', 'cactus', 'herb')),
                    target_frequency INTEGER DEFAULT 7,
                    current_streak INTEGER DEFAULT 0,
                    longest_streak INTEGER DEFAULT 0,
                    total_completed INTEGER DEFAULT 0,
                    difficulty INTEGER CHECK(difficulty BETWEEN 1 AND 5),
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            ''')
            
            # 创建习惯记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS habit_records (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    record_date DATE NOT NULL,
                    completed BOOLEAN DEFAULT 0,
                    completed_time TIME,
                    notes TEXT,
                    plant_growth_stage INTEGER DEFAULT 0,
                    UNIQUE(habit_id, record_date),
                    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
                )
            ''')
            
            # 创建提醒表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reminders (
                    reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    reminder_time TIME NOT NULL,
                    days_of_week TEXT DEFAULT '1,2,3,4,5,6,7',
                    is_active BOOLEAN DEFAULT 1,
                    notification_id TEXT,
                    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
                )
            ''')
            
            # 创建成就表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS achievements (
                    achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    achievement_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    badge_icon TEXT NOT NULL,
                    unlocked_at DATETIME,
                    requirement_value INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            ''')
            
            # 创建花园状态表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS garden_states (
                    state_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    habit_id INTEGER NOT NULL,
                    plant_growth INTEGER DEFAULT 0,
                    plant_health INTEGER DEFAULT 100,
                    last_watered DATE,
                    stage INTEGER DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
                )
            ''')
            
            # 创建默认用户
            cursor.execute('SELECT COUNT(*) FROM users')
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    'INSERT INTO users (username, avatar_color) VALUES (?, ?)',
                    ('我的花园', '#4CAF50')
                )
    
    # ========== 用户操作 ==========
    
    def get_user(self, user_id: int = 1) -> Optional[User]:
        """获取用户信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if row:
                return User.from_dict(dict(row))
        return None
    
    def update_user(self, user: User) -> bool:
        """更新用户信息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET 
                    username = ?, avatar_color = ?, daily_goal_time = ?, last_login = ?
                WHERE user_id = ?
            ''', (user.username, user.avatar_color, user.daily_goal_time, 
                  datetime.now(), user.user_id))
            return cursor.rowcount > 0
    
    # ========== 习惯操作 ==========
    
    def create_habit(self, habit: Habit) -> int:
        """创建习惯"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO habits 
                (user_id, name, category, icon, plant_type, target_frequency, difficulty)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (habit.user_id, habit.name, habit.category, habit.icon,
                  habit.plant_type, habit.target_frequency, habit.difficulty))
            habit_id = cursor.lastrowid
            
            # 创建对应的花园状态
            cursor.execute('''
                INSERT INTO garden_states (user_id, habit_id, plant_growth, plant_health, stage)
                VALUES (?, ?, 0, 100, 1)
            ''', (habit.user_id, habit_id))
            
            return habit_id
    
    def get_habit(self, habit_id: int) -> Optional[Habit]:
        """获取单个习惯"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM habits WHERE habit_id = ?', (habit_id,))
            row = cursor.fetchone()
            if row:
                return Habit.from_dict(dict(row))
        return None
    
    def get_all_habits(self, user_id: int = 1, active_only: bool = True) -> List[Habit]:
        """获取所有习惯"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if active_only:
                cursor.execute(
                    'SELECT * FROM habits WHERE user_id = ? AND is_active = 1 ORDER BY created_at DESC',
                    (user_id,)
                )
            else:
                cursor.execute(
                    'SELECT * FROM habits WHERE user_id = ? ORDER BY created_at DESC',
                    (user_id,)
                )
            return [Habit.from_dict(dict(row)) for row in cursor.fetchall()]
    
    def update_habit(self, habit: Habit) -> bool:
        """更新习惯"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE habits SET 
                    name = ?, category = ?, icon = ?, plant_type = ?,
                    target_frequency = ?, current_streak = ?, longest_streak = ?,
                    total_completed = ?, difficulty = ?, is_active = ?
                WHERE habit_id = ?
            ''', (habit.name, habit.category, habit.icon, habit.plant_type,
                  habit.target_frequency, habit.current_streak, habit.longest_streak,
                  habit.total_completed, habit.difficulty, habit.is_active, habit.habit_id))
            return cursor.rowcount > 0
    
    def delete_habit(self, habit_id: int) -> bool:
        """删除习惯（软删除）"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE habits SET is_active = 0 WHERE habit_id = ?', (habit_id,))
            return cursor.rowcount > 0
    
    def hard_delete_habit(self, habit_id: int) -> bool:
        """彻底删除习惯"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM habits WHERE habit_id = ?', (habit_id,))
            return cursor.rowcount > 0
    
    # ========== 习惯记录操作 ==========
    
    def create_or_update_record(self, record: HabitRecord) -> int:
        """创建或更新习惯记录"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO habit_records (habit_id, record_date, completed, completed_time, notes, plant_growth_stage)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(habit_id, record_date) DO UPDATE SET
                    completed = excluded.completed,
                    completed_time = excluded.completed_time,
                    notes = excluded.notes,
                    plant_growth_stage = excluded.plant_growth_stage
            ''', (record.habit_id, record.record_date, record.completed,
                  str(record.completed_time) if record.completed_time else None,
                  record.notes, record.plant_growth_stage))
            
            # 更新习惯统计
            if record.completed:
                self._update_habit_stats(cursor, record.habit_id)
            
            return cursor.lastrowid
    
    def _update_habit_stats(self, cursor, habit_id: int):
        """更新习惯统计数据"""
        # 获取所有完成的记录
        cursor.execute('''
            SELECT record_date FROM habit_records 
            WHERE habit_id = ? AND completed = 1 
            ORDER BY record_date DESC
        ''', (habit_id,))
        records = cursor.fetchall()
        
        if not records:
            return
        
        # 计算连续天数
        streak = 0
        today = date.today()
        current_date = today
        
        for row in records:
            record_date = date.fromisoformat(row[0]) if isinstance(row[0], str) else row[0]
            if record_date == current_date or record_date == current_date - timedelta(days=1):
                streak += 1
                current_date = record_date - timedelta(days=1)
            else:
                break
        
        # 更新习惯表
        cursor.execute('''
            UPDATE habits SET 
                current_streak = ?,
                longest_streak = MAX(longest_streak, ?),
                total_completed = (SELECT COUNT(*) FROM habit_records WHERE habit_id = ? AND completed = 1)
            WHERE habit_id = ?
        ''', (streak, streak, habit_id, habit_id))
    
    def get_record(self, habit_id: int, record_date: date) -> Optional[HabitRecord]:
        """获取指定日期的记录"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM habit_records WHERE habit_id = ? AND record_date = ?',
                (habit_id, record_date)
            )
            row = cursor.fetchone()
            if row:
                return HabitRecord.from_dict(dict(row))
        return None
    
    def get_records_by_date_range(self, habit_id: int, start_date: date, end_date: date) -> List[HabitRecord]:
        """获取日期范围内的记录"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM habit_records 
                WHERE habit_id = ? AND record_date BETWEEN ? AND ?
                ORDER BY record_date
            ''', (habit_id, start_date, end_date))
            return [HabitRecord.from_dict(dict(row)) for row in cursor.fetchall()]
    
    def get_today_records(self, user_id: int = 1) -> List[Dict]:
        """获取今日所有习惯的打卡情况"""
        today = date.today()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT h.*, r.completed, r.completed_time, r.notes, g.stage, g.plant_health
                FROM habits h
                LEFT JOIN habit_records r ON h.habit_id = r.habit_id AND r.record_date = ?
                LEFT JOIN garden_states g ON h.habit_id = g.habit_id
                WHERE h.user_id = ? AND h.is_active = 1
                ORDER BY h.created_at
            ''', (today, user_id))
            
            results = []
            for row in cursor.fetchall():
                data = dict(row)
                data['completed_today'] = bool(data.get('completed'))
                results.append(data)
            return results
    
    # ========== 提醒操作 ==========
    
    def create_reminder(self, reminder: Reminder) -> int:
        """创建提醒"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reminders (habit_id, reminder_time, days_of_week, is_active)
                VALUES (?, ?, ?, ?)
            ''', (reminder.habit_id, reminder.reminder_time, 
                  reminder.days_of_week, reminder.is_active))
            return cursor.lastrowid
    
    def get_reminders(self, habit_id: int) -> List[Reminder]:
        """获取习惯的所有提醒"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM reminders WHERE habit_id = ?',
                (habit_id,)
            )
            return [Reminder.from_dict(dict(row)) for row in cursor.fetchall()]
    
    def update_reminder(self, reminder: Reminder) -> bool:
        """更新提醒"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE reminders SET 
                    reminder_time = ?, days_of_week = ?, is_active = ?
                WHERE reminder_id = ?
            ''', (reminder.reminder_time, reminder.days_of_week,
                  reminder.is_active, reminder.reminder_id))
            return cursor.rowcount > 0
    
    def delete_reminder(self, reminder_id: int) -> bool:
        """删除提醒"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM reminders WHERE reminder_id = ?', (reminder_id,))
            return cursor.rowcount > 0
    
    # ========== 成就操作 ==========
    
    def create_achievement(self, achievement: Achievement) -> int:
        """创建成就"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO achievements 
                (user_id, achievement_type, title, description, badge_icon, unlocked_at, requirement_value)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (achievement.user_id, achievement.achievement_type, achievement.title,
                  achievement.description, achievement.badge_icon, achievement.unlocked_at,
                  achievement.requirement_value))
            return cursor.lastrowid
    
    def get_achievements(self, user_id: int = 1, unlocked_only: bool = False) -> List[Achievement]:
        """获取用户成就"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if unlocked_only:
                cursor.execute(
                    'SELECT * FROM achievements WHERE user_id = ? AND unlocked_at IS NOT NULL ORDER BY unlocked_at DESC',
                    (user_id,)
                )
            else:
                cursor.execute(
                    'SELECT * FROM achievements WHERE user_id = ? ORDER BY unlocked_at DESC NULLS LAST',
                    (user_id,)
                )
            return [Achievement.from_dict(dict(row)) for row in cursor.fetchall()]
    
    def unlock_achievement(self, achievement_type: str, user_id: int = 1) -> bool:
        """解锁成就"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE achievements SET unlocked_at = ?
                WHERE achievement_type = ? AND user_id = ? AND unlocked_at IS NULL
            ''', (datetime.now(), achievement_type, user_id))
            return cursor.rowcount > 0
    
    # ========== 花园状态操作 ==========
    
    def get_garden_state(self, habit_id: int) -> Optional[GardenState]:
        """获取花园状态"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM garden_states WHERE habit_id = ?', (habit_id,))
            row = cursor.fetchone()
            if row:
                return GardenState.from_dict(dict(row))
        return None
    
    def get_all_garden_states(self, user_id: int = 1) -> List[GardenState]:
        """获取用户所有花园状态"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT g.* FROM garden_states g
                JOIN habits h ON g.habit_id = h.habit_id
                WHERE g.user_id = ? AND h.is_active = 1
            ''', (user_id,))
            return [GardenState.from_dict(dict(row)) for row in cursor.fetchall()]
    
    def update_garden_state(self, state: GardenState) -> bool:
        """更新花园状态"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE garden_states SET 
                    plant_growth = ?, plant_health = ?, last_watered = ?, stage = ?
                WHERE state_id = ?
            ''', (state.plant_growth, state.plant_health, state.last_watered, 
                  state.stage, state.state_id))
            return cursor.rowcount > 0
    
    def water_plant(self, habit_id: int) -> bool:
        """浇灌植物"""
        today = date.today()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 获取当前状态
            cursor.execute('SELECT * FROM garden_states WHERE habit_id = ?', (habit_id,))
            row = cursor.fetchone()
            if not row:
                return False
            
            state = dict(row)
            
            # 增加生长值和健康值
            new_growth = min(100, state['plant_growth'] + 5)
            new_health = min(100, state['plant_health'] + 10)
            
            # 计算新的生长阶段
            new_stage = state['stage']
            if new_growth >= 80 and state['stage'] < 5:
                new_stage = 5
            elif new_growth >= 60 and state['stage'] < 4:
                new_stage = 4
            elif new_growth >= 40 and state['stage'] < 3:
                new_stage = 3
            elif new_growth >= 20 and state['stage'] < 2:
                new_stage = 2
            
            cursor.execute('''
                UPDATE garden_states SET 
                    plant_growth = ?, plant_health = ?, last_watered = ?, stage = ?
                WHERE habit_id = ?
            ''', (new_growth, new_health, today, new_stage, habit_id))
            
            return cursor.rowcount > 0
    
    # ========== 统计数据 ==========
    
    def get_monthly_stats(self, user_id: int, year: int, month: int) -> Dict[str, Any]:
        """获取月度统计"""
        from calendar import monthrange
        start_date = date(year, month, 1)
        end_date = date(year, month, monthrange(year, month)[1])
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 获取该月总完成数
            cursor.execute('''
                SELECT COUNT(*) FROM habit_records r
                JOIN habits h ON r.habit_id = h.habit_id
                WHERE h.user_id = ? AND r.record_date BETWEEN ? AND ? AND r.completed = 1
            ''', (user_id, start_date, end_date))
            total_completed = cursor.fetchone()[0]
            
            # 获取习惯数量
            cursor.execute('''
                SELECT COUNT(*) FROM habits WHERE user_id = ? AND is_active = 1
            ''', (user_id,))
            habit_count = cursor.fetchone()[0]
            
            # 计算应完成数
            days_in_month = monthrange(year, month)[1]
            expected_completions = habit_count * days_in_month
            
            # 完成率
            completion_rate = (total_completed / expected_completions * 100) if expected_completions > 0 else 0
            
            # 获取最长连续天数
            cursor.execute('''
                SELECT MAX(longest_streak) FROM habits WHERE user_id = ?
            ''', (user_id,))
            longest_streak = cursor.fetchone()[0] or 0
            
            # 当前最长连续天数
            cursor.execute('''
                SELECT MAX(current_streak) FROM habits WHERE user_id = ?
            ''', (user_id,))
            current_streak = cursor.fetchone()[0] or 0
            
            return {
                'total_completed': total_completed,
                'expected_completions': expected_completions,
                'completion_rate': round(completion_rate, 1),
                'habit_count': habit_count,
                'longest_streak': longest_streak,
                'current_streak': current_streak,
                'year': year,
                'month': month
            }
    
    def get_habit_calendar_data(self, habit_id: int, year: int, month: int) -> Dict[int, bool]:
        """获取习惯的日历数据"""
        from calendar import monthrange
        start_date = date(year, month, 1)
        end_date = date(year, month, monthrange(year, month)[1])
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT record_date, completed FROM habit_records
                WHERE habit_id = ? AND record_date BETWEEN ? AND ?
            ''', (habit_id, start_date, end_date))
            
            result = {}
            for row in cursor.fetchall():
                record_date = date.fromisoformat(row[0]) if isinstance(row[0], str) else row[0]
                result[record_date.day] = bool(row[1])
            return result
    
    # ========== 数据备份与恢复 ==========
    
    def export_all_data(self) -> Dict[str, Any]:
        """导出所有数据"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            data = {
                'export_time': str(datetime.now()),
                'version': '1.0',
                'users': [],
                'habits': [],
                'records': [],
                'reminders': [],
                'achievements': [],
                'garden_states': []
            }
            
            for table, key in [('users', 'users'), ('habits', 'habits'), 
                               ('habit_records', 'records'), ('reminders', 'reminders'),
                               ('achievements', 'achievements'), ('garden_states', 'garden_states')]:
                cursor.execute(f'SELECT * FROM {table}')
                data[key] = [dict(row) for row in cursor.fetchall()]
            
            return data
    
    def import_all_data(self, data: Dict[str, Any]) -> bool:
        """导入所有数据"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 清空现有数据
                for table in ['garden_states', 'achievements', 'reminders', 
                              'habit_records', 'habits', 'users']:
                    cursor.execute(f'DELETE FROM {table}')
                
                # 导入用户
                for user in data.get('users', []):
                    cursor.execute('''
                        INSERT INTO users (user_id, username, avatar_color, daily_goal_time, created_at, last_login)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (user['user_id'], user['username'], user['avatar_color'],
                          user['daily_goal_time'], user['created_at'], user['last_login']))
                
                # 导入习惯
                for habit in data.get('habits', []):
                    cursor.execute('''
                        INSERT INTO habits (habit_id, user_id, name, category, icon, plant_type,
                            target_frequency, current_streak, longest_streak, total_completed,
                            difficulty, is_active, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (habit['habit_id'], habit['user_id'], habit['name'], habit['category'],
                          habit['icon'], habit['plant_type'], habit['target_frequency'],
                          habit['current_streak'], habit['longest_streak'], habit['total_completed'],
                          habit['difficulty'], habit['is_active'], habit['created_at']))
                
                # 导入记录
                for record in data.get('records', []):
                    cursor.execute('''
                        INSERT INTO habit_records (record_id, habit_id, record_date, completed,
                            completed_time, notes, plant_growth_stage)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (record['record_id'], record['habit_id'], record['record_date'],
                          record['completed'], record['completed_time'], record['notes'],
                          record['plant_growth_stage']))
                
                # 导入提醒
                for reminder in data.get('reminders', []):
                    cursor.execute('''
                        INSERT INTO reminders (reminder_id, habit_id, reminder_time, days_of_week,
                            is_active, notification_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (reminder['reminder_id'], reminder['habit_id'], reminder['reminder_time'],
                          reminder['days_of_week'], reminder['is_active'], reminder['notification_id']))
                
                # 导入成就
                for ach in data.get('achievements', []):
                    cursor.execute('''
                        INSERT INTO achievements (achievement_id, user_id, achievement_type, title,
                            description, badge_icon, unlocked_at, requirement_value)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (ach['achievement_id'], ach['user_id'], ach['achievement_type'],
                          ach['title'], ach['description'], ach['badge_icon'],
                          ach['unlocked_at'], ach['requirement_value']))
                
                # 导入花园状态
                for state in data.get('garden_states', []):
                    cursor.execute('''
                        INSERT INTO garden_states (state_id, user_id, habit_id, plant_growth,
                            plant_health, last_watered, stage)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (state['state_id'], state['user_id'], state['habit_id'],
                          state['plant_growth'], state['plant_health'], state['last_watered'],
                          state['stage']))
                
                return True
        except Exception as e:
            print(f"导入数据失败: {e}")
            return False
