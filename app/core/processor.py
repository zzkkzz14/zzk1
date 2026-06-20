"""Skill 处理器 - 负责协调 AI 回答过程"""

from typing import Optional
from ..models.skill import Skill, SkillType, SkillPriority, ProcessStep
from ..core.base import registry


class ProcessResult:
    """处理结果"""
    
    def __init__(self, success: bool, output: str = "", steps_completed: list = None, 
                 errors: list = None, metadata: dict = None):
        self.success = success
        self.output = output
        self.steps_completed = steps_completed or []
        self.errors = errors or []
        self.metadata = metadata or {}
    
    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "output": self.output,
            "steps_completed": self.steps_completed,
            "errors": self.errors,
            "metadata": self.metadata
        }


class SkillProcessor:
    """Skill 处理器 - 约束 AI 回答过程"""
    
    def __init__(self):
        self.registry = registry
    
    def find_matching_skill(self, context: dict) -> Optional[Skill]:
        """根据上下文找到匹配的 Skill"""
        query = context.get("query", "").lower()
        task_type = context.get("task_type")
        
        # 1. 优先按类型匹配
        if task_type:
            skills = self.registry.find_by_type(task_type)
            if skills:
                return self._select_highest_priority(skills)
        
        # 2. 按关键词匹配
        skills = self.registry.find_by_keyword(query)
        if skills:
            return self._select_highest_priority(skills)
        
        # 3. 返回默认 Skill
        return self._get_default_skill()
    
    def _select_highest_priority(self, skills: list[Skill]) -> Skill:
        """选择优先级最高的 Skill"""
        priority_order = {
            SkillPriority.CRITICAL: 4,
            SkillPriority.HIGH: 3,
            SkillPriority.MEDIUM: 2,
            SkillPriority.LOW: 1
        }
        return max(skills, key=lambda s: priority_order.get(s.priority, 0))
    
    def _get_default_skill(self) -> Skill:
        """获取默认 Skill"""
        return Skill(
            id="default",
            name="默认处理",
            description="默认的回答处理方式",
            skill_type=SkillType.ROUTINE,
            priority=SkillPriority.LOW,
            process_steps=[
                ProcessStep(name="理解问题", description="分析用户意图", order=1),
                ProcessStep(name="组织回答", description="构建清晰简洁的回答", order=2),
                ProcessStep(name="输出结果", description="直接给出答案", order=3)
            ],
            guidelines=[
                "回答简洁直接",
                "避免冗余信息",
                "优先给出结论"
            ],
            forbidden_actions=[
                "不要过度解释",
                "不要重复问题"
            ]
        )
    
    def validate_process(self, skill: Skill, context: dict) -> list[str]:
        """验证过程是否符合约束"""
        errors = []
        
        # 检查必填步骤
        required_steps = [s for s in skill.process_steps if s.required]
        completed_steps = context.get("completed_steps", [])
        
        for step in required_steps:
            if step.name not in completed_steps:
                errors.append(f"缺少必要步骤: {step.name}")
        
        # 检查输出约束
        output = context.get("output", "")
        constraints = skill.output_constraints
        
        if constraints:
            if constraints.max_length and len(output) > constraints.max_length:
                errors.append(f"输出超出最大长度限制: {constraints.max_length}")
            
            if constraints.min_length and len(output) < constraints.min_length:
                errors.append(f"输出未达最小长度要求: {constraints.min_length}")
            
            for must_include in constraints.must_include:
                if must_include not in output:
                    errors.append(f"输出缺少必要内容: {must_include}")
            
            for must_exclude in constraints.must_exclude:
                if must_exclude in output:
                    errors.append(f"输出包含禁止内容: {must_exclude}")
        
        return errors
    
    def generate_prompt(self, skill: Skill, context: dict) -> str:
        """生成约束性提示词"""
        prompt_parts = []
        
        # 基本信息
        prompt_parts.append(f"## 任务类型: {skill.skill_type}")
        prompt_parts.append(f"## 优先级: {skill.priority}")
        
        # 过程约束
        if skill.process_steps:
            prompt_parts.append("\n## 回答过程要求:")
            sorted_steps = sorted(skill.process_steps, key=lambda s: s.order)
            for step in sorted_steps:
                required_mark = "[必须]" if step.required else "[可选]"
                prompt_parts.append(f"{required_mark} {step.order}. {step.name}: {step.description}")
        
        # 行为指导
        if skill.guidelines:
            prompt_parts.append("\n## 行为指导:")
            for guideline in skill.guidelines:
                prompt_parts.append(f"- {guideline}")
        
        # 禁止行为
        if skill.forbidden_actions:
            prompt_parts.append("\n## 禁止行为:")
            for forbidden in skill.forbidden_actions:
                prompt_parts.append(f"- {forbidden}")
        
        # 输出约束
        if skill.output_constraints:
            prompt_parts.append("\n## 输出要求:")
            if skill.output_constraints.format_hint:
                prompt_parts.append(f"格式: {skill.output_constraints.format_hint}")
            if skill.output_constraints.max_length:
                prompt_parts.append(f"最大长度: {skill.output_constraints.max_length} 字符")
        
        return "\n".join(prompt_parts)
    
    def process(self, context: dict) -> ProcessResult:
        """处理请求"""
        skill = self.find_matching_skill(context)
        
        if not skill:
            return ProcessResult(
                success=False,
                errors=["无法找到匹配的 Skill"]
            )
        
        # 生成约束提示
        constraint_prompt = self.generate_prompt(skill, context)
        
        return ProcessResult(
            success=True,
            output=constraint_prompt,
            metadata={
                "matched_skill": skill.id,
                "skill_name": skill.name,
                "skill_type": skill.skill_type
            }
        )