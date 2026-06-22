# AI Skill Framework

一个用于约束和规范 AI 回答思路的框架，注重过程和结果，避免回答过程繁琐。

## 项目简介

本项目通过定义 Skill（技能）来约束 AI 的回答行为。每个 Skill 包含：
- **触发关键词**：用于匹配用户查询
- **过程步骤**：定义回答的必经步骤
- **行为指导**：规范回答风格
- **禁止行为**：限制不当回答

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
uvicorn app.main:app --reload
```

服务启动后访问：
- API 文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/health

### 3. 测试 API

使用浏览器打开 http://127.0.0.1:8000/docs，可以直接测试所有 API 接口。

或使用 Python 测试：

```python
import requests

url = "http://127.0.0.1:8000/skills/process"
payload = {"query": "帮我写一个登录功能的代码"}

response = requests.post(url, json=payload)
print(response.json())
```

## API 接口

### 1. 处理查询

**POST** `/skills/process`

根据用户查询匹配 Skill，返回约束提示。

请求示例：
```json
{
  "query": "帮我写一个登录功能的代码",
  "task_type": null,
  "context": {}
}
```

响应示例：
```json
{
  "success": true,
  "output": "## 任务类型: coding\n## 优先级: high\n...",
  "matched_skill": "coding",
  "skill_name": "编码任务"
}
```

### 2. 查询所有 Skills

**GET** `/skills/`

返回所有已注册的 Skill 列表。

### 3. 查询指定 Skill

**GET** `/skills/{skill_id}`

返回指定 Skill 的详细信息。

### 4. 创建新 Skill

**POST** `/skills/`

创建新的 Skill。

请求示例：
```json
{
  "id": "my-skill",
  "name": "自定义技能",
  "description": "我的自定义 Skill",
  "skill_type": "routine",
  "priority": "medium",
  "trigger_keywords": ["关键词1", "关键词2"],
  "guidelines": ["指导原则1", "指导原则2"],
  "forbidden_actions": ["禁止行为1"],
  "tags": ["tag1", "tag2"]
}
```

### 5. 删除 Skill

**DELETE** `/skills/{skill_id}`

删除指定的 Skill。

### 6. 图像生成

**POST** `/skills/image/generate`

使用 Agnes Image 2.1 Flash 生成图像。

请求示例：
```json
{
  "prompt": "一只可爱的小猫，在草地上玩耍，阳光明媚",
  "size": "1024x1024",
  "n": 1,
  "negative_prompt": "模糊，低质量，丑陋"
}
```

响应示例：
```json
{
  "success": true,
  "model": "agnes-image-2.1-flash",
  "data": {
    "data": [
      {
        "url": "https://api.agnes-ai.com/image/xxx.png"
      }
    ]
  }
}
```

### 7. 图生图

**POST** `/skills/image/generate-from-image`

基于输入图像生成新图像。

请求示例：
```json
{
  "image": "https://example.com/input.jpg",
  "prompt": "将这幅图转换为水彩画风格",
  "size": "1024x1024",
  "strength": 0.7
}
```

### 8. 获取支持的尺寸

**GET** `/skills/image/sizes`

返回 Agnes Image 支持的所有图像尺寸。

## Agnes Image 2.1 Flash 集成

### 配置 API Key

使用图像生成功能需要配置 Agnes API Key：

```bash
# Windows PowerShell
$env:AGNES_API_KEY="your-api-key"

