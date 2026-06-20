"""测试 Skill 处理器"""

import pytest
from app.core.processor import SkillProcessor, ProcessResult
from app.core.base import registry
from app.models.skill import Skill, SkillType, SkillPriority, ProcessStep


class TestSkillProcessor:
    """SkillProcessor 测试类"""
    
    def setup_method(self):
        """每个测试方法前执行"""
        self.processor = SkillProcessor()
    
    def test_find_matching_skill_by_keyword(self):
        """测试通过关键词匹配 Skill"""
        context = {
            "query": "帮我写一个登录功能的代码"
        }
        skill = self.processor.find_matching_skill(context)
        assert skill is not None
        assert skill.id == "coding"
    
    def test_find_matching_skill_by_type(self):
        """测试通过类型匹配 Skill"""
        context = {
            "query": "分析一下这个数据",
            "task_type": SkillType.ANALYSIS
        }
        skill = self.processor.find_matching_skill(context)
        assert skill is not None
    
    def test_get_default_skill(self):
        """测试获取默认 Skill"""
        context = {
            "query": "随便说点什么"
        }
        skill = self.processor.find_matching_skill(context)
        assert skill is not None
        assert skill.id == "default"
    
    def test_generate_prompt(self):
        """测试生成约束提示"""
        skill = registry.get("coding")
        context = {"query": "写一个函数"}
        prompt = self.processor.generate_prompt(skill, context)
        
        assert "编码任务" in prompt
        assert "理解需求" in prompt
        assert "编写代码" in prompt
    
    def test_validate_process_success(self):
        """测试验证过程成功"""
        skill = registry.get("coding")
        context = {
            "completed_steps": ["理解需求", "设计方案", "编写代码", "验证结果"],
            "output": "```python\nprint('hello')\n```"
        }
        errors = self.processor.validate_process(skill, context)
        assert len(errors) == 0
    
    def test_validate_process_missing_step(self):
        """测试验证过程缺少步骤"""
        skill = registry.get("coding")
        context = {
            "completed_steps": ["理解需求"],
            "output": "```python\nprint('hello')\n```"
        }
        errors = self.processor.validate_process(skill, context)
        assert len(errors) > 0
        assert any("缺少必要步骤" in e for e in errors)
    
    def test_process(self):
        """测试处理请求"""
        context = {
            "query": "帮我写代码实现排序"
        }
        result = self.processor.process(context)
        
        assert result.success is True
        assert result.output != ""
        assert result.metadata.get("matched_skill") == "coding"


class TestProcessResult:
    """ProcessResult 测试类"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        result = ProcessResult(
            success=True,
            output="test output",
            steps_completed=["step1", "step2"],
            errors=[],
            metadata={"key": "value"}
        )
        
        result_dict = result.to_dict()
        assert result_dict["success"] is True
        assert result_dict["output"] == "test output"
        assert len(result_dict["steps_completed"]) == 2