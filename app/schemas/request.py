"""API 请求/响应模型"""

from typing import Optional, Any
from pydantic import BaseModel, Field


class SkillCreateRequest(BaseModel):
    """创建 Skill 请求"""
    id: str = Field(..., description="Skill ID")
    name: str = Field(..., description="Skill 名称")
    description: str = Field(..., description="Skill 描述")
    skill_type: str = Field(..., description="Skill 类型")
    priority: str = Field(default="medium", description="优先级")
    process_steps: list[dict] = Field(default_factory=list, description="过程步骤")
    output_constraints: Optional[dict] = Field(None, description="输出约束")
    guidelines: list[str] = Field(default_factory=list, description="行为指导")
    forbidden_actions: list[str] = Field(default_factory=list, description="禁止行为")
    trigger_keywords: list[str] = Field(default_factory=list, description="触发关键词")
    examples: list[dict] = Field(default_factory=list, description="示例")
    tags: list[str] = Field(default_factory=list, description="标签")


class ProcessRequest(BaseModel):
    """处理请求"""
    query: str = Field(..., description="用户查询")
    task_type: Optional[str] = Field(None, description="任务类型")
    context: dict = Field(default_factory=dict, description="额外上下文")


class ProcessResponse(BaseModel):
    """处理响应"""
    success: bool = Field(..., description="是否成功")
    output: str = Field(default="", description="约束提示输出")
    matched_skill: Optional[str] = Field(None, description="匹配的 Skill ID")
    skill_name: Optional[str] = Field(None, description="Skill 名称")
    steps_completed: list[str] = Field(default_factory=list, description="完成的步骤")
    errors: list[str] = Field(default_factory=list, description="错误信息")


class SkillResponse(BaseModel):
    """Skill 响应"""
    id: str
    name: str
    description: str
    skill_type: str
    priority: str
    process_steps: list[dict]
    guidelines: list[str]
    forbidden_actions: list[str]
    tags: list[str]


class SkillListResponse(BaseModel):
    """Skill 列表响应"""
    total: int = Field(..., description="总数")
    skills: list[SkillResponse] = Field(..., description="Skill 列表")