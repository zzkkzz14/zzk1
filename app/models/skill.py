"""Skill 模型定义 - 约束 AI 回答行为的核心数据结构"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ProcessStep(BaseModel):
    """回答过程中的步骤定义"""
    name: str = Field(..., description="步骤名称")
    description: str = Field(..., description="步骤描述")
    required: bool = Field(default=True, description="是否必须执行")
    order: int = Field(..., description="执行顺序")


class OutputConstraint(BaseModel):
    """输出约束定义"""
    max_length: Optional[int] = Field(None, description="最大输出长度")
    min_length: Optional[int] = Field(None, description="最小输出长度")
    format_hint: Optional[str] = Field(None, description="格式提示")
    must_include: list[str] = Field(default_factory=list, description="必须包含的内容")
    must_exclude: list[str] = Field(default_factory=list, description="必须排除的内容")


class SkillPriority(str, Enum):
    """Skill 优先级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SkillType(str, Enum):
    """Skill 类型"""
    RESEARCH = "research"       # 研究类：需要深入分析
    CODING = "coding"           # 编码类：需要写代码
    ANALYSIS = "analysis"       # 分析类：需要推理
    CREATIVE = "creative"       # 创意类：需要发散思维
    ROUTINE = "routine"         # 常规类：简单任务
    IMAGE_GENERATION = "image_generation"  # 图像生成类：需要生成图片


class Skill(BaseModel):
    """Skill 定义 - 约束 AI 的回答思路"""
    
    id: str = Field(..., description="Skill 唯一标识")
    name: str = Field(..., description="Skill 名称")
    description: str = Field(..., description="Skill 描述")
    
    # 类型与优先级
    skill_type: SkillType = Field(..., description="Skill 类型")
    priority: SkillPriority = Field(default=SkillPriority.MEDIUM, description="优先级")
    
    # 过程约束
    process_steps: list[ProcessStep] = Field(
        default_factory=list, 
        description="回答过程步骤"
    )
    
    # 输出约束
    output_constraints: Optional[OutputConstraint] = Field(
        None, 
        description="输出约束"
    )
    
    # 行为指导
    guidelines: list[str] = Field(
        default_factory=list,
        description="行为指导原则"
    )
    
    # 禁止行为
    forbidden_actions: list[str] = Field(
        default_factory=list,
        description="禁止的行为"
    )
    
    # 触发条件
    trigger_keywords: list[str] = Field(
        default_factory=list,
        description="触发关键词"
    )
    
    # 示例
    examples: list[dict] = Field(
        default_factory=list,
        description="示例输入输出"
    )
    
    # 元数据
    version: str = Field(default="1.0.0", description="版本号")
    author: Optional[str] = Field(None, description="作者")
    tags: list[str] = Field(default_factory=list, description="标签")
    
    class Config:
        use_enum_values = True