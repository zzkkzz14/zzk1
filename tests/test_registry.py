"""测试 Skill 注册表"""

import pytest
from app.core.base import SkillRegistry
from app.models.skill import Skill, SkillType, SkillPriority, ProcessStep


class TestSkillRegistry:
    """SkillRegistry 测试类"""
    
    def setup_method(self):
        """每个测试方法前执行"""
        self.registry = SkillRegistry()
        self.test_skill = Skill(
            id="test_skill",
            name="测试 Skill",
            description="用于测试的 Skill",
            skill_type=SkillType.ROUTINE,
            priority=SkillPriority.MEDIUM,
            process_steps=[
                ProcessStep(name="步骤1", description="第一步", order=1)
            ],
            trigger_keywords=["测试", "test"],
            tags=["test"]
        )
    
    def test_register(self):
        """测试注册 Skill"""
        self.registry.register(self.test_skill)
        assert self.registry.get("test_skill") is not None
    
    def test_unregister(self):
        """测试注销 Skill"""
        self.registry.register(self.test_skill)
        result = self.registry.unregister("test_skill")
        assert result is True
        assert self.registry.get("test_skill") is None
    
    def test_unregister_nonexistent(self):
        """测试注销不存在的 Skill"""
        result = self.registry.unregister("nonexistent")
        assert result is False
    
    def test_list_all(self):
        """测试列出所有 Skill"""
        self.registry.register(self.test_skill)
        skills = self.registry.list_all()
        assert len(skills) == 1
        assert skills[0].id == "test_skill"
    
    def test_find_by_type(self):
        """测试按类型查找"""
        self.registry.register(self.test_skill)
        skills = self.registry.find_by_type(SkillType.ROUTINE)
        assert len(skills) == 1
        
        skills = self.registry.find_by_type(SkillType.CODING)
        assert len(skills) == 0
    
    def test_find_by_keyword(self):
        """测试按关键词查找"""
        self.registry.register(self.test_skill)
        
        skills = self.registry.find_by_keyword("测试")
        assert len(skills) == 1
        
        skills = self.registry.find_by_keyword("test")
        assert len(skills) == 1
        
        skills = self.registry.find_by_keyword("不存在的关键词")
        assert len(skills) == 0