"""工具函数"""
import os
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any


def get_app_data_dir() -> str:
    """获取应用数据目录"""
    if os.name == 'nt':  # Windows
        base_dir = os.environ.get('APPDATA', os.path.expanduser('~'))
    else:  # Linux/Mac
        base_dir = os.path.expanduser('~/.local/share')
    
    app_dir = os.path.join(base_dir, 'HabitBloom')
    os.makedirs(app_dir, exist_ok=True)
    return app_dir


def get_database_path() -> str:
    """获取数据库文件路径"""
    return os.path.join(get_app_data_dir(), 'habitbloom.db')


def get_backup_dir() -> str:
    """获取备份目录"""
    backup_dir = os.path.join(get_app_data_dir(), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def get_week_dates(date: datetime = None) -> List[datetime]:
    """获取某日期所在周的所有日期"""
    if date is None:
        date = datetime.now()
    
    start_of_week = date - timedelta(days=date.weekday())
    return [start_of_week + timedelta(days=i) for i in range(7)]


def get_month_dates(year: int, month: int) -> List[datetime]:
    """获取某月的所有日期"""
    from calendar import monthrange
    num_days = monthrange(year, month)[1]
    return [datetime(year, month, day) for day in range(1, num_days + 1)]


def calculate_streak(records: List[Dict], habit_id: int) -> int:
    """计算连续打卡天数"""
    if not records:
        return 0
    
    today = datetime.now().date()
    streak = 0
    current_date = today
    
    # 按日期排序记录
    sorted_records = sorted(
        [r for r in records if r.get('completed')],
        key=lambda x: x.get('record_date', ''),
        reverse=True
    )
    
    for record in sorted_records:
        record_date = datetime.strptime(record['record_date'], '%Y-%m-%d').date()
        
        if record_date == current_date or record_date == current_date - timedelta(days=1):
            streak += 1
            current_date = record_date - timedelta(days=1)
        else:
            break
    
    return streak


def calculate_growth_stage(streak_days: int, difficulty: int = 1) -> int:
    """根据连续天数计算植物生长阶段"""
    from .constants import GROWTH_STAGES, DIFFICULTY_LEVELS
    
    multiplier = DIFFICULTY_LEVELS.get(difficulty, {}).get('growth_multiplier', 1.0)
    adjusted_days = int(streak_days * multiplier)
    
    stage = 1
    for s, info in sorted(GROWTH_STAGES.items(), reverse=True):
        if adjusted_days >= info['min_days']:
            stage = s
            break
    
    return stage


def calculate_completion_rate(records: List[Dict], target_frequency: int = 7) -> float:
    """计算完成率"""
    if not records:
        return 0.0
    
    completed_count = sum(1 for r in records if r.get('completed'))
    expected_count = len(records) * (target_frequency / 7)
    
    if expected_count == 0:
        return 0.0
    
    return min(100.0, (completed_count / expected_count) * 100)


def format_time_ago(dt: datetime) -> str:
    """格式化为相对时间"""
    now = datetime.now()
    diff = now - dt
    
    if diff.days > 365:
        return f"{diff.days // 365}年前"
    elif diff.days > 30:
        return f"{diff.days // 30}个月前"
    elif diff.days > 0:
        return f"{diff.days}天前"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600}小时前"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60}分钟前"
    else:
        return "刚刚"


def export_data_to_json(data: Dict[str, Any], filepath: str) -> bool:
    """导出数据为JSON文件"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        return True
    except Exception as e:
        print(f"导出数据失败: {e}")
        return False


def import_data_from_json(filepath: str) -> Optional[Dict[str, Any]]:
    """从JSON文件导入数据"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"导入数据失败: {e}")
        return None


def get_greeting() -> str:
    """根据时间获取问候语"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "早上好"
    elif 12 <= hour < 14:
        return "中午好"
    elif 14 <= hour < 18:
        return "下午好"
    elif 18 <= hour < 22:
        return "晚上好"
    else:
        return "夜深了"
