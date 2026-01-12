"""花园管理器"""
from datetime import date, timedelta
from typing import Optional, List, Dict, Any

from ..database.db_manager import DatabaseManager
from ..database.models import GardenState, Habit
from ..utils.constants import PLANT_TYPES, GROWTH_STAGES


class GardenManager:
    """花园管理器 - 处理花园和植物相关的业务逻辑"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_garden_overview(self, user_id: int = 1) -> Dict[str, Any]:
        """获取花园概览"""
        habits = self.db.get_all_habits(user_id)
        garden_states = self.db.get_all_garden_states(user_id)
        
        # 创建习惯ID到花园状态的映射
        state_map = {s.habit_id: s for s in garden_states}
        
        plants = []
        for habit in habits:
            state = state_map.get(habit.habit_id)
            plant_info = self._get_plant_info(habit, state)
            plants.append(plant_info)
        
        # 统计信息
        total_plants = len(plants)
        healthy_plants = sum(1 for p in plants if p['health'] >= 50)
        blooming_plants = sum(1 for p in plants if p['stage'] >= 4)
        
        return {
            'plants': plants,
            'total_plants': total_plants,
            'healthy_plants': healthy_plants,
            'blooming_plants': blooming_plants,
            'garden_health': round(healthy_plants / total_plants * 100) if total_plants > 0 else 0
        }
    
    def _get_plant_info(self, habit: Habit, state: Optional[GardenState]) -> Dict[str, Any]:
        """获取植物信息"""
        plant_type_info = PLANT_TYPES.get(habit.plant_type, PLANT_TYPES['flower'])
        
        if state:
            stage = state.stage
            health = state.plant_health
            growth = state.plant_growth
            last_watered = state.last_watered
        else:
            stage = 1
            health = 100
            growth = 0
            last_watered = None
        
        # 获取当前阶段的图标
        stages = plant_type_info['stages']
        stage_index = min(stage - 1, len(stages) - 1)
        current_icon = stages[stage_index]
        
        # 获取阶段名称
        stage_info = GROWTH_STAGES.get(stage, GROWTH_STAGES[1])
        
        # 检查是否需要浇水
        needs_water = self._check_needs_water(last_watered)
        
        return {
            'habit_id': habit.habit_id,
            'name': habit.name,
            'icon': habit.icon,
            'plant_icon': current_icon,
            'plant_type': habit.plant_type,
            'stage': stage,
            'stage_name': stage_info['name'],
            'health': health,
            'growth': growth,
            'needs_water': needs_water,
            'last_watered': last_watered,
            'current_streak': habit.current_streak,
            'category': habit.category,
            'is_completed_today': False  # 将在视图层设置
        }
    
    def _check_needs_water(self, last_watered: Optional[date]) -> bool:
        """检查是否需要浇水"""
        if last_watered is None:
            return True
        
        today = date.today()
        days_since_water = (today - last_watered).days
        return days_since_water >= 1
    
    def get_plant_detail(self, habit_id: int) -> Optional[Dict[str, Any]]:
        """获取植物详细信息"""
        habit = self.db.get_habit(habit_id)
        if not habit:
            return None
        
        state = self.db.get_garden_state(habit_id)
        plant_info = self._get_plant_info(habit, state)
        
        # 添加额外的详细信息
        plant_type_info = PLANT_TYPES.get(habit.plant_type, PLANT_TYPES['flower'])
        
        plant_info.update({
            'total_completed': habit.total_completed,
            'longest_streak': habit.longest_streak,
            'created_at': habit.created_at,
            'all_stages': plant_type_info['stages'],
            'next_stage_progress': self._calculate_next_stage_progress(state)
        })
        
        return plant_info
    
    def _calculate_next_stage_progress(self, state: Optional[GardenState]) -> int:
        """计算到下一阶段的进度"""
        if not state or state.stage >= 5:
            return 100
        
        current_stage = state.stage
        next_stage = current_stage + 1
        
        current_min = GROWTH_STAGES[current_stage]['growth_percent']
        next_min = GROWTH_STAGES[next_stage]['growth_percent']
        
        if state.plant_growth >= next_min:
            return 100
        
        progress_range = next_min - current_min
        current_progress = state.plant_growth - current_min
        
        return int(current_progress / progress_range * 100) if progress_range > 0 else 0
    
    def water_plant(self, habit_id: int) -> Dict[str, Any]:
        """浇灌植物"""
        success = self.db.water_plant(habit_id)
        
        if not success:
            return {'success': False, 'message': '浇灌失败'}
        
        # 获取更新后的状态
        state = self.db.get_garden_state(habit_id)
        habit = self.db.get_habit(habit_id)
        plant_info = self._get_plant_info(habit, state)
        
        return {
            'success': True,
            'message': '浇灌成功！植物更健康了',
            'plant': plant_info
        }
    
    def update_all_plants_health(self, user_id: int = 1):
        """更新所有植物的健康状态（每日调用）"""
        states = self.db.get_all_garden_states(user_id)
        today = date.today()
        
        for state in states:
            if state.last_watered:
                days_since_water = (today - state.last_watered).days
                
                if days_since_water > 0:
                    # 每天未浇水减少健康值
                    health_decrease = min(days_since_water * 5, 50)
                    state.plant_health = max(0, state.plant_health - health_decrease)
                    self.db.update_garden_state(state)
    
    def get_garden_by_category(self, category: str, user_id: int = 1) -> List[Dict]:
        """按类别获取花园植物"""
        overview = self.get_garden_overview(user_id)
        return [p for p in overview['plants'] if p['category'] == category]
    
    def get_wilting_plants(self, user_id: int = 1) -> List[Dict]:
        """获取需要关注的植物（健康值低或需要浇水）"""
        overview = self.get_garden_overview(user_id)
        return [p for p in overview['plants'] if p['health'] < 50 or p['needs_water']]
