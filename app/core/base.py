"""Skill 基类和核心接口"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from ..models.skill import Skill, SkillType, SkillPriority


class SkillExecutor(ABC):
    """Skill 执行器基类"""
    
    @abstractmethod
    def can_handle(self, context: dict) -> bool:
        """判断是否能处理该上下文"""
        pass
    
    @abstractmethod
    def execute(self, context: dict) -> dict:
        """执行 Skill"""
        pass
    
    @abstractmethod
    def validate_result(self, result: dict) -> bool:
        """验证执行结果"""
        pass


class SkillRegistry:
    """Skill 注册表"""
    
    def __init__(self):
        self._skills: dict[str, Skill] = {}
        self._executors: dict[str, SkillExecutor] = {}
    
    def register(self, skill: Skill, executor: Optional[SkillExecutor] = None) -> None:
        """注册 Skill"""
        self._skills[skill.id] = skill
        if executor:
            self._executors[skill.id] = executor
    
    def unregister(self, skill_id: str) -> bool:
        """注销 Skill"""
        if skill_id in self._skills:
            del self._skills[skill_id]
            self._executors.pop(skill_id, None)
            return True
        return False
    
    def get(self, skill_id: str) -> Optional[Skill]:
        """获取 Skill"""
        return self._skills.get(skill_id)
    
    def get_executor(self, skill_id: str) -> Optional[SkillExecutor]:
        """获取执行器"""
        return self._executors.get(skill_id)
    
    def list_all(self) -> list[Skill]:
        """列出所有 Skill"""
        return list(self._skills.values())
    
    def find_by_type(self, skill_type: SkillType) -> list[Skill]:
        """按类型查找"""
        return [s for s in self._skills.values() if s.skill_type == skill_type]
    
    def find_by_keyword(self, keyword: str) -> list[Skill]:
        """按关键词查找"""
        keyword_lower = keyword.lower()
        results = []
        for skill in self._skills.values():
            # 检查触发关键词
            if any(keyword_lower in kw.lower() for kw in skill.trigger_keywords):
                results.append(skill)
            # 检查标签
            elif any(keyword_lower in tag.lower() for tag in skill.tags):
                results.append(skill)
        return results


# 全局注册表实例
registry = SkillRegistry()