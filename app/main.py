"""FastAPI 主应用"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.skills import router as skills_router
from .core.base import registry
from .models.skill import Skill, SkillType, SkillPriority, ProcessStep, OutputConstraint

# 创建应用
app = FastAPI(
    title="AI Skill Framework",
    description="约束和规范 AI 回答思路的框架",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(skills_router)


def init_default_skills():
    """初始化默认 Skills"""
    
    # 编码类 Skill
    coding_skill = Skill(
        id="coding",
        name="编码任务",
        description="处理代码编写和调试任务",
        skill_type=SkillType.CODING,
        priority=SkillPriority.HIGH,
        process_steps=[
            ProcessStep(name="理解需求", description="分析用户要实现的功能", required=True, order=1),
            ProcessStep(name="设计方案", description="设计代码结构和实现方案", required=True, order=2),
            ProcessStep(name="编写代码", description="实现具体代码", required=True, order=3),
            ProcessStep(name="验证结果", description="检查代码正确性", required=True, order=4)
        ],
        output_constraints=OutputConstraint(
            format_hint="代码块 + 简要说明",
            must_include=["```"],
            must_exclude=["抱歉", "对不起"]
        ),
        guidelines=[
            "先理解需求再写代码",
            "代码要有注释",
            "给出完整可运行的代码",
            "说明关键实现思路"
        ],
        forbidden_actions=[
            "不要只给代码片段",
            "不要省略必要的 import",
            "不要过度解释基础概念"
        ],
        trigger_keywords=["写代码", "写", "代码", "实现", "编程", "开发", "bug", "调试", "函数", "类", "接口", "API", "脚本"],
        tags=["code", "development", "programming"]
    )
    
    # 研究类 Skill
    research_skill = Skill(
        id="research",
        name="研究分析",
        description="深入分析和研究问题",
        skill_type=SkillType.RESEARCH,
        priority=SkillPriority.HIGH,
        process_steps=[
            ProcessStep(name="收集信息", description="搜索和收集相关信息", required=True, order=1),
            ProcessStep(name="分析数据", description="对收集的信息进行分析", required=True, order=2),
            ProcessStep(name="得出结论", description="基于分析给出结论", required=True, order=3)
        ],
        guidelines=[
            "使用可靠的信息源",
            "区分事实和观点",
            "给出信息来源"
        ],
        forbidden_actions=[
            "不要编造数据",
            "不要忽略相反证据"
        ],
        trigger_keywords=["研究", "分析", "调查", "为什么", "原因"],
        tags=["research", "analysis"]
    )
    
    # 简洁回答 Skill
    concise_skill = Skill(
        id="concise",
        name="简洁回答",
        description="快速简洁地回答问题",
        skill_type=SkillType.ROUTINE,
        priority=SkillPriority.MEDIUM,
        process_steps=[
            ProcessStep(name="理解问题", description="快速理解用户意图", order=1),
            ProcessStep(name="直接回答", description="给出简洁答案", order=2)
        ],
        output_constraints=OutputConstraint(
            max_length=500
        ),
        guidelines=[
            "直接给出答案",
            "避免冗余解释",
            "一句话能说清楚就不用两句"
        ],
        forbidden_actions=[
            "不要重复问题",
            "不要过度铺垫"
        ],
        tags=["quick", "simple"]
    )
    
    # 图像生成 Skill
    image_gen_skill = Skill(
        id="image_generation",
        name="图像生成",
        description="使用 Agnes Image 2.1 Flash 生成图像",
        skill_type=SkillType.IMAGE_GENERATION,
        priority=SkillPriority.HIGH,
        process_steps=[
            ProcessStep(name="解析需求", description="分析用户要生成的图像内容", required=True, order=1),
            ProcessStep(name="构建提示词", description="根据需求构建结构化提示词", required=True, order=2),
            ProcessStep(name="调用API", description="调用 Agnes Image API 生成图像", required=True, order=3),
            ProcessStep(name="返回结果", description="返回生成的图像URL", required=True, order=4)
        ],
        output_constraints=OutputConstraint(
            format_hint="JSON 格式，包含图像 URL",
            must_include=["url"]
        ),
        guidelines=[
            "使用结构化提示词（主体+风格+细节）",
            "根据场景选择合适的图像尺寸",
            "添加适当的负面提示词提高质量"
        ],
        forbidden_actions=[
            "不要生成违法违规内容",
            "不要生成未经授权的人物肖像",
            "不要过度描述图像内容"
        ],
        trigger_keywords=["生成图片", "生成图像", "画", "图片", "图像", "设计", "插画", "海报", "logo", "封面"],
        tags=["image", "generation", "design", "art"]
    )
    
    # 注册默认 Skills
    registry.register(coding_skill)
    registry.register(research_skill)
    registry.register(concise_skill)
    registry.register(image_gen_skill)


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    init_default_skills()


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "AI Skill Framework",
        "version": "1.0.0",
        "description": "约束和规范 AI 回答思路的框架",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}