# Linux/Mac
export AGNES_API_KEY="your-api-key"
```

获取 API Key：https://platform.agnes-ai.com/settings/apiKeys

### 支持的图像尺寸

- 512x512
- 1024x1024
- 2048x2048
- 4096x4096
- 1024x768
- 768x1024
- 1920x1080
- 1080x1920
- 2560x1440
- 1440x2560

### 提示词构建建议

使用结构化提示词可以获得更好的效果：
```
主体描述, 艺术风格, 细节描述, 背景描述, 光照描述
```

示例：
```
一只可爱的橘猫, in the style of Studio Ghibli, 坐在窗台上, 背景是城市夜景, warm lighting
```

## 内置 Skills

项目内置了四个默认 Skill：

| Skill ID | 名称 | 触发关键词 | 用途 |
|----------|------|-----------|------|
| coding | 编码任务 | 写、代码、实现、编程、开发、bug、调试、函数、类、接口、API、脚本 | 处理代码编写和调试任务 |
| research | 研究分析 | 研究、分析、调查、为什么、原因 | 深入分析和研究问题 |
| concise | 简洁回答 | - | 快速简洁地回答简单问题 |
| image_generation | 图像生成 | 生成图片、生成图像、画、图片、图像、设计、插画、海报、logo、封面 | 使用 Agnes Image 2.1 Flash 生成图像 |

## Skill 匹配逻辑

1. **按类型匹配**：如果请求中指定了 `task_type`，优先按类型匹配
2. **按关键词匹配**：检查查询中是否包含 Skill 的触发关键词或标签
3. **默认 Skill**：如果没有匹配到任何 Skill，返回默认处理方式

## 项目结构

```
ai-skill-framework/
├── app/
│   ├── api/
│   │   └── skills.py      # API 路由定义（含图像生成接口）
│   ├── core/
│   │   ├── base.py        # Skill 注册表和执行器基类
│   │   └── processor.py   # Skill 处理器
│   ├── models/
│   │   └── skill.py       # Skill 数据模型（含图像生成类型）
│   ├── schemas/
│   │   └── request.py     # API 请求/响应模型
│   ├── services/
│   │   └── agnes_image.py # Agnes Image API 服务模块
│   └── main.py            # FastAPI 主应用
├── tests/
│   ├── test_processor.py  # 处理器测试
│   └── registry.py        # 注册表测试
├── requirements.txt       # 项目依赖
└── README.md              # 项目说明
```

## 扩展开发

### 添加新 Skill

在 `app/main.py` 的 `init_default_skills()` 函数中添加新 Skill：

```python
new_skill = Skill(
    id="my-custom-skill",
    name="自定义技能",
    description="处理特定类型的任务",
    skill_type=SkillType.ROUTINE,
    priority=SkillPriority.HIGH,
    trigger_keywords=["关键词1", "关键词2"],
    process_steps=[
        ProcessStep(name="步骤1", description="描述", required=True, order=1),
        ProcessStep(name="步骤2", description="描述", required=True, order=2)
    ],
    guidelines=["指导原则"],
    forbidden_actions=["禁止行为"],
    tags=["标签"]
)
registry.register(new_skill)
```

### 自定义 Skill 类型

在 `app/models/skill.py` 中扩展 `SkillType` 枚举：

```python
class SkillType(str, Enum):
    ROUTINE = "routine"
    CODING = "coding"
    RESEARCH = "research"
    IMAGE_GENERATION = "image_generation"
    MY_TYPE = "my_type"  # 新增类型
```

### 图像生成扩展

在 `app/services/agnes_image.py` 中可以扩展更多功能：

```python
# 添加自定义提示词模板
def build_product_prompt(self, product_name: str, style: str = "modern") -> str:
    """构建产品图提示词"""
    return f"product photography of {product_name}, {style} style, white background, studio lighting, high quality"

# 添加批量生成功能
def batch_generate(self, prompts: list[str], size: str = "1024x1024") -> list[dict]:
    """批量生成图像"""
    results = []
    for prompt in prompts:
        result = self.generate_image(prompt, size=size)
        results.append(result)
    return results
```

## 注意事项

1. **中文编码**：使用 PowerShell 的 `Invoke-RestMethod` 发送中文时可能有编码问题，建议使用浏览器或 Python 的 `requests` 库测试
2. **关键词匹配**：关键词匹配是子串匹配，查询中包含关键词的任意部分即可匹配
3. **优先级**：当多个 Skill 匹配时，选择优先级最高的 Skill（CRITICAL > HIGH > MEDIUM > LOW）
4. **图像生成**：使用图像生成功能需要先配置 AGNES_API_KEY 环境变量，获取地址：https://platform.agnes-ai.com/settings/apiKeys
5. **4K 分辨率**：4096x4096 等高分辨率图像生成时间较长，请耐心等待
6. **内容合规**：请勿生成违法违规或侵犯他人权益的图像内容