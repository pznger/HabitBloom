# HabitBloom 常量定义

# 习惯类别
CATEGORIES = {
    'health': {'name': '健康', 'icon': '💪', 'color': '#4CAF50'},
    'study': {'name': '学习', 'icon': '📚', 'color': '#2196F3'},
    'work': {'name': '工作', 'icon': '💼', 'color': '#FF9800'},
    'life': {'name': '生活', 'icon': '🏠', 'color': '#9C27B0'}
}

# 植物类型
PLANT_TYPES = {
    'flower': {'name': '花朵', 'icon': '🌸', 'stages': ['🌱', '🌿', '🌷', '🌸', '💐']},
    'tree': {'name': '树木', 'icon': '🌳', 'stages': ['🌱', '🌿', '🪴', '🌲', '🌳']},
    'cactus': {'name': '仙人掌', 'icon': '🌵', 'stages': ['🌱', '🌿', '🪴', '🌵', '🏜️']},
    'herb': {'name': '草药', 'icon': '🌿', 'stages': ['🌱', '☘️', '🌿', '🍀', '🌾']}
}

# 生长阶段
GROWTH_STAGES = {
    1: {'name': '种子', 'min_days': 0, 'growth_percent': 0},
    2: {'name': '发芽', 'min_days': 3, 'growth_percent': 20},
    3: {'name': '幼苗', 'min_days': 7, 'growth_percent': 40},
    4: {'name': '开花', 'min_days': 14, 'growth_percent': 70},
    5: {'name': '结果', 'min_days': 21, 'growth_percent': 100}
}

# 成就类型
ACHIEVEMENTS = {
    'streak_7': {'title': '初见坚持', 'desc': '连续打卡7天', 'icon': '🥉', 'days': 7},
    'streak_21': {'title': '习惯形成', 'desc': '连续打卡21天', 'icon': '🥈', 'days': 21},
    'streak_66': {'title': '习惯大师', 'desc': '连续打卡66天', 'icon': '🥇', 'days': 66},
    'streak_100': {'title': '传奇坚持者', 'desc': '连续打卡100天', 'icon': '🏆', 'days': 100},
    'perfect_week': {'title': '完美一周', 'desc': '一周内所有习惯全部完成', 'icon': '💎', 'days': 0},
    'habit_master': {'title': '习惯收藏家', 'desc': '同时养成5个习惯', 'icon': '🌟', 'days': 0},
    'early_bird': {'title': '早起鸟儿', 'desc': '连续7天在早上8点前完成习惯', 'icon': '🐦', 'days': 7}
}

# 主题颜色
THEMES = {
    'spring': {
        'name': '春日',
        'primary': '#4CAF50',
        'secondary': '#8BC34A',
        'background': '#F1F8E9',
        'accent': '#CDDC39'
    },
    'summer': {
        'name': '盛夏',
        'primary': '#FF9800',
        'secondary': '#FFC107',
        'background': '#FFF8E1',
        'accent': '#FFEB3B'
    },
    'autumn': {
        'name': '金秋',
        'primary': '#FF5722',
        'secondary': '#FF7043',
        'background': '#FBE9E7',
        'accent': '#FFAB91'
    },
    'winter': {
        'name': '冬雪',
        'primary': '#607D8B',
        'secondary': '#78909C',
        'background': '#ECEFF1',
        'accent': '#B0BEC5'
    }
}

# 难度等级
DIFFICULTY_LEVELS = {
    1: {'name': '轻松', 'color': '#4CAF50', 'growth_multiplier': 1.0},
    2: {'name': '简单', 'color': '#8BC34A', 'growth_multiplier': 1.2},
    3: {'name': '适中', 'color': '#FFC107', 'growth_multiplier': 1.5},
    4: {'name': '困难', 'color': '#FF9800', 'growth_multiplier': 1.8},
    5: {'name': '挑战', 'color': '#F44336', 'growth_multiplier': 2.0}
}

# 默认习惯模板
DEFAULT_HABITS = [
    {'name': '晨练', 'icon': '🏃', 'category': 'health', 'plant_type': 'tree', 'difficulty': 3},
    {'name': '阅读', 'icon': '📖', 'category': 'study', 'plant_type': 'flower', 'difficulty': 2},
    {'name': '喝水', 'icon': '💧', 'category': 'health', 'plant_type': 'herb', 'difficulty': 1},
    {'name': '冥想', 'icon': '🧘', 'category': 'health', 'plant_type': 'flower', 'difficulty': 2},
    {'name': '写日记', 'icon': '✍️', 'category': 'life', 'plant_type': 'flower', 'difficulty': 2}
]

# 应用设置
APP_NAME = "HabitBloom"
APP_VERSION = "1.0.0"
DATABASE_NAME = "habitbloom.db"
BACKUP_DIR = "backups"
