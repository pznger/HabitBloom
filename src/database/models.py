"""数据模型定义"""
from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import Optional, List


@dataclass
class User:
    """用户模型"""
    user_id: Optional[int] = None
    username: str = "用户"
    avatar_color: str = "#4CAF50"
    daily_goal_time: str = "08:00"
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'avatar_color': self.avatar_color,
            'daily_goal_time': self.daily_goal_time,
            'created_at': str(self.created_at) if self.created_at else None,
            'last_login': str(self.last_login) if self.last_login else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username', '用户'),
            avatar_color=data.get('avatar_color', '#4CAF50'),
            daily_goal_time=data.get('daily_goal_time', '08:00'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            last_login=datetime.fromisoformat(data['last_login']) if data.get('last_login') else None
        )


@dataclass
class Habit:
    """习惯模型"""
    habit_id: Optional[int] = None
    user_id: int = 1
    name: str = ""
    category: str = "life"  # health, study, work, life
    icon: str = "🌱"
    plant_type: str = "flower"  # flower, tree, cactus, herb
    target_frequency: int = 7  # 每周目标次数
    current_streak: int = 0
    longest_streak: int = 0
    total_completed: int = 0
    difficulty: int = 1  # 1-5
    is_active: bool = True
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            'habit_id': self.habit_id,
            'user_id': self.user_id,
            'name': self.name,
            'category': self.category,
            'icon': self.icon,
            'plant_type': self.plant_type,
            'target_frequency': self.target_frequency,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'total_completed': self.total_completed,
            'difficulty': self.difficulty,
            'is_active': self.is_active,
            'created_at': str(self.created_at) if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Habit':
        return cls(
            habit_id=data.get('habit_id'),
            user_id=data.get('user_id', 1),
            name=data.get('name', ''),
            category=data.get('category', 'life'),
            icon=data.get('icon', '🌱'),
            plant_type=data.get('plant_type', 'flower'),
            target_frequency=data.get('target_frequency', 7),
            current_streak=data.get('current_streak', 0),
            longest_streak=data.get('longest_streak', 0),
            total_completed=data.get('total_completed', 0),
            difficulty=data.get('difficulty', 1),
            is_active=data.get('is_active', True),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )


@dataclass
class HabitRecord:
    """习惯记录模型"""
    record_id: Optional[int] = None
    habit_id: int = 0
    record_date: Optional[date] = None
    completed: bool = False
    completed_time: Optional[time] = None
    notes: str = ""
    plant_growth_stage: int = 0
    
    def to_dict(self) -> dict:
        return {
            'record_id': self.record_id,
            'habit_id': self.habit_id,
            'record_date': str(self.record_date) if self.record_date else None,
            'completed': self.completed,
            'completed_time': str(self.completed_time) if self.completed_time else None,
            'notes': self.notes,
            'plant_growth_stage': self.plant_growth_stage
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'HabitRecord':
        record_date = None
        if data.get('record_date'):
            if isinstance(data['record_date'], str):
                record_date = date.fromisoformat(data['record_date'])
            else:
                record_date = data['record_date']
        
        return cls(
            record_id=data.get('record_id'),
            habit_id=data.get('habit_id', 0),
            record_date=record_date,
            completed=data.get('completed', False),
            completed_time=time.fromisoformat(data['completed_time']) if data.get('completed_time') else None,
            notes=data.get('notes', ''),
            plant_growth_stage=data.get('plant_growth_stage', 0)
        )


@dataclass
class Reminder:
    """提醒模型"""
    reminder_id: Optional[int] = None
    habit_id: int = 0
    reminder_time: str = "08:00"
    days_of_week: str = "1,2,3,4,5,6,7"  # 1=周日
    is_active: bool = True
    notification_id: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            'reminder_id': self.reminder_id,
            'habit_id': self.habit_id,
            'reminder_time': self.reminder_time,
            'days_of_week': self.days_of_week,
            'is_active': self.is_active,
            'notification_id': self.notification_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Reminder':
        return cls(
            reminder_id=data.get('reminder_id'),
            habit_id=data.get('habit_id', 0),
            reminder_time=data.get('reminder_time', '08:00'),
            days_of_week=data.get('days_of_week', '1,2,3,4,5,6,7'),
            is_active=data.get('is_active', True),
            notification_id=data.get('notification_id')
        )
    
    def get_active_days(self) -> List[int]:
        """获取活跃的星期列表"""
        return [int(d) for d in self.days_of_week.split(',') if d.strip()]


@dataclass
class Achievement:
    """成就模型"""
    achievement_id: Optional[int] = None
    user_id: int = 1
    achievement_type: str = ""
    title: str = ""
    description: str = ""
    badge_icon: str = "🏆"
    unlocked_at: Optional[datetime] = None
    requirement_value: int = 0
    
    def to_dict(self) -> dict:
        return {
            'achievement_id': self.achievement_id,
            'user_id': self.user_id,
            'achievement_type': self.achievement_type,
            'title': self.title,
            'description': self.description,
            'badge_icon': self.badge_icon,
            'unlocked_at': str(self.unlocked_at) if self.unlocked_at else None,
            'requirement_value': self.requirement_value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Achievement':
        return cls(
            achievement_id=data.get('achievement_id'),
            user_id=data.get('user_id', 1),
            achievement_type=data.get('achievement_type', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            badge_icon=data.get('badge_icon', '🏆'),
            unlocked_at=datetime.fromisoformat(data['unlocked_at']) if data.get('unlocked_at') else None,
            requirement_value=data.get('requirement_value', 0)
        )
    
    @property
    def is_unlocked(self) -> bool:
        return self.unlocked_at is not None


@dataclass
class GardenState:
    """花园状态模型"""
    state_id: Optional[int] = None
    user_id: int = 1
    habit_id: int = 0
    plant_growth: int = 0  # 0-100
    plant_health: int = 100  # 0-100
    last_watered: Optional[date] = None
    stage: int = 1  # 1=种子,2=发芽,3=幼苗,4=开花,5=结果
    
    def to_dict(self) -> dict:
        return {
            'state_id': self.state_id,
            'user_id': self.user_id,
            'habit_id': self.habit_id,
            'plant_growth': self.plant_growth,
            'plant_health': self.plant_health,
            'last_watered': str(self.last_watered) if self.last_watered else None,
            'stage': self.stage
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GardenState':
        last_watered = None
        if data.get('last_watered'):
            if isinstance(data['last_watered'], str):
                last_watered = date.fromisoformat(data['last_watered'])
            else:
                last_watered = data['last_watered']
        
        return cls(
            state_id=data.get('state_id'),
            user_id=data.get('user_id', 1),
            habit_id=data.get('habit_id', 0),
            plant_growth=data.get('plant_growth', 0),
            plant_health=data.get('plant_health', 100),
            last_watered=last_watered,
            stage=data.get('stage', 1)
        )
    
    def get_health_status(self) -> str:
        """获取健康状态描述"""
        if self.plant_health >= 80:
            return "茂盛"
        elif self.plant_health >= 50:
            return "健康"
        elif self.plant_health >= 20:
            return "需要浇灌"
        else:
            return "缺水"
