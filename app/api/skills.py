"""Skill API 路由"""

from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel, Field

from ..models.skill import Skill, SkillType, SkillPriority, ProcessStep, OutputConstraint
from ..core.base import registry
from ..core.processor import SkillProcessor
from ..schemas.request import (
    SkillCreateRequest, 
    ProcessRequest, 
    ProcessResponse,
    SkillResponse,
    SkillListResponse
)
from ..services.agnes_image import agnes_service

router = APIRouter(prefix="/skills", tags=["skills"])
processor = SkillProcessor()


class ImageGenerateRequest(BaseModel):
    """图像生成请求"""
    prompt: str = Field(..., description="提示词")
    size: str = Field(default="1024x1024", description="图像尺寸")
    n: int = Field(default=1, description="生成数量")
    negative_prompt: Optional[str] = Field(None, description="负面提示词")


class ImageGenerateFromImageRequest(BaseModel):
    """图生图请求"""
    image: str = Field(..., description="输入图像（URL 或 base64 编码）")
    prompt: str = Field(..., description="提示词")
    size: str = Field(default="1024x1024", description="图像尺寸")
    n: int = Field(default=1, description="生成数量")
    strength: float = Field(default=0.7, description="变换强度")
    negative_prompt: Optional[str] = Field(None, description="负面提示词")


@router.post("/", response_model=SkillResponse)
async def create_skill(request: SkillCreateRequest):
    """创建新的 Skill"""
    if registry.get(request.id):
        raise HTTPException(status_code=400, detail="Skill ID 已存在")
    
    # 转换 process_steps
    process_steps = [
        ProcessStep(
            name=s.get("name", ""),
            description=s.get("description", ""),
            required=s.get("required", True),
            order=s.get("order", i)
        )
        for i, s in enumerate(request.process_steps)
    ]
    
    # 转换 output_constraints
    output_constraints = None
    if request.output_constraints:
        output_constraints = OutputConstraint(**request.output_constraints)
    
    skill = Skill(
        id=request.id,
        name=request.name,
        description=request.description,
        skill_type=SkillType(request.skill_type),
        priority=SkillPriority(request.priority),
        process_steps=process_steps,
        output_constraints=output_constraints,
        guidelines=request.guidelines,
        forbidden_actions=request.forbidden_actions,
        trigger_keywords=request.trigger_keywords,
        examples=request.examples,
        tags=request.tags
    )
    
    registry.register(skill)
    
    return SkillResponse(
        id=skill.id,
        name=skill.name,
        description=skill.description,
        skill_type=skill.skill_type,
        priority=skill.priority,
        process_steps=[s.model_dump() for s in skill.process_steps],
        guidelines=skill.guidelines,
        forbidden_actions=skill.forbidden_actions,
        tags=skill.tags
    )


@router.get("/", response_model=SkillListResponse)
async def list_skills(
    skill_type: Optional[str] = None,
    keyword: Optional[str] = None
):
    """列出所有 Skill"""
    if skill_type:
        skills = registry.find_by_type(SkillType(skill_type))
    elif keyword:
        skills = registry.find_by_keyword(keyword)
    else:
        skills = registry.list_all()
    
    return SkillListResponse(
        total=len(skills),
        skills=[
            SkillResponse(
                id=s.id,
                name=s.name,
                description=s.description,
                skill_type=s.skill_type,
                priority=s.priority,
                process_steps=[step.model_dump() for step in s.process_steps],
                guidelines=s.guidelines,
                forbidden_actions=s.forbidden_actions,
                tags=s.tags
            )
            for s in skills
        ]
    )


@router.get("/debug")
async def debug_skills():
    """调试：查看所有 Skill 的触发关键词"""
    skills = registry.list_all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "trigger_keywords": s.trigger_keywords,
            "tags": s.tags
        }
        for s in skills
    ]


@router.get("/debug/match/{query}")
async def debug_match(query: str):
    """调试：测试关键词匹配"""
    skills = registry.find_by_keyword(query)
    return {
        "query": query,
        "matched_count": len(skills),
        "matched_skills": [{"id": s.id, "name": s.name} for s in skills]
    }


@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(skill_id: str):
    """获取指定 Skill"""
    skill = registry.get(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")
    
    return SkillResponse(
        id=skill.id,
        name=skill.name,
        description=skill.description,
        skill_type=skill.skill_type,
        priority=skill.priority,
        process_steps=[s.model_dump() for s in skill.process_steps],
        guidelines=skill.guidelines,
        forbidden_actions=skill.forbidden_actions,
        tags=skill.tags
    )


@router.delete("/{skill_id}")
async def delete_skill(skill_id: str):
    """删除 Skill"""
    if not registry.unregister(skill_id):
        raise HTTPException(status_code=404, detail="Skill 不存在")
    return {"message": "删除成功"}


@router.post("/process", response_model=ProcessResponse)
async def process_query(request: ProcessRequest):
    """处理查询 - 返回约束提示"""
    context = {
        "query": request.query,
        "task_type": request.task_type,
        **request.context
    }
    
    result = processor.process(context)
    
    return ProcessResponse(
        success=result.success,
        output=result.output,
        matched_skill=result.metadata.get("matched_skill"),
        skill_name=result.metadata.get("skill_name"),
        steps_completed=result.steps_completed,
        errors=result.errors
    )


@router.post("/{skill_id}/validate")
async def validate_process(skill_id: str, context: dict):
    """验证过程是否符合约束"""
    skill = registry.get(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")
    
    errors = processor.validate_process(skill, context)
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


@router.post("/image/generate")
async def generate_image(request: ImageGenerateRequest):
    """
    使用 Agnes Image 2.1 Flash 生成图像
    
    需要配置 AGNES_API_KEY 环境变量
    """
    if not agnes_service.api_key:
        raise HTTPException(status_code=400, detail="请配置 AGNES_API_KEY 环境变量")
    
    try:
        result = agnes_service.generate_image(
            prompt=request.prompt,
            size=request.size,
            n=request.n,
            negative_prompt=request.negative_prompt
        )
        return {
            "success": True,
            "model": "agnes-image-2.1-flash",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image/generate-from-image")
async def generate_image_from_image(request: ImageGenerateFromImageRequest):
    """
    使用 Agnes Image 2.1 Flash 进行图生图
    
    需要配置 AGNES_API_KEY 环境变量
    """
    if not agnes_service.api_key:
        raise HTTPException(status_code=400, detail="请配置 AGNES_API_KEY 环境变量")
    
    try:
        result = agnes_service.generate_image_from_image(
            image=request.image,
            prompt=request.prompt,
            size=request.size,
            n=request.n,
            strength=request.strength,
            negative_prompt=request.negative_prompt
        )
        return {
            "success": True,
            "model": "agnes-image-2.1-flash",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/image/sizes")
async def get_supported_sizes():
    """获取 Agnes Image 支持的图像尺寸"""
    return {
        "success": True,
        "sizes": agnes_service.get_supported_sizes()
    }